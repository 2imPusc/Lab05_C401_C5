"""Phân loại sự cố: tự xử được hay cần cứu hộ."""

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, CLASSIFIER_PROMPT


def classify_issue(issue_option: int, user_description: str = "") -> dict:
    """
    Phân loại sự cố dựa vào option chọn + mô tả bổ sung.

    Returns:
        {"severity": "self_serviceable"|"needs_rescue", "reason": "..."}
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
        # Fallback: tai nạn luôn cần cứu hộ, còn lại mặc định tự xử
        if issue_option == 3:
            result = {"severity": "needs_rescue", "reason": "Tai nạn cần hỗ trợ chuyên nghiệp"}
        else:
            result = {"severity": "self_serviceable", "reason": "Vấn đề có thể tự xử lý với hướng dẫn"}

    return result

