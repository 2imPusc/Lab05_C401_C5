# ROI Analysis | Dự án AI Cứu Hộ VinFast (Nhóm C5)

---

## 1. Bảng Ước Tính 3 Kịch Bản (ROI Scenarios)

|   | Conservative | Realistic  | Optimistic  |
|---|-------------|-----------|------------|
| **Assumption** | 200 sự cố/tháng. 40% dùng Bot; 60% xong việc qua Bot. | 500 sự cố/tháng. 70% dùng Bot; 85% xong việc qua Bot. | 1,000 sự cố/tháng (Cao điểm). 90% dùng Bot; 95% xong việc qua Bot. |
| **Cost** | ~$200/tháng (API + Infra cơ bản) | ~$600/tháng (API LLM + Monitoring) | ~$1,200/tháng (Hệ thống dự phòng cao) |
| **Benefit** | Giảm 48 cuộc gọi. Tiết kiệm ~24 giờ làm việc. | Giảm 297 cuộc gọi. Giải phóng ~150 giờ (tương đương 1 nhân sự full-time). | Giảm 855 cuộc gọi. Tiết kiệm ~420 giờ làm việc. |
| **Net** | **Âm hoặc Hòa vốn.** Chi phí vận hành AI > Chi phí nhân sự tiết kiệm được. | **Bắt đầu có lãi.** Tiết kiệm nhân sự khoảng $1,500 - $2,000. | **Hiệu quả cao.** Lợi nhuận ròng khoảng $3,000 - $4,000/tháng. |
---

## 2. Cost Breakdown

| Hạng mục | Cách tính | Realistic |
|----------|-----------|-----------|
| **API Inference** | $0.05/lượt chat × 5,000 lượt | $250/tháng |
| **Infrastructure** | Hosting (Azure/AWS), Database, GPS API | $200/tháng |
| **Nhân lực Maintain** | 10 giờ/tuần × $20/giờ | $800/tháng |
| **Data Correction** | Review lỗi phân loại (lốp vs máy) | $150/tháng |
| **Tổng cost/tháng** | | **~$1,400** |

---

## 3. Lợi Ích Phi Tài Chính 

| Benefit | Đo bằng gì | Tại sao quan trọng |
|---------|-----------|-------------------|
| **User Experience** | NPS, CSAT (Sự hài lòng) | Giảm hoảng loạn cho chủ xe khi gặp sự cố khẩn cấp. |
| **Data Flywheel** | Số lượng correction/ngày | Càng nhiều ca cứu hộ, AI càng phân loại chính xác mã lỗi xe VinFast. |
| **Brand Perception** | Media sentiment | Khẳng định vị thế xe điện thông minh, xử lý sự cố công nghệ cao. |

---

## 4. Time-to-Value 

* **Tuần 1-4 (Deployment):** Thu thập dữ liệu, user làm quen với giao diện chatbot trên App/Màn hình xe.
* **Tháng 2 (Optimization):** Hệ thống được cải thiện dựa trên dữ liệu thực tế. Tỷ lệ xử lý tự động tăng, giảm tải đáng kể cho tổng đài. User quen thao tác; bắt đầu thấy giảm tải rõ rệt cho tổng đài cứu hộ (>50% ca tự động).
* **Tháng 3+ (Scale):** Data flywheel hoạt động; AI dự báo được vùng có nhu cầu cứu hộ cao để điều xe lưu động chờ sẵn.

---

## 5. Lợi Thế Cạnh Tranh

 **Proprietary Data:**
  - Dữ liệu mã lỗi riêng của xe VinFast.
  - Dữ liệu GPS và hành vi người dùng khi gặp sự cố.
  - Dữ liệu hạ tầng trạm sạc và điều kiện vận hành thực tế.

 **Network Effect:**
  - Lượng người dùng tăng kéo theo lượng dữ liệu tăng.
  - Hệ thống ngày càng chính xác hơn trong việc phân loại lỗi và đề xuất hướng xử lý.
  - Có khả năng chuyển từ reactive sang proactive.

Lợi thế cạnh tranh này mang tính dài hạn và khó bị sao chép do phụ thuộc vào dữ liệu thực tế tích lũy theo thời gian.
---

## 6. Câu Hỏi Mở Rộng

* **Nếu API cost giảm 10x:** Kịch bản **Optimistic** sẽ cực kỳ bùng nổ, cho phép chatbot xử lý cả những yêu cầu tư vấn kỹ thuật thông thường thay vì chỉ cứu hộ khẩn cấp. Đồng thời cá nhân hóa trải nghiệm người dùng theo hành vi và lịch sử sử dụng xe
* **Critical Mass:** Cần tối thiểu 500 ca sự cố/tháng để AI có đủ dữ liệu học hỏi về các loại địa hình và tình trạng xe khác nhau.