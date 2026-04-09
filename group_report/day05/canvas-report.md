# AI Product Canvas — template

Điền Canvas cho product AI của nhóm. Mỗi ô có câu hỏi guide — trả lời trực tiếp, xóa phần in nghiêng khi điền.

---

## Canvas

|                   | Value                                                                                                                                                                                                                                                                                                                                           | Trust                                                                                                                                                                                                                                                                                                                              | Feasibility                                                                                                                                                                                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được?                                                                                                                                                                                                                                                                           | Khi AI sai thì user bị ảnh hưởng thế nào?<br />User biết AI sai bằng cách nào? <br />User sửa bằng cách nào?                                                                                                                                                                                                                       | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì?                                                                                                                                                                                                         |
| **Trả lời**       | **User:** Khách hàng (KH) tra cứu chuyến bay, đặt vé máy bay<br /><br />**Pain:** Mất thời gian tìm kiếm thông tin, thao tác tay phức tạp<br />và tự điền thông tin thủ công.<br /><br />**AI Solution:** Chuyển ngôn ngữ tự nhiên thành bộ lọc vé ngay lập tức<br />dẫn thẳng tới trang thanh toán để tăng tỷ lệ chuyển đổi (Conversion Rate). | **Ảnh hưởng:** User bị sai lệch thông tin chuyến bay, <br />ngày giờ hoặc thông tin cá nhân.<br /><br />**Nhận biết:** Qua bước xác nhận (Confirm) và <br />hiển thị quá trình truy xuất (Showing Work).<br /><br />**Sửa lỗi:** Phản hồi lại câu lệnh mới, sửa thông tin trong form gợi ý<br /> hoặc chuyển sang nhân viên hỗ trợ | **Cost:** Chi phí gọi API LLM và API hệ thống vé (khoảng 0,01 - 0,02 USD/request).<br />: Mục tiêu dưới 5 giây (phản hồi thời gian thực). <br />: API bị giới hạn (Rate limit), dữ liệu từ hệ thống không hợp lệ <br />hoặc thông tin vé bị lỗi thời (Stale data). |

---

## Automation hay augmentation?

☐ Automation — AI làm thay, user không can thiệp
☑ **Augmentation — AI gợi ý, user quyết định cuối cùng**

**Justify:** Vì nghiệp vụ hàng không yêu cầu Precision (Độ chính xác) cao. Việc AI gợi ý các thẻ vé (Cards) để user tự tay xác nhận trước khi thanh toán giúp triệt tiêu rủi ro đặt nhầm vé khi AI gặp lỗi xác suất.

## Learning signal

| #   | Câu hỏi                                                                                                   | Trả lời                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | User correction đi vào đâu?                                                                               | Lưu vào Database để phân loại các dạng lỗi (Failure Mode Library) và dùng làm dữ liệu tinh chỉnh (Fine-tuning)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 2   | Product thu signal gì để biết tốt lên hay tệ đi?                                                          | **Tín hiệu tốt** (Positive Signals - Model đang làm tốt), tỷ lệ chuyển đổi (Conversion Rate) tăng, user click chọn ngay các thẻ vé (Cards) do AI gợi ý ở câu lệnh đầu tiên (First-prompt success rate). Thời gian (Latency/Time-to-checkout) từ lúc gõ câu lệnh đến lúc hoàn tất thanh toán giảm.<br>**Tín hiệu xấu** (Negative Signals - Model đang làm tệ): User phải gõ/sửa lại câu lệnh nhiều lần. User phải chỉnh sửa lại các trường thông tin (điểm đi, điểm đến, ngày bay) ở bước Xác nhận (Confirm) do AI trích xuất sai. User bỏ qua gợi ý của AI và quay lại dùng bộ lọc thủ công truyền thống. Tỷ lệ thoát (Drop-off rate) ở bước hiển thị kết quả cao. |
| 3   | Data thuộc loại nào? ☐ User-specific · ☐ Domain-specific · ☐ Real-time · ☐ Human-judgment · ☐ Khác:\_\_\_ | **Domain-specific**: Dữ liệu đặc thù của ngành hàng không (cách người Việt gọi tên sân bay, mã IATA, từ lóng, cách viết tắt ngày tháng/dịp lễ Tết).<br> **Human-judgment**: Quyết định của user ở bước cuối cùng (click chọn vé nào, sửa thông tin gì) chính là nhãn dán (label) chất lượng nhất để đánh giá AI đúng hay sai. <br> **User-specific** (tùy chọn thêm): Lịch sử hành vi, sở thích bay (thích bay sáng/tối, thích hãng giá rẻ hay VNA) của từng khách hàng cụ thể để cá nhân hóa gợi ý thẻ vé.                                                                                                                                                        |

**Có marginal value không?** (Model đã biết cái này chưa? Ai khác cũng thu được data này không?)
Có Marginal Value rất cao.

Justify: Các mô hình LLM nền tảng (Foundation Models) có thể hiểu ngôn ngữ tự nhiên cơ bản, nhưng chúng không nắm bắt được thói quen gõ tìm kiếm, các lỗi sai phổ biến (Failure Modes) và hành vi chốt đơn đặc thù của tệp khách hàng nội địa trên hệ thống của bạn.

Dữ liệu sửa lỗi từ UI (User thao tác sửa ngày, đổi chuyến) là dữ liệu độc quyền (Proprietary data) sinh ra từ luồng sản phẩm của riêng bạn, các đối thủ cạnh tranh hoặc các LLM chung chung bên ngoài không thể tự nhiên có được để fine-tune.

---

## Cách dùng

1. Điền Value trước — chưa rõ pain thì chưa điền Trust/Feasibility
2. Trust: trả lời 4 câu UX (đúng → sai → không chắc → user sửa)
3. Feasibility: ước lượng cost, không cần chính xác — order of magnitude đủ
4. Learning signal: nghĩ về vòng lặp dài hạn, không chỉ demo ngày mai
5. Đánh [?] cho chỗ chưa biết — Canvas là hypothesis, không phải đáp án
