import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

# ── Function to load prompts from XML ────────────────
def load_prompts_from_xml(file_path="prompts.xml"):
    """
    Đọc file XML và chuyển thành dictionary để dễ truy cập.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Chuyển các tag thành key (viết hoa) và nội dung thẻ thành value
        return {child.tag.upper(): child.text.strip() for child in root}
    except FileNotFoundError:
        print(f"⚠️ Warning: {file_path} not found. Using empty prompts.")
        return {}
    except Exception as e:
        print(f"⚠️ Error parsing XML: {e}")
        return {}

# Load prompts một lần duy nhất khi khởi động app
PROMPTS_DICT = load_prompts_from_xml()

# ── LLM ──────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.3

# ── System prompts (Lấy từ Dictionary) ───────────────
# Sử dụng .get() để tránh lỗi nếu file XML thiếu thẻ
CLASSIFIER_PROMPT = PROMPTS_DICT.get("CLASSIFIER_PROMPT", "")
REACT_AGENT_PROMPT = PROMPTS_DICT.get("REACT_AGENT_PROMPT", "")
RESCUE_AGENT_PROMPT = PROMPTS_DICT.get("RESCUE_AGENT_PROMPT", "")

# ── App settings ─────────────────────────────────────
APP_TITLE = "🚗 VinFast Rescue AI"
APP_ICON = "🚗"
ISSUE_OPTIONS = {
    1: {"label": "🔋 Hết pin / hết xăng", "icon": "🔋", "color": "#FFF3CD"},
    2: {"label": "⚙️ Hỏng máy / lỗi kỹ thuật", "icon": "⚙️", "color": "#CCE5FF"},
    3: {"label": "💥 Tai nạn / va chạm", "icon": "💥", "color": "#F8D7DA"},
    4: {"label": "🛞 Thủng lốp", "icon": "🛞", "color": "#D4EDDA"},
}