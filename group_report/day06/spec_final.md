# SPEC — AI Product Hackathon

**Nhóm:** C5 (Phúc, Khánh Nam, Hưng, Tú Nam, Hiếu, Quân)
**Track:** ☑ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool · ☐ XanhSM · ☐ Open
**Problem statement (1 câu):** Khi xe VinFast gặp sự cố khẩn cấp (hết pin, lỗi kỹ thuật), người dùng phải mất 30-60 phút gọi tổng đài và chờ xử lý thủ công; AI Assistant sẽ tự động chẩn đoán lỗi tức thời và điều phối cứu hộ, giúp rút ngắn thời gian tiếp nhận xuống dưới 60 giây.

---

## 1. AI Product Canvas

|                   | Value                                                                                                                                                                                                                                                                                                                                                 | Trust                                                                                                                                                                                                                                                                                                                                                                  | Feasibility                                                                                                                                                                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Câu hỏi guide** | User nào?<br />Pain gì?<br /> AI giải quyết gì mà cách hiện tại không giải được?                                                                                                                                                                                                                                                                      | Khi AI sai thì user bị ảnh hưởng thế nào?<br />User biết AI sai bằng cách nào? <br />User sửa bằng cách nào?                                                                                                                                                                                                                                                           | Cost bao nhiêu/request?<br />Latency bao lâu? <br />Risk chính là gì?                                                                                                                                                                                                                 |
| **Trả lời**       | **User:** Chủ xe điện VinFast (Người đang cần hỗ trợ).<br />**Pain:** Chờ đợi cứu hộ lâu, mất 30-60 phút tra cứu mã lỗi hoặc chờ tổng đài xử lý thủ công khi xe gặp sự cố.<br />**AI giải quyết:** Chẩn đoán lỗi tức thời bằng ngôn ngữ tự nhiên<br />hướng dẫn tự xử lý (nếu lỗi nhẹ) hoặc nối máy cứu hộ ngay lập tức, tiết kiệm thời gian chờ đợi. | **AI sai:** Sai chẩn đoán (VD: lỗi phần mềm lại báo thay lốp) gây lãng phí thời gian<br />hoặc sai mức độ nghiêm trọng gây mất an toàn.<br />**Nhận biết:** AI hiển thị Confidence % và Reasoning từng bước.<br />Ưu tiên **Recall > Precision** (chấp nhận báo động dư còn hơn bỏ sót).<br />**Cách sửa:** Luôn có nút [Gọi kỹ thuật viên] để user thoát vòng lặp AI. | **Cost:** ~$0.05 - $0.1/phiên hội thoại (API LLM).<br />**Latency:** < 3 giây/phản hồi.<br />**Risk chính:** AI hallucinate bịa ra tên/số điện thoại cứu hộ không có thật; <br />User gặp sự cố ở vùng mất sóng 4G/5G; <br />Dịch vụ cứu hộ thực tế không làm theo thỏa thuận của AI. |

---

## Automation hay augmentation?

☐ Automation — AI làm thay, user không can thiệp
☑ Augmentation — AI gợi ý, user quyết định cuối cùng

**Justify:** Sự cố xe hơi liên quan trực tiếp đến an toàn tính mạng, tài sản và sự hoảng loạn của người dùng. AI chỉ nên đóng vai trò là "Tổng đài viên Triage" (phân loại bệnh) và gợi ý hướng giải quyết. Quyết định cuối cùng (chạm vào dây điện, reset hệ thống, hoặc chốt điều xe kéo cứu hộ) BẮT BUỘC phải do con người (User hoặc Kỹ thuật viên thật) xác nhận để đảm bảo pháp lý và an toàn.

---

## Learning signal

| #   | Câu hỏi                                          | Trả lời                                                                                                                                                                                                                                |
| --- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | User correction đi vào đâu?                      | _Lịch sử chat và quyết định thực tế cuối cùng (do kỹ thuật viên hoặc user chốt) được ghi thành `correction log` → Dùng để cập nhật Knowledge Base (RAG) hoặc fine-tune model._                                                         |
| 2   | Product thu signal gì để biết tốt lên hay tệ đi? | _Implicit: Tỷ lệ session kết thúc thành công mà không cần escalate (chuyển tiếp) lên kỹ thuật viên người thật.<br />Explicit: Rating 1-5 sao sau phiên hỗ trợ.<br />Correction: Mã lỗi thực tế thợ ghi nhận khác với mã AI chẩn đoán._ |
| 3   | Data thuộc loại nào?                             | _☑ Domain-specific (Lỗi đặc thù hệ thống xe VinFast) · ☑ Human-judgment (Thợ kỹ thuật chốt lỗi cuối cùng)_                                                                                                                             |

**Có marginal value không?** Cực kỳ cao. Các LLM chung (như GPT-4, Claude) không nắm được hệ thống mã lỗi nội bộ, phần mềm nội bộ cập nhật liên tục của VinFast. Việc thu thập Data từ các ca cứu hộ thực tế sẽ tạo ra một Knowledge Base độc quyền, tạo rào cản cạnh tranh lớn.

---

## 2. User Stories — 4 paths

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

---

## 3. Eval metrics + threshold

## Precision hay recall?

[ ] Precision — khi Chatbot nói "có" thì thực sự đúng (ít false positive)

[x] **Recall — tìm được hết những cái cần tìm (ít false negative)**

**Tại sao?** Vì triết lý vận hành của hệ thống là "thà gọi cứu hộ dư còn hơn bỏ sót người cần cứu". Trong các tình huống xe hết pin hoặc gặp sự cố kỹ thuật trên đường, việc không nhận diện được một yêu cầu khẩn cấp (false negative) có thể gây nguy hiểm trực tiếp cho người dùng.

**Nếu sai ngược lại thì sao?** Nếu ưu tiên Precision, chatbot có thể quá khắt khe trong việc xác nhận sự cố, dẫn đến việc người dùng bị kẹt lại mà không có sự trợ giúp, gây ra sự bất tiện, lo lắng và làm giảm trải nghiệm dịch vụ của VinFast.

---

## Metrics table

| Metric                                                | Threshold                                       | Red flag (dừng khi)                                                                                                                                            |
| ----------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tỉ lệ hoàn thành (Completion Rate)**                | ≥ 90% người dùng hoàn thành yêu cầu qua bot     | < 70% (Người dùng kết thúc chatbot trước khi gọi được cứu hộ)                                                                                                  |
| **Thời gian xử lý (Completion Time)**                 | < 60 giây từ khi bắt đầu chat đến khi phát lệnh | > 120 giây (Thời gian chờ vượt quá ngưỡng kiên nhẫn)                                                                                                           |
| **Độ chính xác phân loại (Classification Accuracy)**  | $\geq$ 90%                                      | $\leq$ 70% (Phân loại sai sự cố của phương tiện người dùng dẫn đến gọi sai dịch vụ cứu hộ)                                                                     |
| **Độ trễ phản hồi chấp nhận (Target Latency)**        | < 5 giây cho mỗi phản hồi                       | > 10 giây (Gây cảm giác hệ thống bị treo và tốn quá tổng thời gian so với việc người dùng tự tìm kiếm thủ công)                                                |
| **Độ chính xác vị trí (GPS Accuracy)**                | Sai số < 50m                                    | > 200m (Cứu hộ không thể tìm thấy xe dựa trên tọa độ)                                                                                                          |
| **Tỉ lệ hướng dẫn nguy hiểm (Safety Violation Rate)** | 0% — Zero tolerance                             | > 0% (Bất kỳ lần nào Chatbot đưa ra hướng dẫn liên quan hệ thống điện cao áp, pin lithium mà không có cảnh báo an toàn → dừng hệ thống ngay lập tức để review) |
| **Tỉ lệ chuyển tiếp (Escalation Rate)**               | 10–30% sessions cần chuyển lên kỹ thuật viên    | < 5% (Bot có thể đang "ép" user ở lại thay vì escalate) HOẶC > 50% (Bot không đủ năng lực xử lý, cần cải thiện model)                                          |
| **Mức độ hài lòng (CSAT)**                            | ≥ 4.0/5.0 sau mỗi phiên hỗ trợ                  | < 3.0/5.0 (Trải nghiệm kém, user sẽ quay lại gọi tổng đài thủ công)                                                                                            |

---

## Mở rộng (optional — bonus)

### User-facing metrics vs internal metrics

| Metric                          | User thấy? | Dùng để làm gì                                                                                                              |
| ------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Reasoning từng bước**         | [x] Có     | Giúp người dùng hiểu Chatbot đang xử lý gì để tăng sự tin tưởng.                                                            |
| **Nút [ Gọi kỹ thuật viên ]**   | [x] Có     | Lối thoát khẩn cấp nếu người dùng thấy Chatbot không xử lý được vấn đề.                                                     |
| **ETA (Thời gian chờ dự kiến)** | [x] Có     | Giảm hoảng loạn bằng cách thông báo thời gian cứu hộ đến.                                                                   |
| **CSAT (1-5 sao)**              | [x] Có     | Thu thập đánh giá cuối phiên để đo chất lượng trải nghiệm thực tế từ góc nhìn người dùng.                                   |
| **Safety Violation alert**      | [ ] Không  | Metric nội bộ — đếm số lần Chatbot suýt/đã đưa hướng dẫn nguy hiểm. User không cần thấy, nhưng team phải monitor real-time. |
| **Escalation Rate**             | [ ] Không  | Metric nội bộ — theo dõi tỉ lệ chuyển tiếp để cân bằng giữa "bot quá yếu" và "bot ép user ở lại".                           |

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

## 4. Top 3 failure modes

Liệt kê cách sản phẩm có thể thất bại — không phải danh sách tính năng.

> **"Failure mode nào người dùng KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."**

---

## Template

| #   | Trigger                                                                                                                                                                                                                                 | Hậu quả                                                                                                                                                      | Mitigation                                                                                                                                                                                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Chẩn đoán sai loại sự cố:** Người dùng mô tả không rõ ràng (ví dụ: "xe không chạy được" nhưng không rõ do phần mềm hay phần cứng).                                                                                                    | **Chatbot** phân loại sai dẫn đến điều động sai loại xe cứu hộ (ví dụ: điều động xe kéo thay vì xe sửa chữa lưu động).                                       | **Augmentation:** **Chatbot** chỉ đóng vai trò gợi ý; người dùng và kỹ thuật viên là bên đưa ra quyết định cuối cùng.                                                                                                                                                                                   |
| 2   | **Lỗi định vị hoặc mất kết nối:** Người dùng ở khu vực mất sóng hoặc GPS không chính xác.                                                                                                                                               | Cứu hộ không thể tìm thấy vị trí xe, làm tăng thời gian chờ đợi (ETA) và gây hoảng loạn cho người dùng.                                                      | Tự động lấy tọa độ GPS từ thiết bị kết hợp với thông tin định danh xe (VIN/Biển số) để xác thực.                                                                                                                                                                                                        |
| 3   | **Ảo giác thông tin (Hallucination):** **Chatbot **tự sáng tạo ra tên dịch vụ cứu hộ không tồn tại hoặc thông báo sai giá thỏa thuận.                                                                                                   | Người dùng tin vào thông tin sai lệch, dẫn đến việc dịch vụ không được thực hiện hoặc xảy ra tranh chấp về chi phí.                                          | Hiển thị mức độ tin tưởng (confidence %), minh bạch hóa các bước suy luận (reasoning) và luôn cung cấp nút `[ Gọi kỹ thuật viên ]`.                                                                                                                                                                     |
| 4   | **Tai nạn nghiêm trọng — User mất khả năng tương tác:** Xe va chạm mạnh hoặc lật, người lái bị thương không thể cầm điện thoại hoặc nhập liệu vào Chatbot.                                                                              | Chatbot chờ input mãi mà không có phản hồi. Không ai được điều động đến hiện trường. Tính mạng người dùng bị đe dọa trực tiếp.                               | **Auto-detect crash** thông qua dữ liệu accelerometer từ xe hoặc điện thoại. Khi phát hiện va chạm bất thường + user không phản hồi trong 30 giây → Tự động gửi tọa độ GPS và gọi cứu hộ khẩn cấp (SOS) mà không cần user xác nhận. Đây là trường hợp duy nhất chuyển từ **Augmentation → Automation**. |
| 5   | **Hướng dẫn nguy hiểm liên quan điện cao áp:** Xe điện VinFast sử dụng hệ thống pin lithium điện áp cao (400-800V). Chatbot có thể hướng dẫn user "mở nắp capo kiểm tra" hoặc "tự kiểm tra dây cáp" trong khi hệ thống đang rò rỉ điện. | User bị điện giật, bỏng hoặc tử vong do tiếp xúc với hệ thống điện cao áp.**Đây là failure mode nguy hiểm nhất vì user KHÔNG BIẾT mình đang gặp nguy hiểm.** | Xây dựng**Safety Blacklist**: danh sách các hướng dẫn Chatbot TUYỆT ĐỐI KHÔNG được đưa ra (mở nắp khoang pin, chạm vào dây cáp màu cam, tự thay/reset pin cao áp). Khi sự cố liên quan hệ thống điện/pin → Chatbot chỉ được phép nói: "Hãy rời xa xe ít nhất 5 mét và chờ kỹ thuật viên chuyên môn."    |
| 6   | **Quá tải hệ thống khi thiên tai/sự cố hàng loạt:** Mưa bão, ngập lụt hoặc sự cố hạ tầng sạc khiến hàng trăm xe cùng gặp vấn đề trong thời gian ngắn.                                                                                   | API LLM bị rate-limit hoặc timeout. Hàng đợi cứu hộ tràn. Người dùng không nhận được phản hồi, mất niềm tin hoàn toàn vào hệ thống.                          | **Graceful degradation**: Khi tải vượt ngưỡng → Chatbot tự động chuyển sang chế độ rút gọn (chỉ hỏi 2 câu: "Loại sự cố?" + "Vị trí?") thay vì multi-turn conversation. Ưu tiên xử lý theo mức độ nghiêm trọng (tai nạn > hết pin > lỗi nhẹ). Hiển thị thứ tự hàng đợi cho user.                         |

---

## Mở rộng (optional — bonus)

### Severity × likelihood matrix

- **FIX NGAY (Top Priority):**
  - **Hướng dẫn nguy hiểm điện cao áp (#5).** Severity: Chí mạng. Likelihood: Trung bình. Lý do: User KHÔNG BIẾT mình đang gặp nguy hiểm → failure mode "im lặng" nguy hiểm nhất.
  - **Chẩn đoán sai loại sự cố (#1).** Severity: Cao. Likelihood: Cao (ngôn ngữ tự nhiên rất đa dạng).
- **Monitor + plan:**
  - **Tai nạn nghiêm trọng — mất khả năng tương tác (#4).** Severity: Chí mạng. Likelihood: Thấp. Cần auto-detect crash mechanism.
  - **Lỗi định vị hoặc mất sóng (#2).** Severity: Cao. Likelihood: Thấp ở đô thị, cao ở vùng sâu/đèo núi.
- **Fix khi có thời gian:**
  - **Quá tải hệ thống (#6).** Severity: Trung bình. Likelihood: Thấp (chỉ khi thiên tai/sự cố hàng loạt).
  - Độ trễ phản hồi của **Chatbot** vượt quá 5 giây.

### Cascade failure (Chuỗi thất bại liên hoàn)

Khi một thất bại ban đầu kéo theo một loạt các hậu quả khác:

1. **Chatbot** nhận diện sai lỗi xe.
2. Hệ thống điều động xe kéo đến hiện trường thay vì xe sửa chữa.
3. Kỹ thuật viên không có thiết bị phù hợp để xử lý tại chỗ.
4. Người dùng phải đặt lại yêu cầu và chờ đợi thêm 30-60 phút.
5. **Kết quả:** Chi phí vận hành tăng gấp đôi và lòng tin vào dịch vụ VinFast bị sụp đổ.

### Adversarial / misuse scenarios

| Scenario                       | Hậu quả                                                                              | Phòng tránh                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Người dùng spam yêu cầu cứu hộ | Làm tăng chi phí vận hành API (~ ¢1-2/lượt) và làm nghẽn hệ thống.                   | Thiết lập giới hạn số lượng yêu cầu (rate limiting) dựa trên số VIN hoặc tài khoản người dùng.   |
| Phản hồi sai từ thực tế        | **Chatbot** học từ các dữ liệu hiệu chỉnh sai, làm giảm độ chính xác theo thời gian. | Xây dựng vòng lặp phản hồi (Feedback loop) với sự giám sát chặt chẽ từ kỹ thuật viên chuyên môn. |

### Câu hỏi mở rộng

- **Failure mode ở quy mô lớn:**
  - Khi hệ thống chịu tải cao, thời gian xử lý có thể tăng lên, khiến người dùng từ bỏ **Chatbot** để quay lại gọi tổng đài thủ công.
  - Khi nguồn dữ liệu vị trí thay đổi (vd. Sau sát nhập tỉnh, thông tin địa lý hành chính thay đổi)
- **Automation và Augmentation:** Việc ưu tiên mô hình Augmentation (có sự can thiệp của con người) sẽ giúp giảm thiểu các thất bại ngầm mà **Chatbot** có thể gây ra trong quá trình tự động hóa hoàn toàn.

## 5. ROI 3 kịch bản

## 5.1. Bảng Ước Tính 3 Kịch Bản (ROI Scenarios)

|                | Conservative                                                               | Realistic                                                                 | Optimistic                                                         |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ | --- |
| **Assumption** | 200 sự cố/tháng. 40% dùng Bot; 60% xong việc qua Bot.                      | 500 sự cố/tháng. 70% dùng Bot; 85% xong việc qua Bot.                     | 1,000 sự cố/tháng (Cao điểm). 90% dùng Bot; 95% xong việc qua Bot. |
| **Cost**       | ~$200/tháng (API + Infra cơ bản)                                           | ~$600/tháng (API LLM + Monitoring)                                        | ~$1,200/tháng (Hệ thống dự phòng cao)                              |     |
| **Benefit**    | Giảm 48 cuộc gọi. Tiết kiệm ~24 giờ làm việc.                              | Giảm 297 cuộc gọi. Giải phóng ~150 giờ (tương đương 1 nhân sự full-time). | Giảm 855 cuộc gọi. Tiết kiệm ~420 giờ làm việc.                    |
| **Net**        | **Âm hoặc Hòa vốn.** Chi phí vận hành AI > Chi phí nhân sự tiết kiệm được. | **Bắt đầu có lãi.** Tiết kiệm nhân sự khoảng $1,500 - $2,000.             | **Hiệu quả cao.** Lợi nhuận ròng khoảng $3,000 - $4,000/tháng.     |

---

## 5.2. Cost Breakdown

| Hạng mục              | Cách tính                              | Realistic   |
| --------------------- | -------------------------------------- | ----------- | --- |
| **API Inference**     | $0.05/lượt chat × 5,000 lượt           | $250/tháng  |     |
| **Infrastructure**    | Hosting (Azure/AWS), Database, GPS API | $200/tháng  |
| **Nhân lực Maintain** | 10 giờ/tuần × $20/giờ                  | $800/tháng  |     |
| **Data Correction**   | Review lỗi phân loại (lốp vs máy)      | $150/tháng  |
| **Tổng cost/tháng**   |                                        | **~$1,400** |

---

## 5.3. Lợi Ích Phi Tài Chính

| Benefit              | Đo bằng gì               | Tại sao quan trọng                                                   |
| -------------------- | ------------------------ | -------------------------------------------------------------------- |
| **User Experience**  | NPS, CSAT (Sự hài lòng)  | Giảm hoảng loạn cho chủ xe khi gặp sự cố khẩn cấp.                   |
| **Data Flywheel**    | Số lượng correction/ngày | Càng nhiều ca cứu hộ, AI càng phân loại chính xác mã lỗi xe VinFast. |
| **Brand Perception** | Media sentiment          | Khẳng định vị thế xe điện thông minh, xử lý sự cố công nghệ cao.     |

---

## 5.4. Time-to-Value

- **Tuần 1-4 (Deployment):** Thu thập dữ liệu, user làm quen với giao diện chatbot trên App/Màn hình xe.
- **Tháng 2 (Optimization):** Hệ thống được cải thiện dựa trên dữ liệu thực tế. Tỷ lệ xử lý tự động tăng, giảm tải đáng kể cho tổng đài. User quen thao tác; bắt đầu thấy giảm tải rõ rệt cho tổng đài cứu hộ (>50% ca tự động).
- **Tháng 3+ (Scale):** Data flywheel hoạt động; AI dự báo được vùng có nhu cầu cứu hộ cao để điều xe lưu động chờ sẵn.

---

## 5.5. Lợi Thế Cạnh Tranh

**Proprietary Data:**

- Dữ liệu mã lỗi riêng của xe VinFast.
- Dữ liệu GPS và hành vi người dùng khi gặp sự cố.
- Dữ liệu hạ tầng trạm sạc và điều kiện vận hành thực tế.

**Network Effect:**

- Lượng người dùng tăng kéo theo lượng dữ liệu tăng.
- Hệ thống ngày càng chính xác hơn trong việc phân loại lỗi và đề xuất hướng xử lý.
- Có khả năng chuyển từ reactive sang proactive.

## Lợi thế cạnh tranh này mang tính dài hạn và khó bị sao chép do phụ thuộc vào dữ liệu thực tế tích lũy theo thời gian.

## 5.6. Câu Hỏi Mở Rộng

- **Nếu API cost giảm 10x:** Kịch bản **Optimistic** sẽ cực kỳ bùng nổ, cho phép chatbot xử lý cả những yêu cầu tư vấn kỹ thuật thông thường thay vì chỉ cứu hộ khẩn cấp. Đồng thời cá nhân hóa trải nghiệm người dùng theo hành vi và lịch sử sử dụng xe
- **Critical Mass:** Cần tối thiểu 500 ca sự cố/tháng để AI có đủ dữ liệu học hỏi về các loại địa hình và tình trạng xe khác nhau.

## 6. Mini AI spec (1 trang)

## 6.1. Product Vision

Sản phẩm là một hệ thống hỗ trợ cứu hộ tích hợp AI dành riêng cho hệ sinh thái xe điện VinFast. Mục tiêu cốt lõi là cắt giảm thời gian chờ đợi từ 30–60 phút xuống còn dưới 60 giây bằng cách tự động hóa khâu tiếp nhận và phân loại sự cố. Thay vì phải gọi tổng đài và mô tả thủ công, người dùng có thể tương tác nhanh qua Chatbot để được điều phối cứu hộ chính xác.

## 6.2. Target Users

- **Chủ xe VinFast:** Đặc biệt là người lái các dòng xe điện (VF e34, VF 5, VF 8, VF 9...) gặp sự cố kỹ thuật, hết pin hoặc tai nạn trên đường.
- **Đội ngũ vận hành (Ops):** Tổng đài viên và kỹ thuật viên cứu hộ cần dữ liệu chính xác về vị trí và loại lỗi để điều động phương tiện phù hợp.

## 6.3. Cơ chế AI: Augmentation

Hệ thống được thiết kế theo mô hình **Augmentation**, trong đó AI đóng vai trò là trợ lý đắc lực giúp tăng tốc độ xử lý thông tin, nhưng con người (người dùng và kỹ thuật viên) vẫn là bên đưa ra quyết định cuối cùng.

- **Nhận diện & Phân loại:** AI sử dụng LLM để hiểu ngôn ngữ tự nhiên, từ đó phân loại sự cố vào các nhóm: hỏng máy, thủng lốp, hết pin, hay tai nạn.
- **Tự động hóa dữ liệu:** Tự động trích xuất tọa độ GPS từ thiết bị và thông tin định danh xe (VIN/Biển số) để loại bỏ sai sót do nhập liệu thủ công.
- **Điều phối thông minh:** Gợi ý trạm bảo hành hoặc xe cứu hộ gần nhất dựa trên khoảng cách và thời gian chờ dự kiến (ETA).

## 6.4. Quality Metrics

- **Chiến lược Recall > Precision:** Trong tình huống cứu hộ, hệ thống ưu tiên không bỏ sót bất kỳ yêu cầu hỗ trợ nào (High Recall). Thà ghi nhận dư một ca cần cứu hộ còn hơn để khách hàng rơi vào tình trạng nguy hiểm do AI không nhận diện được yêu cầu.
- **Độ chính xác vị trí:** Sai số định vị phải duy trì ở mức < 50m để đảm bảo xe cứu hộ tìm thấy mục tiêu nhanh nhất.
- **Tính minh bạch:** AI hiển thị các bước reasoning để người dùng hiểu tại sao phương án đó được đưa ra.

## 6.5. Main Risks

- **Hallucination :** LLM có thể gợi ý các dịch vụ cứu hộ không tồn tại hoặc sai thông tin kỹ thuật.
- **Mất kết nối:** Rủi ro khi người dùng ở khu vực mất sóng hoặc GPS không chính xác.
- **Mô tả mơ hồ:** Người dùng có thể mô tả không rõ ràng (ví dụ: "xe không chạy được") dẫn đến việc AI điều động sai loại xe cứu hộ (xe kéo thay vì xe sửa lưu động).

## 6.6. Data Flywheel

Dự án tạo ra lợi thế cạnh tranh bền vững thông qua cơ chế tự học:

1. **Thu thập:** Ghi lại mọi tương tác giữa người dùng và Chatbot.
2. **Feedback Loop:** Kết quả xử lý thực tế từ kỹ thuật viên tại hiện trường sẽ được dùng để đối chiếu với chẩn đoán ban đầu của AI.
3. **Cải thiện:** Correction signals giúp AI ngày càng hiểu sâu về các mã lỗi đặc thù của xe VinFast, giúp hệ thống càng dùng càng chính xác và khó bị sao chép bởi các đối thủ khác.

Ngoài ra, các dữ liệu về hỏng hóc, sửa chữa có thể được khai thác cho việc phát triển sản phẩm xe điện trong việc phát hiện các điểm yếu, vấn đề của sản phẩm khi đến tay người dùng
