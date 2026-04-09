# Individual reflection — Le Huu Hung (AI20K001)

## 1. Role
- Phụ trách Canvas Template và User Stories-4Path.
- Thiết kế Mock data + Coding UI của demo.
- Điều chỉnh System Promp.

## 2. Đóng góp cụ thể
- Thiết kế Canvas Template cho AI Product và User Stories-4path. 
- Thiết kế User Stories-4path và Transition flow giữa các path.
- Thiết kế mock data, cụ thể cho bài như địa điểm trạm sạc, và khoảng cách.
- Điều chỉnh system prompt, convert sang tiếng anh để hạn chế token.

## 3. SPEC mạnh/yếu
- Mạnh nhất: failure modes — nhóm nghĩ ra được các case như "người dùng hoảng loạn không mô tả đúng tình trạng xe" hoặc "vị trí xe nằm ở vùng sóng yếu, GPS không chính xác". AI có mitigation cụ thể là giữ tone giọng bình tĩnh, đặt câu hỏi trắc nghiệm ngắn gọn (hết pin hay xịt lốp) và hướng dẫn tìm các cột mốc nhận diện xung quanh.

- Yếu nhất: ROI và Metrics — Việc giả định giảm thời gian xử lý từ 30-60 phút xuống còn dưới 5 phút hơi lạc quan nếu không tính đến độ trễ của đội cứu hộ thực tế. Nên tách rõ phần thời gian AI tiếp nhận thông tin và thời gian xe cứu hộ thực tế đến nơi để tính toán ROI chuẩn xác hơn.

## 4. Đóng góp khác
- Test prompt với nhiều kịch bản sự cố đa dạng (hết pin giữa cao tốc, lỗi phần mềm giữa đêm, xịt lốp trong hẻm nhỏ) để đảm bảo chatbot phân luồng (4-path) chuẩn xác, ghi log kết quả để tinh chỉnh prompt.

- Hỗ trợ team định nghĩa lại tiêu chí đánh giá (metrics) — trong tình huống khẩn cấp, "tốc độ phản hồi" và "tính súc tích" quan trọng hơn sự "thân thiện, dông dài". Đã chỉnh system prompt để AI trả lời ngắn gọn, đi thẳng vào phương án xử lý.

## 5. Điều học được
- Trước hackathon, tôi nghĩ làm AI chatbot chỉ cần prompt cho nó hiểu ý người dùng là đủ. Nhưng khi làm case cứu hộ VinFast và thiết kế luồng xử lý khoảng cách trạm sạc, tôi mới hiểu: AI trong tình huống khẩn cấp cần khả năng "tự động hóa quy trình" (thu thập vị trí, đối chiếu mock data khoảng cách, đưa ra quyết định gọi xe cứu hộ hay chỉ đường đến trạm). Việc thiết kế User Stories và Transition Flow chặt chẽ quan trọng không kém gì việc viết prompt.

## 6. Nếu làm lại
- Sẽ thử kết nối với một Map API thật (như Google Maps hoặc Mapbox) thay vì chỉ dùng mock data cho vị trí trạm sạc, để demo thực tế và thuyết phục hơn. Ngoài ra, sẽ test prompt bằng giọng nói (Voice-to-text) vì người dùng đang lái xe gặp sự cố thường ưu tiên gọi điện hơn là gõ phím.
## 7. AI giúp gì / AI sai gì
- **Giúp:** Dùng ChatGPT/Claude để generate nhanh các file JSON chứa mock data tọa độ, khoảng cách    
  trạm sạc và các tình huống xe hỏng, tiết kiệm được rất nhiều thời gian làm data giả. Dùng AI để hỗ trợ code UI nhanh cho bản demo.
- **Sai/mislead:** AI từng gợi ý thêm luồng "tự động kết nối với cổng OBD2 của xe để chẩn đoán mã lỗi phần cứng sâu" — tính năng này nghe cực kỳ ấn tượng nhưng hoàn toàn vượt quá scope của hackathon và tính khả thi trong thời gian ngắn. Nhóm suýt bị sa đà vào technical details (chi tiết kỹ thuật) nếu không kịp bám sát lại Problem Statement ban đầu là giải quyết khâu "giao tiếp thủ công mất 30-60p".