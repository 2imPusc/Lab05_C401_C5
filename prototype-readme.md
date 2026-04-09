# Prototype — Hệ thống hỗ trợ cứu hộ xe điện cho VinFast 

## Mô tả
Khi xe VinFast gặp sự cố khẩn cấp (hết pin, lỗi kỹ thuật), người dùng phải mất 30-60 phút gọi tổng đài và chờ xử lý thủ công; AI Assistant sẽ tự động chẩn đoán lỗi tức thời và điều phối cứu hộ, giúp rút ngắn thời gian tiếp nhận xuống dưới 60 giây.



## Level: Mock prototype
- UI build demo nhanh bằng Streamlit
- 1 flow chính chạy thật: **nhập mô tả sự cố xe → nhận chẩn đoán hoặc gợi ý phương án cứu hộ**

## Links
- Sketch: https://drive.google.com/file/d/1g4SwT_Ng6sgcf6qDW1Dwehcwfb0l77lL/view?usp=drive_link
- Mock Prototype: https://www.figma.com/design/sQgQ21NckKnaFcvuI3MVyA/UI-UX?node-id=3-18&p=f
- Video demo (backup): https://drive.google.com/file/d/1L31hed_n0w8ZQXCax5aTLG30hfvokHGk/view?usp=drive_link

## Tools
- UI: Streamlit
- AI: OpenAI (gpt-4o-mini)
- Prompt: system prompt + few-shot examples cho 10 sự cố xe phổ biến nhất (VD: báo lỗi pin đỏ, xịt lốp, không khởi động được, sập màn hình...)

## Phân công
| Thành viên | Phần | Output |
|-----------|------|--------|
| Phúc | slides | dem-slides.pdf |
| Khánh Nam | Sketch | Prototype |
| Hưng | Canvas, User Story 4 paths | spec/spec-final.md phần 1,2|
| Tú Nam | Mock Prototype | Prototype |
| Hiếu | Roi-3-Scenarios, Mini-AI-Spec | spec/spec-final.md phần 5,6 |
| Quân | Eval-metrics, Failure-Modes | spec/spec-final.md phần 3,4 |
