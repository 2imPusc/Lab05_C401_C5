"""Phân loại sự cố: tự xử được hay cần cứu hộ."""

import json
import unicodedata
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, CLASSIFIER_PROMPT

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _remove_accents(text: str) -> str:
    """Bỏ dấu tiếng Việt để so sánh fuzzy (VD: 'hết pin' → 'het pin')."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _compute_confidence(issue_option: int, user_description: str) -> str:
    """
    Rule-based confidence: dựa vào KB keyword matching + độ dài input.
    Không dùng LLM để tránh hallucination.

    Logic:
    - Tai nạn (option 3) → luôn "high"
    - Chỉ chọn nút, không mô tả → "medium"
    - Có match keyword trong KB → "high"
    - Không match + mô tả ngắn (<15 ký tự) → "low"
    - Không match + mô tả dài → "medium"

    Returns: "high" | "medium" | "low"
    """
    if issue_option == 3:
        return "high"

    if not user_description.strip():
        return "medium"

    with open(_DATA_DIR / "troubleshoot_kb.json", "r", encoding="utf-8") as f:
        kb = json.load(f)

    # So sánh cả có dấu và không dấu để handle user gõ không dấu
    desc_lower = user_description.lower()
    desc_no_accent = _remove_accents(user_description)

    total_keyword_hits = 0
    for entry in kb:
        for kw in entry["keywords"]:
            kw_no_accent = _remove_accents(kw)
            if kw in desc_lower or kw_no_accent in desc_no_accent:
                total_keyword_hits += 1

    if total_keyword_hits == 0 and len(user_description.strip()) < 15:
        return "low"

    if total_keyword_hits == 0:
        return "medium"

    return "high"


def classify_issue(issue_option: int, user_description: str = "") -> dict:
    """
    Phân loại sự cố dựa vào option chọn + mô tả bổ sung.

    Returns:
        {"severity": "self_serviceable"|"needs_rescue",
         "confidence": "high"|"medium"|"low",
         "reason": "..."}
    """
    option_map = {
        1: "Hết pin / hết xăng",
        2: "Hỏng máy / lỗi kỹ thuật",
        3: "Tai nạn / va chạm",
        4: "Thủng lốp",
    }

    issue_text = option_map.get(issue_option, "Không xác định")
    if user_description:
        issue_text += f". Chi tiết thêm: {user_description}"

    # Rule-based confidence (không phụ thuộc LLM)
    confidence = _compute_confidence(issue_option, user_description)

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=0,
    )

    response = llm.invoke([
        SystemMessage(content=CLASSIFIER_PROMPT),
        HumanMessage(content=f"Vấn đề: {issue_text}"),
    ])

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        if issue_option == 3:
            result = {"severity": "needs_rescue", "reason": "Tai nạn cần hỗ trợ chuyên nghiệp"}
        else:
            result = {"severity": "self_serviceable", "reason": "Vấn đề có thể tự xử lý với hướng dẫn"}

    result["confidence"] = confidence
    return result
