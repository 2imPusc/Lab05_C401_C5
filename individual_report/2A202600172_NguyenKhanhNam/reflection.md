## Role
- Code, review code, explain code, and pitch idea to other groups

## Phụ trách cụ thể
- (Vibe)code logic agent chính và nhận mock JSON data các bạn khác để chỉnh sửa và áp dụng
- Review code

## SPEC phần nào mạnh nhất, phần nào yếu nhất? Vì sao?

### Mạnh nhất — Mục 3: Cơ chế AI (Augmentation) & Mục 4: Quality Metrics

Hai phần này được định nghĩa rõ ràng và có tư duy kỹ thuật tốt. Cơ chế Augmentation xác định đúng vai trò của AI (hỗ trợ, không thay thế con người) — phù hợp với bối cảnh cứu hộ có tính rủi ro cao.

Chiến lược Recall > Precision thể hiện sự hiểu biết thực tế về trade-off trong ML: trong tình huống khẩn cấp, false negative (bỏ sót yêu cầu cứu hộ) nguy hiểm hơn nhiều so với false positive. Việc đặt ngưỡng định vị < 50m cũng là một metric đo lường được, không chung chung.

### Yếu nhất — Mục 6: Data Flywheel

Phần này mô tả ý tưởng hấp dẫn nhưng thiếu tính khả thi cụ thể. SPEC không làm rõ:
- Feedback từ kỹ thuật viên được thu thập theo format nào?
- Ai gán nhãn correction signal?
- Chu kỳ re-training là bao lâu?
- Không có dữ liệu hiện tại (cold start problem) thì flywheel khởi động như thế nào?

Nếu không giải quyết được những câu hỏi này, Data Flywheel chỉ là lý thuyết, không phải lợi thế cạnh tranh thực sự.

## Đóng góp cụ thể khác
- Debug UI and agent
- Test UI features

## Điều học được trong hackathon mà trước đó chưa biết

Cách defend sản phẩm của mình và tiếp nhận ý kiến phản biện một cách có chọn lọc — phân biệt được ý kiến cần thay đổi và ý kiến cần giải thích lại.

## Nếu làm lại, đổi gì?

- Modular testing cho agent ReAct từ đầu: thay vì để đến cuối mới debug — mỗi tool/action của agent nên có unit test riêng để dễ isolate lỗi
- Thêm Quick Call button và User Feedback flow vào UI: ngay từ iteration đầu, vì đây là hai touch point quan trọng nhất với người dùng trong tình huống khẩn cấp

## AI giúp gì? AI sai/mislead ở đâu?
AI giúp: Scaffold nhanh phần codebase cho agent — đặc biệt là boilerplate cho ReAct loop, tool definitions và prompt templates, giúp tiết kiệm đáng kể thời gian setup ban đầu
AI mislead: Vibecoding khiến codebase khó đọc lại và khó maintain — code chạy được nhưng thiếu tính module hóa. Structure được generate ra không khớp với kiến trúc hệ thống nhóm đã thiết kế, dẫn đến phải refactor nhiều chỗ. Bài học: cần prompt rõ ràng hơn về context và constraints trước khi để AI generate code lớn
