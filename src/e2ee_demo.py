"""
De tai 43 - Ma hoa dau cuoi (End-to-End Encryption) trong he thong IoT
Sinh vien: Nguyen Thai Thanh Binh - MSSV 231A010880
Hoc phan: INT4410 - Bao mat IoT

Muc dich:
  Mo phong 2 kich ban truyen du lieu tu thiet bi IoT (device) qua may chu
  trung gian (cloud) den ung dung nguoi dung cuoi (app), de so sanh:

  Kich ban A - "TLS-only" (ma hoa duong truyen, khong phai E2EE):
      Device  --(TLS, cloud co the giai ma)-->  Cloud  --(TLS)-->  App
      => Cloud DOC DUOC noi dung ban ro cua du lieu cam bien.

  Kich ban B - "End-to-End Encryption":
      Device --(payload da ma hoa bang khoa chi Device+App biet)--> Cloud
      Cloud chi luu/chuyen tiep ciphertext, KHONG co khoa giai ma.
      Cloud --(chuyen tiep nguyen ciphertext)--> App --(giai ma)--> ban ro
      => Cloud KHONG the doc duoc noi dung ban ro.

Thuat toan dung: AES-256-GCM (thu vien 'cryptography', khong tu viet
thuat toan mat ma - dung khuyen nghi cua OWASP ISVS va Mbed TLS).

Chay: python3 e2ee_demo.py
"""

import json
import os
import base64
from datetime import datetime, timezone

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


LOG_LINES = []


def log(line=""):
    print(line)
    LOG_LINES.append(line)


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


# ---------------------------------------------------------------------------
# Du lieu cam bien giao lap (vi du: nhip tim + vi tri phong benh nhan)
# ---------------------------------------------------------------------------
def make_sensor_payload(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "heart_rate_bpm": 78,
        "room": "Phong 302",
        "patient_note": "Chi so on dinh",
    }


# ---------------------------------------------------------------------------
# KICH BAN A: TLS-only -> Cloud giai ma va doc duoc ban ro
# ---------------------------------------------------------------------------
def scenario_tls_only():
    log("=" * 70)
    log("KICH BAN A: Ma hoa duong truyen (TLS-only), KHONG phai E2EE")
    log("=" * 70)

    payload = make_sensor_payload("device-ward302-01")
    plaintext_json = json.dumps(payload, ensure_ascii=False)

    # Trong TLS-only, du lieu duoc "giai ma tai cloud" truoc khi xu ly/luu.
    # O day ta mo phong: cloud nhan duoc goi tin va TRUC TIEP doc duoc JSON.
    log("[Device] Gui du lieu qua ket noi TLS toi Cloud.")
    log(f"[Device] Du lieu goc (plaintext): {plaintext_json}")

    log("\n[Cloud] TLS handshake thanh cong, cloud giai ma tang van chuyen.")
    log("[Cloud] *** Cloud DOC DUOC toan bo noi dung ban ro sau day: ***")
    log(f"[Cloud]   -> {plaintext_json}")
    log("[Cloud] => Neu cloud bi xam nhap / nhan vien noi bo lam sai quy")
    log("           trinh, du lieu nhay cam (nhip tim, phong benh, ghi chu)")
    log("           co the bi doc, sua hoac ro ri ngay tai lop trung gian.")

    log("\n[Cloud] Chuyen tiep du lieu (co the o dang khac) toi App.")
    log("[App]   Nhan va hien thi du lieu binh thuong.")
    log(f"[App]   -> {plaintext_json}")
    return payload


# ---------------------------------------------------------------------------
# KICH BAN B: End-to-End Encryption -> Cloud chi thay ciphertext
# ---------------------------------------------------------------------------
def scenario_e2ee():
    log("\n" + "=" * 70)
    log("KICH BAN B: Ma hoa dau cuoi (End-to-End Encryption - E2EE)")
    log("=" * 70)

    # Khoa bi mat nay CHI Device va App biet. Cloud khong duoc cap khoa nay.
    # Trong thuc te, khoa nay duoc thiet lap qua qua trinh provisioning an
    # toan hoac trao doi khoa (xem De tai 40), khong hard-code nhu demo.
    e2ee_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(e2ee_key)

    payload = make_sensor_payload("device-ward302-01")
    plaintext_json = json.dumps(payload, ensure_ascii=False)
    plaintext_bytes = plaintext_json.encode("utf-8")

    # --- DEVICE: ma hoa payload truoc khi roi khoi thiet bi ---
    nonce = os.urandom(12)  # nonce 96-bit, moi lan ma hoa phai khac nhau
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, associated_data=None)

    envelope = {
        "device_id": payload["device_id"],
        "alg": "AES-256-GCM",
        "nonce_b64": b64(nonce),
        "ciphertext_b64": b64(ciphertext),
    }
    envelope_json = json.dumps(envelope, ensure_ascii=False)

    log("[Device] Ma hoa payload bang khoa E2EE (chi Device + App co).")
    log(f"[Device] Goi tin gui di (ciphertext, KHONG phai ban ro):")
    log(f"[Device]   -> {envelope_json}")

    # --- CLOUD: chi luu / chuyen tiep, KHONG co khoa giai ma ---
    log("\n[Cloud] Nhan goi tin, LUU va CHUYEN TIEP nguyen trang.")
    log("[Cloud] Cloud KHONG co khoa E2EE nen thu doc thu:")
    try:
        # Cloud khong co 'e2ee_key' that (mo phong bang khoa sai)
        fake_key = AESGCM.generate_key(bit_length=256)
        AESGCM(fake_key).decrypt(nonce, ciphertext, associated_data=None)
        log("[Cloud]   -> (khong nen xay ra) giai ma thanh cong")
    except Exception as e:
        log(f"[Cloud]   -> That bai khi giai ma: {type(e).__name__}")
        log("[Cloud]   => Cloud CHI THAY chuoi ciphertext vo nghia, khong")
        log("              biet nhip tim, phong benh hay ghi chu benh nhan.")

    # --- APP: nhan tu cloud, tu giai ma bang khoa dung (chia se rieng voi device) ---
    received_nonce = base64.b64decode(envelope["nonce_b64"])
    received_ciphertext = base64.b64decode(envelope["ciphertext_b64"])
    decrypted_bytes = aesgcm.decrypt(
        received_nonce, received_ciphertext, associated_data=None
    )
    decrypted_json = decrypted_bytes.decode("utf-8")

    log("\n[App]   Nhan ciphertext tu Cloud, dung khoa E2EE de giai ma.")
    log(f"[App]   -> Giai ma thanh cong: {decrypted_json}")

    assert decrypted_json == plaintext_json, "Loi: du lieu giai ma khong khop!"
    log("[App]   => Du lieu giai ma khop 100% voi du lieu goc tu Device.")
    return payload


# ---------------------------------------------------------------------------
# Kiem tra toan ven: neu Cloud (ke tan cong) sua ciphertext -> App phai phat hien
# ---------------------------------------------------------------------------
def scenario_tampering_detected():
    log("\n" + "=" * 70)
    log("KIEM TRA BO SUNG: AES-GCM phat hien du lieu bi sua doi (tampering)")
    log("=" * 70)

    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    payload = make_sensor_payload("device-ward302-01")
    plaintext_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, associated_data=None)

    # Gia lap ke tan cong/cloud doc hai sua 1 byte trong ciphertext
    tampered = bytearray(ciphertext)
    tampered[0] ^= 0xFF
    tampered = bytes(tampered)

    log("[Attacker/Cloud] Thu sua 1 byte trong ciphertext truoc khi den App.")
    try:
        aesgcm.decrypt(nonce, tampered, associated_data=None)
        log("[App] (khong nen xay ra) giai ma thanh cong voi du lieu bi sua")
    except Exception as e:
        log(f"[App] Tu choi du lieu: xac thuc GCM that bai ({type(e).__name__})")
        log("[App] => AES-GCM cung cap ca bi mat (confidentiality) lan toan")
        log("         ven/xac thuc (integrity/authenticity) chi trong 1 buoc.")


def main():
    scenario_tls_only()
    scenario_e2ee()
    scenario_tampering_detected()

    log("\n" + "=" * 70)
    log("KET LUAN NHANH")
    log("=" * 70)
    log("- TLS-only: bao ve du lieu TREN DUONG TRUYEN, nhung cloud/trung")
    log("  gian van doc duoc ban ro sau khi giai ma tang van chuyen.")
    log("- E2EE: chi Device va App (2 dau cuoi) giu khoa; Cloud chi thay")
    log("  ciphertext, phu hop du lieu nhay cam (y te, camera rieng tu,")
    log("  khoa cua) nhung danh doi la kho quan ly khoa/khoi phuc/debug hon.")

    out_dir = os.path.join(os.path.dirname(__file__), "..", "results", "logs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "sample_output.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG_LINES))
    print(f"\n[Log da luu tai] {os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
