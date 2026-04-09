# Individual reflection — Đỗ Minh Phúc (2A202600039)

## 1. Role: Leader nhóm

- Phụ trách kiểm tra và đánh giá các nội dung SPEC
- Phát triển system prompt, code flow agent

## 2. Đóng góp cụ thể

- Thiết kế conversation flow:
  1. Người dùng nhập mô tả sự cố.
  2. Hệ thống phản hồi hướng dẫn xử lý và hỏi thêm thông tin nếu còn thiếu.
  3. Vòng lặp tiếp tục cho đến khi:
  - Người dùng xác nhận đã xử lý xong, hoặc
  - Người dùng báo không thể tự sửa / hệ thống nhận diện lỗi vượt khả năng tự xử lý.
  4. Hệ thống gợi ý các phương án cứu hộ phù hợp (kèm ETA, mức giá dự kiến).
  5. Người dùng xác nhận phương án và thông tin liên hệ.
  6. Hệ thống gửi thông tin kết nối hai chiều giữa người dùng và đội cứu hộ để liên lạc trực tiếp.

- Thiết kế slide
- Thêm phần gợi ý phần hồi, chat với AI trong thao tác của người dùng

## 3. SPEC mạnh/yếu

- Mạnh nhất: Nhóm xác định được các tình huống nguy hiểm thật sự như hướng dẫn sai liên quan điện cao áp, mất kết nối, hoặc AI không chắc chắn, và đều có phương án fallback rõ ràng
- Yếu nhất:
  - Chưa xử lý đến các vấn đề về pháp lý như người sửa theo hướng dẫn bị hỏng
  - Vấn đề về quyền riêng tư với GPS

## 4. Đóng góp khác

- Xử lý repo github cho team

## 5. Điều học được

- Với sự cố xe trên đường, ưu tiên recall cao để tránh bỏ sót ca cần cứu hộ. Nhưng vẫn phải có guardrail để không gây false alarm quá mức, làm tăng chi phí vận hành.
- Cần phân chia block thời gian để nhóm hoạt động riêng kết hợp với trao đổi chung để dabate với nhau và phát huy điểm mạnh của team hơn
  - bạn Hiếu: tốt về tìm kiếm thông tin
  - anh Nguyễn Nam: về mặt kỹ thuật, xử lý code
  - anh Lê Nam: có nhiều kinh nghiệm về thực hiện sản phẩm
  - anh Lê Hưng: hòa đồng, tích cực tham gia trong hoạt động nhóm
  - anh Chu Quân: tốt trong phản biện và đánh giá

## 6. Nếu làm lại

Nếu làm lại, em nghĩ sẽ cùng nhóm dành nhiều thời gian trao đổi sâu hơn trong quá trình phát hiện và nghiên cứu sâu vào đề tài để khai thác thêm tiềm năng cũng như nhìn nhận thêm các vấn đề thực tế của giải pháp. Nhóm đã thực hiện bắt tay vào build sớm rồi phát sinh thêm các ý tưởng trong quá trình build demo và bị "loãng thông tin" với mục tiêu. Đồng thời thiết kế các phase để quản lý nhóm hoạt động kết hợp giữa độc lập và nhóm để

## 7. AI giúp gì / AI sai gì

- **Giúp:** AI hỗ trợ brainstorm failure modes và gợi ý nhiều edge cases nhanh, giúp nhóm mở rộng góc nhìn khi thiết kế trust and safety. Đặc biệt là vấn đề về gợi ý pháp lý, các vấn đề gợi ý người dùng thực hiện thao tác nguy hiểm
- **Sai/mislead:** AI thực hiện code không hiểu đúng ý, luồng flow. Mở rộng bài toán sớm nhưng không đào sâu
- **Bài học**:Dùng AI tốt nhất ở vai trò đồng tư duy, còn quyết định cuối cùng vẫn phải bám mục tiêu sản phẩm
