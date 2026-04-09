# Mini AI Spec: VinFast Smart Rescue Orchestrator
**Dự án: Hệ thống Điều phối Cứu hộ Thông minh | Nhóm C5**

---

## 1. Product Vision
Sản phẩm là một hệ thống hỗ trợ cứu hộ tích hợp AI dành riêng cho hệ sinh thái xe điện VinFast. Mục tiêu cốt lõi là cắt giảm thời gian chờ đợi từ 30–60 phút xuống còn dưới 60 giây bằng cách tự động hóa khâu tiếp nhận và phân loại sự cố. Thay vì phải gọi tổng đài và mô tả thủ công, người dùng có thể tương tác nhanh qua Chatbot để được điều phối cứu hộ chính xác.

## 2. Target Users
* **Chủ xe VinFast:** Đặc biệt là người lái các dòng xe điện (VF e34, VF 5, VF 8, VF 9...) gặp sự cố kỹ thuật, hết pin hoặc tai nạn trên đường.
* **Đội ngũ vận hành (Ops):** Tổng đài viên và kỹ thuật viên cứu hộ cần dữ liệu chính xác về vị trí và loại lỗi để điều động phương tiện phù hợp.

## 3. Cơ chế AI: Augmentation 
Hệ thống được thiết kế theo mô hình **Augmentation**, trong đó AI đóng vai trò là trợ lý đắc lực giúp tăng tốc độ xử lý thông tin, nhưng con người (người dùng và kỹ thuật viên) vẫn là bên đưa ra quyết định cuối cùng.
* **Nhận diện & Phân loại:** AI sử dụng LLM để hiểu ngôn ngữ tự nhiên, từ đó phân loại sự cố vào các nhóm: hỏng máy, thủng lốp, hết pin, hay tai nạn.
* **Tự động hóa dữ liệu:** Tự động trích xuất tọa độ GPS từ thiết bị và thông tin định danh xe (VIN/Biển số) để loại bỏ sai sót do nhập liệu thủ công.
* **Điều phối thông minh:** Gợi ý trạm bảo hành hoặc xe cứu hộ gần nhất dựa trên khoảng cách và thời gian chờ dự kiến (ETA).

## 4. Quality Metrics
* **Chiến lược Recall > Precision:** Trong tình huống cứu hộ, hệ thống ưu tiên không bỏ sót bất kỳ yêu cầu hỗ trợ nào (High Recall). Thà ghi nhận dư một ca cần cứu hộ còn hơn để khách hàng rơi vào tình trạng nguy hiểm do AI không nhận diện được yêu cầu.
* **Độ chính xác vị trí:** Sai số định vị phải duy trì ở mức < 50m để đảm bảo xe cứu hộ tìm thấy mục tiêu nhanh nhất.
* **Tính minh bạch:** AI luôn hiển thị mức độ confidence % và các bước reasoning để người dùng hiểu tại sao phương án đó được đưa ra.

## 5. Main Risks
* **Hallucination :** LLM có thể gợi ý các dịch vụ cứu hộ không tồn tại hoặc sai thông tin kỹ thuật.
* **Mất kết nối:** Rủi ro khi người dùng ở khu vực mất sóng hoặc GPS không chính xác.
* **Mô tả mơ hồ:** Người dùng có thể mô tả không rõ ràng (ví dụ: "xe không chạy được") dẫn đến việc AI điều động sai loại xe cứu hộ (xe kéo thay vì xe sửa lưu động).

## 6. Data Flywheel
Dự án tạo ra lợi thế cạnh tranh bền vững thông qua cơ chế tự học:
1.  **Thu thập:** Ghi lại mọi tương tác giữa người dùng và Chatbot.
2.  **Feedback Loop:** Kết quả xử lý thực tế từ kỹ thuật viên tại hiện trường sẽ được dùng để đối chiếu với chẩn đoán ban đầu của AI.
3.  **Cải thiện:** Correction signals giúp AI ngày càng hiểu sâu về các mã lỗi đặc thù của xe VinFast, giúp hệ thống càng dùng càng chính xác và khó bị sao chép bởi các đối thủ khác.