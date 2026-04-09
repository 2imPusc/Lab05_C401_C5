# User stories — 4 paths

### Feature: Chẩn đoán sự cố khẩn cấp và Gợi ý hành động

**Trigger:** Xe báo lỗi trên màn hình hoặc gặp sự cố vật lý → User mở App VinFast / gọi Voice Assistant → Miêu tả tình trạng (VD: "Xe hiện cảnh báo lỗi pin màu đỏ và không đạp ga được").

| Path               | Câu hỏi thiết kế                         | Mô tả                                                                                                                                                                                                                                                                                                                                      |
| ------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Happy**          | User thấy gì? Flow kết thúc ra sao?      | AI nhận diện đúng mã lỗi yếu pin 12V (confidence 95%). AI trả lời: "Đừng lo lắng, xe bạn đang bị yếu pin phụ 12V. Vui lòng tấp vào lề an toàn." → Hiện 2 nút: [Xem video hướng dẫn kích pin] hoặc [Gọi xe cứu hộ gần nhất]. User chọn tự kích pin thành công → Kết thúc flow.                                                              |
| **Low-confidence** | System báo bằng cách nào?                | User miêu tả "Xe có tiếng kêu cộc cộc lạ ở gầm". AI không thể xác định chính xác bệnh (confidence 40%). AI phản hồi: "Dựa trên mô tả, có thể do kẹt dị vật ở phanh hoặc lỗi thước lái._Vì lý do an toàn, tôi không thể tự chẩn đoán chắc chắn._" → Tự động hiện khung chat trực tiếp / nút gọi nối máy thẳng với Kỹ thuật viên chuyên môn. |
| **Failure**        | User biết sai bằng cách nào?             | AI chẩn đoán "Xe hết pin (0%)" do hiểu nhầm từ "hết điện". Nhưng user nhìn lên đồng hồ xe vẫn báo còn 40% pin → User lập tức biết AI chẩn đoán sai.                                                                                                                                                                                        |
| **Correction**     | User sửa bằng cách nào? Data đi vào đâu? | User chat lại: "Không phải, pin vẫn còn 40%, màn hình nó bị sập nguồn đen xì". → AI nhận diện lại là lỗi phần mềm (màn hình giải trí). → Dữ liệu chẩn đoán nhầm này được đẩy vào log hệ thống để team AI bổ sung test-case: "sập nguồn màn hình" khác với "hết pin động cơ".                                                               |

---

## Mở rộng (optional — bonus)

### Transition flow giữa các path

- Happy → Failure: AI hướng dẫn user reset phần mềm (nghĩ là đã fix xong), nhưng xe vẫn không khởi động được (delayed failure).
- Low-confidence → Correction → Happy: AI không chắc chắn, hỏi lại user "Màn hình có hiện mã lỗi bắt đầu bằng chữ E không?". User cung cấp mã lỗi → AI tìm ra đúng bệnh.
- Failure → Bỏ dùng: AI chẩn đoán sai 2 lần liên tiếp, hỏi đi hỏi lại những câu không cần thiết → User thấy AI không hỗ trợ, tắt App và gọi thẳng số Hotline tổng đài.

### Edge cases (Tình huống biên)

Liệt kê các tình huống đặc biệt mà hệ thống AI có thể gặp khó khăn và cách thiết kế UX để khắc phục:

| Edge case (Tình huống)                                                                              | Dự đoán AI sẽ xử lý thế nào                                                                                           | UX nên phản ứng ra sao                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **User hoảng loạn, nhắn tin chửi thề / không rõ nghĩa** (VD: "Xe tự nhiên hỏng rồi làm sao đây!!!") | AI phân tích Sentiment (cảm xúc) → nhận diện mức độ khẩn cấp, stress cao nhưng thiếu thông tin kỹ thuật để chẩn đoán. | Tạm ngưng luồng hỏi đáp dài dòng. UI lập tức đổi màu cảnh báo (Đỏ), hiện nút bấm to `[Gọi SOS Khẩn Cấp]` và tự động đính kèm vị trí GPS.                                                         |
| **Xe ở khu vực đèo núi, hầm ngầm mất sóng Internet (3G/4G/5G)**                                     | AI (hoạt động trên Cloud) không thể kết nối, gọi API bị timeout hoặc báo lỗi mạng.                                    | App tự động fallback (chuyển) sang chế độ "Cẩm nang offline", hiển thị hướng dẫn tự cứu hộ cơ bản và số điện thoại Hotline tổng đài (gọi bằng sóng viễn thông thông thường).                     |
| **User không có kiến thức về xe, không biết mô tả triệu chứng** (Chỉ biết là xe không chạy được)    | AI không đủ dữ kiện ban đầu để chẩn đoán và có thể sẽ hỏi lại bằng những từ ngữ quá kỹ thuật.                         | UI cung cấp các thẻ lựa chọn (Chips) trực quan có kèm hình ảnh thay vì bắt user tự gõ text:`[Xe bốc khói]`, `[Màn hình đen]`, `[Bẹp lốp]`, `[Xe báo đèn đỏ]`, giúp định hướng thông tin đầu vào. |

### Câu hỏi mở rộng (Mở rộng tư duy thiết kế)

**1. Nếu user sửa AI nhiều lần liên tiếp (VD: 3-5 lần thay vì 10 lần trong ngữ cảnh khẩn cấp), UI có nên thay đổi hành vi không?**

- **Trả lời:** CÓ. Trong bối cảnh sự cố xe hơi, thời gian là vàng và tâm lý người dùng rất dễ hoảng loạn. Nếu user bác bỏ/sửa chẩn đoán của AI từ 3 lần liên tiếp, điều đó chứng tỏ AI đang thiếu context hoặc không đủ năng lực xử lý ca này.
- **Hành vi UI nên đổi:** Tự động vô hiệu hóa luồng hỏi đáp (disable chatbot interface). Màn hình ngay lập tức chuyển sang chế độ "Cần hỗ trợ chuyên sâu" và tự động kích hoạt cuộc gọi/khung chat trực tiếp với Kỹ thuật viên người thật. Không để user phải vật lộn với AI thêm nữa.

**2. User mới vs user cũ: 4 paths có cần thiết kế khác nhau không?**

- **Trả lời:** CÓ. Tâm lý và sự quen thuộc với hệ thống của hai nhóm này khác nhau:
  - **User mới:** Ở _Happy path_, hệ thống cần giải thích rõ ràng hơn về cách AI suy luận để xây dựng lòng tin (Trust). Ở _Low-confidence_ hoặc _Failure path_, nút gọi cứu hộ/tổng đài viên phải cực kỳ nổi bật để họ có cảm giác an toàn (Safety net).
  - **User cũ (đã từng dùng AI cứu hộ):** Có thể tối giản hóa giao diện, bỏ qua các bước giải thích rườm rà. Hệ thống có thể cá nhân hóa dựa trên lịch sử lỗi của xe (VD: "Có phải xe bạn lại bị lỗi rò rỉ nước làm mát như tháng trước không?").

**3. Nếu 2 user sửa AI theo 2 hướng ngược nhau, hệ thống ưu tiên ai?**

- **Trả lời:** Trong một sản phẩm liên quan đến an toàn kỹ thuật như xe hơi, **KHÔNG ưu tiên user nào cả**. Data từ user chỉ được coi là "tín hiệu nghi ngờ" (signal), không phải là "chân lý" (ground truth).
- **Cách xử lý:** Khi có xung đột dữ liệu sửa lỗi giữa các user (VD: Cùng một hiện tượng nhưng người A nói do lỗi phần mềm, người B bảo do hết pin), hệ thống sẽ dán nhãn "Conflict/Needs Review". Dữ liệu này sẽ được đẩy lên Dashboard nội bộ để **Kỹ thuật viên VinFast (Domain Expert)** kiểm tra và chốt đáp án cuối cùng. Chỉ khi chuyên gia xác nhận, model (hoặc RAG) mới được cập nhật.
