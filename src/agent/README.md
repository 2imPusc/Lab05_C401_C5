# 🚗 VinFast Rescue AI Agent

AI chatbot hỗ trợ xử lý sự cố xe VinFast — chạy trên Streamlit.

## Cài đặt

```bash
# 1. Tạo virtual environment
python -m venv venv

# 2. Kích hoạt venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Cài dependencies
pip install -r requirements.txt
```

## Cấu hình

Tạo file `.env` trong thư mục `agent/`:

```env
CHATGPT_API_KEY=sk-your-openai-api-key-here
```

## Chạy app

```bash
streamlit run app.py
```

App sẽ mở tại `http://localhost:8501`.

## Cấu trúc project

```
agent/
├── app.py                # Entry point Streamlit
├── config.py             # API keys, prompts, constants
├── core/
│   ├── classifier.py     # Phân loại sự cố (LLM)
│   ├── react_agent.py    # ReAct agent — nhánh tự xử lý
│   └── rescue_agent.py   # Flow cứu hộ — nhánh phức tạp
├── tools/
│   ├── db_lookup.py      # Tra cứu KB + tìm trạm gần nhất
│   ├── gps_tool.py       # Lấy vị trí GPS (mock)
│   └── vehicle_info.py   # Thông tin xe (mock)
├── data/
│   ├── stations.json     # DB trạm sạc/bảo hành
│   └── troubleshoot_kb.json  # Knowledge base sự cố
└── ui/
    ├── components.py     # UI components (buttons, cards)
    └── chat_ui.py        # State machine + session state
```
