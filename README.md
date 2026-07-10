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

## 3. Cách chạy demo

```bash
cd src
pip install cryptography
python3 e2ee_demo.py
```

Kết quả in ra và được lưu vào `results/logs/sample_output.txt`, gồm 3 phần:

1. **Kịch bản TLS-only** — Cloud giải mã được và đọc trọn bản rõ.
2. **Kịch bản E2EE** — Cloud thử giải mã bằng khóa sai → thất bại
   (`InvalidTag`); chỉ App (giữ đúng khóa) giải mã thành công.
3. **Kiểm tra tampering** — sửa 1 byte ciphertext → App phát hiện và từ chối ngay (AES-GCM đảm bảo cả bí mật lẫn toàn vẹn).

## 4. Nguồn GitHub / tài liệu tham khảo

Xem chi tiết đầy đủ tại `references/link_nguon.md`. Tóm tắt 4 nguồn GitHub chính:

- OWASP ISVS — https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS
- Mbed TLS — https://github.com/Mbed-TLS/mbedtls
- Matter (connectedhomeip) — https://github.com/project-chip/connectedhomeip
- PyCA cryptography — https://github.com/pyca/cryptography

## 5. Tình trạng hoàn thành (checklist)

- [x] Tạo cấu trúc repo đúng chuẩn
- [x] Code demo chạy được, có log minh chứng
- [x] Sơ đồ so sánh TLS-only vs E2EE
- [x] Bảng ưu/nhược + khuyến nghị use case (`references/uu_nhuoc.md`)
- [ ] Báo cáo tiểu luận đầy đủ (đang soạn, xem `report/`)
- [ ] Slide trình bày (đang soạn, xem `slides/`)
- [ ] Ảnh chụp màn hình chạy thực tế trên máy cá nhân (bổ sung vào `results/screenshots/`)

## 6. Cam kết an toàn

Toàn bộ demo chạy cục bộ (local), dùng dữ liệu giả lập, không kết nối
hệ thống thật, không chứa secret/token/mật khẩu thật trong repo.
