# SPEC Draft | Nhóm C5 | Phòng C401
## Track: VinFast

---

## Problem Statement

Khi xe VinFast gặp sự cố (hết pin, lỗi kỹ thuật), người dùng phải gọi tổng đài cứu hộ để được hỗ trợ. Tuy nhiên, quy trình hiện tại phụ thuộc nhiều vào trao đổi thủ công — bao gồm xác nhận vị trí, tình trạng xe và phương án xử lý — thường mất 30–60 phút hoặc lâu hơn khi hệ thống quá tải. Trong thời gian này, người dùng không có lựa chọn thay thế đáng tin cậy, gây ra sự bất tiện, lo lắng và giảm trải nghiệm dịch vụ.

---

## Canvas Draft

| | Value | Trust | Feasibility |
|---|---|---|---|
| **Trả lời** | **User:** Chủ xe VinFast, người lái xe điện (VF e34, VF 5, VF 8, VF 9...). **Pain:** Mất thời gian khi tra cứu thông tin kỹ thuật/mã lỗi; hoảng loạn khi xe gặp sự cố khẩn cấp mà không biết gọi ai; thao tác thủ công để tìm trạm sạc hoặc đặt lịch bảo trì mất nhiều bước. **Value:** Đơn giản hóa tra cứu kỹ thuật/lỗi, kết nối cứu hộ tức thời trong tình huống khẩn cấp, tiết kiệm thời gian vận hành. | **Recall cao hơn Precision** — Thà gọi cứu hộ dư còn hơn bỏ sót người cần cứu. **Nếu sai:** Sai chẩn đoán (hết pin → gợi ý thay lốp); sai mức độ nghiêm trọng; sai hướng dẫn xử lý. **Minh bạch hóa:** Hiển thị confidence %, reasoning từng bước, luôn có nút `[ Gọi kỹ thuật viên ]`. **Feedback loop:** User correction + Technician correction; quick recovery khi AI nhận phản hồi sai. | **Cost/latency:** API LLM ~¢1–2/lượt, target latency <5 giây. **Risks:** Chatbot phụ thuộc vào sự sẵn có của dịch vụ cứu hộ; dịch vụ không tuân theo giá thỏa thuận qua LLM; người dùng ngoài vùng phủ hoặc khu vực khó tiếp cận; LLM có thể hallucinate tên dịch vụ cứu hộ không tồn tại. |

**Auto hay Augmentation?** Augmentation — AI gợi ý, người dùng và kỹ thuật viên quyết định cuối cùng.

**Learning signal:** Người dùng chọn phương án nào sau gợi ý AI → so sánh với phương án thực tế được thực hiện → correction signal.

---

## Hướng Đi Chính

### Prototype
Phát triển chatbot xử lý yêu cầu cứu hộ qua 3 bước xác thực nhanh:

1. **Nhận diện sự cố:** Phân loại nhanh tình trạng (xe hỏng máy, thủng lốp, hết pin/xăng, tai nạn).
2. **Xác định vị trí & Định danh:** Tự động lấy tọa độ GPS từ thiết bị và thông tin xe (VIN/Biển số).
3. **Điều phối:** Gợi ý trạm bảo hành hoặc xe cứu hộ gần nhất kèm thời gian chờ dự kiến (ETA).

### Eval Metrics
- Độ chính xác vị trí: Sai số < 50m.
- Tỉ lệ chuyển đổi (Completion Rate): ≥ 90% người dùng hoàn thành yêu cầu cứu hộ qua bot mà không cần bấm "Gọi tổng đài viên".
- Thời gian xử lý: Từ lúc bắt đầu chat đến khi phát lệnh cứu hộ < 60 giây.

### Main Failure Modes
- Người dùng ở khu vực mất sóng hoặc GPS không chính xác.
- Mô tả sự cố không rõ ràng (ví dụ: "xe không chạy được" nhưng không rõ do phần mềm hay phần cứng) → điều động sai loại xe cứu hộ (xe kéo vs. xe sửa chữa lưu động).

---

## Phân Công

| Thành viên | Nhiệm vụ |
|---|---|
| **Phúc** | Admin tasks — nộp Canvas draft, tạo GitHub, manage commits. |
| **Khánh Nam** | Brainstorm pain points VinFast + viết Problem Statement. |
| **Hưng** | Brainstorm pain points VinUni + viết Hướng đi chính. |
| **Tú Nam** | Brainstorm pain points VinUni + làm cột Trust trong Canvas. |
| **Hiếu** | Brainstorm pain points VinMec + làm cột Value trong Canvas. |
| **Quân** | Brainstorm pain points XanhSM + làm cột Feasibility trong Canvas. |
