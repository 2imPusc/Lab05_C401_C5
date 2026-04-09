# Top 3 failure modes | Nhóm C5 - VinFast Rescue

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
