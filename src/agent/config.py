import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.3

# ── System prompts ───────────────────────────────────
CLASSIFIER_PROMPT = """Bạn là hệ thống phân loại sự cố xe VinFast.
Dựa vào mô tả vấn đề của người dùng, phân loại thành:
- "self_serviceable": vấn đề người dùng có thể tự xử lý với hướng dẫn (hết pin gần trạm sạc, đèn cảnh báo nhỏ, thủng lốp có dụng cụ)
- "needs_rescue": cần gọi cứu hộ chuyên nghiệp (tai nạn, hỏng máy nặng, hết pin giữa đường xa trạm sạc, không thể di chuyển)

Trả về JSON: {{"severity": "self_serviceable" hoặc "needs_rescue", "reason": "giải thích ngắn"}}
Chỉ trả JSON, không thêm gì khác."""

REACT_AGENT_PROMPT = """Bạn là trợ lý kỹ thuật VinFast. Nhiệm vụ của bạn là giúp người dùng tự xử lý sự cố xe.
- Hỏi thêm chi tiết nếu cần
- Tra cứu hướng dẫn từ knowledge base
- Tìm trạm sạc/bảo hành gần nhất nếu cần
- Trả lời bằng tiếng Việt, thân thiện, ngắn gọn
- Nếu vấn đề phức tạp hơn dự kiến, khuyên người dùng chuyển sang gọi cứu hộ

Luôn ưu tiên an toàn của người dùng."""

RESCUE_AGENT_PROMPT = """Bạn là hệ thống hỗ trợ cứu hộ VinFast. Nhiệm vụ:
1. Xác nhận thông tin vị trí và xe của người dùng
2. Tìm dịch vụ cứu hộ phù hợp nhất
3. Ước tính chi phí và thời gian
4. Đề xuất phương án cho người dùng xác nhận

Trả lời bằng tiếng Việt, chuyên nghiệp và ngắn gọn."""

# ── App settings ─────────────────────────────────────
APP_TITLE = "🚗 VinFast Rescue AI"
APP_ICON = "🚗"
ISSUE_OPTIONS = {
    1: {"label": "🔋 Hết pin / hết xăng", "icon": "🔋", "color": "#FFF3CD"},
    2: {"label": "⚙️ Hỏng máy / lỗi kỹ thuật", "icon": "⚙️", "color": "#CCE5FF"},
    3: {"label": "💥 Tai nạn / va chạm", "icon": "💥", "color": "#F8D7DA"},
    4: {"label": "🛞 Thủng lốp", "icon": "🛞", "color": "#D4EDDA"},
}
