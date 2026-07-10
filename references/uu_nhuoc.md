# Bảng ưu/nhược: TLS-only vs End-to-End Encryption (E2EE) trong IoT

## 1. Bảng so sánh

| Tiêu chí | TLS-only (device → cloud → app) | End-to-End Encryption (E2EE) |
|---|---|---|
| Ai đọc được dữ liệu tại Cloud | Đọc được (bản rõ sau khi giải mã tầng vận chuyển) | Không đọc được (chỉ thấy ciphertext) |
| Bảo vệ trên đường truyền | Có (chống nghe lén mạng) | Có (chống nghe lén mạng) |
| Bảo vệ khi Cloud bị xâm nhập | Không — dữ liệu vẫn lộ | Có — kẻ tấn công chỉ lấy được ciphertext |
| Rủi ro nội bộ (nhân viên Cloud) | Cao — có thể xem trực tiếp dữ liệu | Thấp — không có khóa để xem |
| Khả năng Cloud xử lý/tìm kiếm dữ liệu (analytics, search) | Dễ dàng | Khó, cần kỹ thuật đặc biệt (searchable encryption, xử lý phía client) |
| Quản lý khóa | Đơn giản hơn (TLS cert theo chuẩn PKI có sẵn) | Phức tạp hơn — cần cấp, lưu, xoay vòng khóa E2EE riêng giữa device–app |
| Khôi phục tài khoản / thiết bị mất khóa | Dễ (cloud có thể hỗ trợ) | Khó — mất khóa có thể mất luôn khả năng đọc dữ liệu cũ |
| Gỡ lỗi (debugging) phía server | Dễ | Khó vì server không thấy nội dung thật |
| Hiệu năng thiết bị (CPU/pin) | Thấp hơn (chỉ 1 lớp mã hóa TLS) | Cao hơn một chút (thêm 1 lớp mã hóa ứng dụng) |
| Phù hợp dữ liệu | Dữ liệu thông thường, ít nhạy cảm | Dữ liệu rất nhạy cảm: y tế, camera riêng tư, khóa cửa, tin nhắn cá nhân |

## 2. Khuyến nghị theo use case

| Use case | Khuyến nghị | Lý do |
|---|---|---|
| Cảm biến nhiệt độ/độ ẩm nhà kính, nông nghiệp | TLS-only là đủ | Dữ liệu không nhạy cảm, cần cloud xử lý/thống kê dễ dàng |
| Thiết bị theo dõi sức khỏe, máy đo tại giường bệnh | **E2EE bắt buộc cân nhắc** | Dữ liệu y tế là dữ liệu cá nhân nhạy cảm, rủi ro pháp lý và đạo đức cao nếu lộ |
| Camera an ninh gia đình | **E2EE nên dùng** | Hình ảnh riêng tư trong nhà; nhiều nhà cung cấp lớn (ví dụ hệ sinh thái theo hướng Matter) đã hướng tới E2EE cho luồng video |
| Khóa cửa thông minh, lệnh mở/đóng | **E2EE nên dùng** cho lệnh điều khiển | Lệnh điều khiển bị lộ hoặc bị sửa có thể gây hậu quả vật lý trực tiếp |
| Dashboard giám sát nhà máy cần cloud phân tích real-time | TLS-only + kiểm soát truy cập chặt tại cloud | E2EE gây khó khăn cho việc cloud xử lý/tổng hợp dữ liệu real-time |

## 3. Kết luận

E2EE không thay thế hoàn toàn TLS — hai lớp này bổ sung cho nhau:
TLS bảo vệ đường truyền, E2EE bảo vệ nội dung ngay cả khi lớp trung
gian (cloud) bị xâm nhập hoặc bị lạm dụng. Với hệ thống IoT xử lý dữ
liệu nhạy cảm (y tế, hình ảnh riêng tư, lệnh điều khiển vật lý), nên
ưu tiên thiết kế E2EE ngay từ đầu, chấp nhận đánh đổi về độ phức tạp
quản lý khóa và khả năng xử lý dữ liệu phía cloud.
