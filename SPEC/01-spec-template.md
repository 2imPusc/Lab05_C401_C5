# SPEC — AI Product Hackathon

**Nhóm:** C5 (Phúc, Khánh Nam, Hưng, Tú Nam, Hiếu, Quân)
**Track:** ☑ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool · ☐ XanhSM · ☐ Open
**Problem statement (1 câu):** Khi xe VinFast gặp sự cố khẩn cấp (hết pin, lỗi kỹ thuật), người dùng phải mất 30-60 phút gọi tổng đài và chờ xử lý thủ công; AI Assistant sẽ tự động chẩn đoán lỗi tức thời và điều phối cứu hộ, giúp rút ngắn thời gian tiếp nhận xuống dưới 60 giây.

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | **User:** Chủ xe điện VinFast.<br>**Pain:** Chờ đợi cứu hộ lâu, hoảng loạn khi gặp sự cố, khó tra cứu mã lỗi.<br>**AI giải:** Chẩn đoán lỗi tức thời qua giọng nói/text, hướng dẫn xử lý hoặc tự động điều xe cứu hộ ngay lập tức. | **AI sai:** Sai chẩn đoán dẫn đến điều sai xe hoặc gây mất an toàn.<br>**User biết:** Hiển thị *Reasoning* từng bước và *Confidence %*.<br>**Cách sửa:** Luôn hiển thị nút `[Gọi kỹ thuật viên]` để user thoát khỏi flow AI. | **Cost:** ~$0.05 - $0.1/session.<br>**Latency:** < 3 giây/phản hồi.<br>**Risk:** AI bịa ra dịch vụ cứu hộ không có thật (Hallucination); Xe mất sóng 4G/5G ở hầm ngầm/đèo núi. |

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation
**Justify:** Sự cố xe hơi liên quan trực tiếp đến an toàn tính mạng. AI chỉ làm "Tổng đài viên Triage" (phân loại sự cố). Quyết định chốt phương án cứu hộ BẮT BUỘC do con người (User/Kỹ thuật viên) xác nhận.

**Learning signal:**
1. User correction đi vào đâu? Lịch sử chat và quyết định thực tế cuối cùng (do KTV hoặc user chốt) được ghi thành `correction log` để cập nhật Knowledge Base (RAG) hoặc fine-tune model.
2. Product thu signal gì để biết tốt lên hay tệ đi?
   * *Implicit:* Tỷ lệ phiên kết thúc thành công không cần escalate (chuyển tiếp) lên người thật.
   * *Explicit:* CSAT (1-5 sao) sau phiên hỗ trợ.
   * *Correction:* Sự chênh lệch giữa mã lỗi thực tế thợ ghi nhận và mã AI chẩn đoán.
3. Data thuộc loại nào? ☐ User-specific · ☑ Domain-specific (Lỗi nội bộ VinFast) · ☐ Real-time · ☑ Human-judgment (Thợ kỹ thuật) · ☐ Khác: ___
   **Có marginal value không?** Cực kỳ cao. LLM chung trên thị trường không có dữ liệu mã lỗi nội bộ hay firmware mới nhất của VinFast. Việc thu thập data thực tế sẽ tạo Knowledge Base độc quyền, tạo rào cản cạnh tranh cực lớn.

---

## 2. User Stories — 4 paths

### Feature: Chẩn đoán sự cố khẩn cấp & Gợi ý hành động

**Trigger:** Xe báo lỗi trên màn hình hoặc gặp sự cố trên đường → User mở App VinFast / Voice Assistant → Mô tả tình trạng (VD: "Màn hình báo lỗi pin màu đỏ và xe không chạy được").

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy** | User thấy gì? Flow kết thúc ra sao? | AI nhận diện đúng mã lỗi yếu pin 12V (confidence 95%). AI trả lời trấn an, hướng dẫn đỗ xe an toàn và hiện 2 nút: `[Xem video tự kích pin]` hoặc `[Gọi xe cứu hộ gần nhất]`. User tự kích pin thành công → Hoàn thành. |
| **Low-confidence** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI chẩn đoán confidence < 50% (VD: user tả tiếng kêu lạ). AI phản hồi: *"Vì lý do an toàn, tôi không thể tự chẩn đoán chắc chắn"* → Tự động hiện khung chat trực tiếp / nút nối máy thẳng với Kỹ thuật viên. |
| **Failure** | User biết AI sai bằng cách nào? Recover ra sao? | AI báo "Xe hết pin (0%)" nhưng màn hình xe vẫn báo còn 40%. User lập tức biết AI sai dựa vào quan sát thực tế → Bấm nút gọi KTV hoặc chat lại để sửa AI. |
| **Correction** | User sửa bằng cách nào? Data đó đi vào đâu? | User chat lại: *"Pin vẫn còn 40% nhưng màn hình sập đen"* → AI nhận diện lại là lỗi phần mềm → Dữ liệu đẩy vào log để AI học cách phân biệt "sập màn hình" và "hết pin động cơ". |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** ☐ Precision · ☑ Recall
**Tại sao?** Triết lý là "Thà gọi cứu hộ dư còn hơn bỏ sót người cần cứu".
**Nếu sai ngược lại thì chuyện gì xảy ra?** Nếu ưu tiên Precision, bot quá khắt khe xác nhận lỗi, có thể bỏ qua một ca tai nạn nguy hiểm hoặc khiến khách hàng bị kẹt lại trên đường giữa đêm, gây phẫn nộ và khủng hoảng truyền thông.

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| **Completion Rate** (Tỉ lệ hoàn thành qua Bot) | ≥ 90% | < 70% (User bỏ cuộc, gọi số hotline quá nhiều) |
| **Completion Time** (Thời gian ra lệnh cứu hộ) | < 60 giây | > 120 giây (Phản tác dụng, thà gọi người còn nhanh hơn) |
| **Safety Violation Rate** (Hướng dẫn nguy hiểm) | 0% (Zero tolerance) | > 0% (Bất kỳ lúc nào Bot xúi user tự đụng vào pin cao áp) |
| **Escalation Rate** (Tỉ lệ chuyển tiếp KTV) | 10–30% | < 5% (Bot ép user) HOẶC > 50% (Bot vô dụng) |

---

## 4. Top 3 failure modes

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 | **Hướng dẫn nguy hiểm điện cao áp:** Sự cố liên quan đến pin lithium / điện 400-800V. | User có nguy cơ bị điện giật, tử vong do làm theo. (Nguy hiểm nhất vì user KHÔNG BIẾT mình gặp nguy). | Kích hoạt **Safety Blacklist**. Cấm tuyệt đối AI hướng dẫn chạm vào capo/cáp cam. Luôn phát cảnh báo: *"Tránh xa xe 5m và chờ cứu hộ."* |
| 2 | **Chẩn đoán sai loại sự cố:** User tả "xe đứng yên" nhưng không nói rõ hỏng máy hay xịt lốp. | Bot phân loại sai → Điều động nhầm loại xe cứu hộ (đem xe cẩu đi thay vì xe sửa lưu động) → Tốn tiền, user đợi lâu. | **Augmentation**: Luôn xác nhận lại với user loại xe cần gọi và cho phép kỹ thuật viên người thật review chéo các ca rủi ro cao. |
| 3 | **Tai nạn, user mất khả năng tương tác:** Xe lật, user bất tỉnh, bot cứ chờ chat lại. | Không ai được điều động đến, đe dọa tính mạng người dùng. | **Auto-detect crash:** Lấy dữ liệu cảm biến xe. Nếu có va chạm + user im lặng 30s → Tự động gọi SOS khẩn cấp (Chuyển sang Automation). |

---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | 200 sự cố/tháng. 40% dùng Bot; 60% xong việc qua Bot. | 500 sự cố/tháng. 70% dùng Bot; 85% xong việc qua Bot. | 1,000 sự cố/tháng. 90% dùng Bot; 95% xong việc. |
| **Cost** | ~$200/tháng (API + Infra cơ bản) | ~$600/tháng (API LLM + Monitoring) | ~$1,200/tháng (Hệ thống dự phòng cao) |
| **Benefit** | Giảm 48 cuộc gọi. Tiết kiệm ~24 giờ làm việc. | Giảm 297 cuộc gọi. Tiết kiệm ~150 giờ (tương đương 1 full-time CS). | Giảm 855 cuộc gọi. Tiết kiệm ~420 giờ làm việc. |
| **Net** | **Âm hoặc Hòa vốn.** | **Bắt đầu có lãi** (~$1,500 - $2,000/tháng). | **Lợi nhuận ròng** (~$3,000 - $4,000/tháng). |

**Kill criteria:** Dừng dự án nếu sau 3 tháng triển khai không đạt ngưỡng *Critical Mass* (500 ca/tháng) hoặc xuất hiện chỉ số Safety Violation Rate > 0%.

---

## 6. Mini AI spec (1 trang)

**Tầm nhìn Sản phẩm (Product Vision):**
VinFast Smart Rescue Orchestrator là hệ thống "Tổng đài viên Triage AI" dành riêng cho hệ sinh thái xe điện VinFast. Sản phẩm giải quyết nỗi đau chờ đợi tổng đài quá tải (mất 30-60 phút) khi xe gặp sự cố trên đường. Thông qua việc phân loại bằng ngôn ngữ tự nhiên và tự động lấy GPS/VIN xe, AI giúp rút ngắn thời gian phát lệnh cứu hộ xuống dưới 1 phút.

**Đối tượng và Phương thức hoạt động (Users & How it works):**
Sản phẩm phục vụ chủ xe điện VinFast và tối ưu hóa vận hành cho đội ngũ cứu hộ. Hệ thống chạy theo mô hình **Augmentation**. AI sẽ tiếp nhận input (text/voice), dự đoán mã lỗi, trích xuất vị trí, và đề xuất ETA của trạm bảo hành/xe cứu hộ gần nhất. Quyết định cuối cùng (nhấn nút chốt gọi cứu hộ) thuộc về con người. 

**Chỉ số Chất lượng & Rủi ro (Quality & Risks):**
Sản phẩm là một hệ thống liên quan mật thiết đến an toàn tính mạng, do đó tối ưu hóa cho mục tiêu **High Recall** (thà ghi nhận nhầm một ca cần cứu hộ còn hơn bỏ qua người đang gặp nạn). Rủi ro lớn nhất là AI xúi giục người dùng chạm vào hệ thống điện cao áp (được kiểm soát chặt bằng rule-based Safety Blacklist) và rủi ro điều phối sai loại xe cẩu do chẩn đoán nhầm bệnh.

**Lợi thế cạnh tranh (Data Flywheel):**
Mỗi lần AI chẩn đoán và bị kỹ thuật viên sửa lại (Technician correction signal), hệ thống sẽ học được đặc thù về mã lỗi độc quyền, hệ thống firmware liên tục cập nhật của VinFast. Lâu dài, hệ thống sẽ tạo ra một Knowledge Base "càng dùng càng thông minh" mà không một LLM chung nào trên thị trường có thể sao chép được, chuyển dịch trạng thái từ hỗ trợ thụ động (reactive) sang dự báo và túc trực cứu hộ chủ động (proactive).
