# Đề tài 43 — Mã hóa đầu cuối trong hệ thống IoT (End-to-End Encryption)

**Học phần:** INT4410 — Bảo mật trong IoT 
**Sinh viên:** Nguyễn Thái Thanh Bình — MSSV 231A010880
**GVHD:** Hồ Nhựt Minh
**Hình thức:** Cá nhân

## 1. Mô tả đề tài

Đề tài phân tích và minh họa **mã hóa đầu cuối (End-to-End Encryption –
E2EE)** trong hệ thống IoT: so sánh với mã hóa đường truyền thông
thường (TLS device → cloud), chứng minh bằng code rằng với E2EE, lớp
trung gian (cloud) không thể đọc được nội dung dữ liệu thật, và đề
xuất khi nào nên áp dụng E2EE trong thực tế (y tế, camera riêng tư,
khóa cửa...).

## 2. Cấu trúc repo 

```
NguyenThaiThanhBinh-MaHoaDauCuoi/
├── README.md
├── report/
│   └── (đặt Bao_cao_tieu_luan.docx/.pdf tại đây)
├── slides/
│   └── (đặt Slide_trinh_bay.pptx/.pdf tại đây)
├── src/
│   └── e2ee_demo.py            # code demo TLS-only vs E2EE
├── configs/
│   └── manifest.json           # tham số thuật toán/endpoint (không chứa secret thật)
├── data/
│   └── payload_mau.json        # dữ liệu cảm biến giả lập
├── results/
│   ├── tls_vs_e2ee.svg         # sơ đồ so sánh
│   ├── screenshots/            # (bổ sung ảnh chụp màn hình khi có)
│   └── logs/
│       └── sample_output.txt   # log chạy demo
└── references/
    └── link_nguon.md           # danh sách tài liệu tham khảo
```


## 3. Nguồn GitHub / tài liệu tham khảo

Xem chi tiết đầy đủ tại `references/link_nguon.md`. Tóm tắt 4 nguồn GitHub chính:

- OWASP ISVS — https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS
- Mbed TLS — https://github.com/Mbed-TLS/mbedtls
- Matter (connectedhomeip) — https://github.com/project-chip/connectedhomeip
- PyCA cryptography — https://github.com/pyca/cryptography

## 4. Tình trạng hoàn thành (checklist)

-  Tạo cấu trúc repo đúng chuẩn


