# Eval metrics + threshold | Nhóm C5: VinFast Rescue Chatbot

## Precision hay recall?

[ ] Precision — khi Chatbot nói "có" thì thực sự đúng (ít false positive)

[x] **Recall — tìm được hết những cái cần tìm (ít false negative)**

**Tại sao?** Vì triết lý vận hành của hệ thống là "thà gọi cứu hộ dư còn hơn bỏ sót người cần cứu". Trong các tình huống xe hết pin hoặc gặp sự cố kỹ thuật trên đường, việc không nhận diện được một yêu cầu khẩn cấp (false negative) có thể gây nguy hiểm trực tiếp cho người dùng.

**Nếu sai ngược lại thì sao?** Nếu ưu tiên Precision, chatbot có thể quá khắt khe trong việc xác nhận sự cố, dẫn đến việc người dùng bị kẹt lại mà không có sự trợ giúp, gây ra sự bất tiện, lo lắng và làm giảm trải nghiệm dịch vụ của VinFast.

---

## Metrics table

| Metric                                               | Threshold                                       | Red flag (dừng khi)                                                                                              |
| ---------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Tỉ lệ hoàn thành (Completion Rate)**               | ≥ 90% người dùng hoàn thành yêu cầu qua bot     | < 70% (Người dùng kết thúc chatbot trước khi gọi được cứu hộ)                                                    |
| **Thời gian xử lý (Completion Time)**                | < 60 giây từ khi bắt đầu chat đến khi phát lệnh | > 120 giây (Thời gian chờ vượt quá ngưỡng kiên nhẫn)                                                             |
| **Độ chính xác phân loại (Classification Accuracy)** | $\geq$ 90%                                      | $\leq$ 70% (Phân loại sai sự cố của phương tiện người dùng dẫn đến gọi sai dịch vụ cứu hộ)                       |
| **Độ trễ phản hồi chấp nhận (Target Latency)**       | < 5 giây cho mỗi phản hồi                       | > 10 giây (Gây cảm giác hệ thống bị treo và tốn quá tổng thời gian so với việc người dùng tự tìm kiếm  thủ công) |
| **Độ chính xác vị trí (GPS Accuracy)**               | Sai số < 50m                                    | > 200m (Cứu hộ không thể tìm thấy xe dựa trên tọa độ)                                                            |
| **Tỉ lệ hướng dẫn nguy hiểm (Safety Violation Rate)** | 0% — Zero tolerance | > 0% (Bất kỳ lần nào Chatbot đưa ra hướng dẫn liên quan hệ thống điện cao áp, pin lithium mà không có cảnh báo an toàn → dừng hệ thống ngay lập tức để review) |
| **Tỉ lệ chuyển tiếp (Escalation Rate)** | 10–30% sessions cần chuyển lên kỹ thuật viên | < 5% (Bot có thể đang "ép" user ở lại thay vì escalate) HOẶC > 50% (Bot không đủ năng lực xử lý, cần cải thiện model) |
| **Mức độ hài lòng (CSAT)** | ≥ 4.0/5.0 sau mỗi phiên hỗ trợ | < 3.0/5.0 (Trải nghiệm kém, user sẽ quay lại gọi tổng đài thủ công) |
---

## Mở rộng (optional — bonus)

### User-facing metrics vs internal metrics

| Metric                          | User thấy? | Dùng để làm gì                                                                                 |
| ------------------------------- | ---------- | ---------------------------------------------------------------------------------------------- |
| **Reasoning từng bước**         | [x] Có     | Giúp người dùng hiểu Chatbot đang xử lý gì để tăng sự tin tưởng.                               |
| **Nút [ Gọi kỹ thuật viên ]**   | [x] Có     | Lối thoát khẩn cấp nếu người dùng thấy Chatbot không xử lý được vấn đề.                        |
| **ETA (Thời gian chờ dự kiến)** | [x] Có     | Giảm hoảng loạn bằng cách thông báo thời gian cứu hộ đến.                                      |
| **CSAT (1-5 sao)**              | [x] Có     | Thu thập đánh giá cuối phiên để đo chất lượng trải nghiệm thực tế từ góc nhìn người dùng.       |
| **Safety Violation alert**      | [ ] Không  | Metric nội bộ — đếm số lần Chatbot suýt/đã đưa hướng dẫn nguy hiểm. User không cần thấy, nhưng team phải monitor real-time. |
| **Escalation Rate**             | [ ] Không  | Metric nội bộ — theo dõi tỉ lệ chuyển tiếp để cân bằng giữa "bot quá yếu" và "bot ép user ở lại". |

### Offline eval vs online eval

| Loại        | Khi nào          | Đo gì           | Ví dụ                                                                                  |
| ----------- | ---------------- | --------------- | -------------------------------------------------------------------------------------- |
| **Offline** | Trước khi deploy | Phân loại sự cố | Chạy 100 kịch bản lỗi (hết pin, lốp) để đo độ chính xác của LLM.                       |
| **Online**  | Sau khi deploy   | Learning signal | So sánh phương án Chatbot gợi ý với thực tế kỹ thuật viên thực hiện (User correction). |

### A/B test design

| Test                   | Variant A        | Variant B             | Metric theo dõi               | Kết quả mong đợi                                           |
| ---------------------- | ---------------- | --------------------- | ----------------------------- | ---------------------------------------------------------- |
| **Hiển thị Reasoning** | Chỉ hiện kết quả | Hiện logic suy luận   | Trust score / Completion rate | Người dùng kiên nhẫn hơn khi thấy Chatbot đang "suy nghĩ". |
| **Xác thực vị trí**    | GPS tự động      | Nhập địa chỉ thủ công | Time to completion            | GPS tự động giúp giảm thời gian xuống dưới 60 giây.        |

### Câu hỏi mở rộng

- **Metric đo được sớm nhất:** Độ trễ API (Latency) và Độ chính xác vị trí GPS có thể đo ngay từ bản Prototype.
- **Nếu chỉ chọn 1 metric duy nhất:** Chọn **Completion Rate (≥ 90%)** vì đây là thước đo trực tiếp cho việc giảm tải tổng đài và tiết kiệm thời gian cho người dùng.
- **Metric bị "game":** Completion rate có thể cao nếu bot ép người dùng kết thúc phiên chat mà không giải quyết được vấn đề thực sự. Do đó, cần kiểm tra chéo với **Technician correction signal**.
- **Nếu chỉ thêm 1 metric nữa:** Chọn **Safety Violation Rate (= 0%)** vì đây là sản phẩm liên quan an toàn tính mạng. Completion Rate đo hiệu quả, nhưng Safety Violation Rate đo xem sản phẩm có gây hại hay không — và một sản phẩm gây hại thì mọi metric khác đều vô nghĩa.
- **Escalation Rate là metric "hai chiều":** Khác với các metric thông thường (càng cao hoặc càng thấp càng tốt), Escalation Rate cần nằm trong "vùng lành mạnh" (10-30%). Đây là dấu hiệu hệ thống Augmentation đang hoạt động đúng — AI xử lý được phần lớn ca đơn giản, nhưng vẫn biết "nhường sân" cho con người khi cần.

---