import serial
import time
import json
import re
import hmac
import hashlib
import requests

# ================== KONFIG ==================
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE   = 9600
READ_TIMEOUT_S = 1

SERVER = 'http://10.254.39.237:5000/ingest'  # ganti IP/host (tanpa < >)
SECRET = b'SAMPAH'                      # samakan dgn server

POST_TIMEOUT_S = 5
VERIFY_TLS = False        # True jika HTTPS dengan cert valid / verify="cert.pem"

SEND_INTERVAL_S = 2       # interval kirim rata-rata (detik)

# ================== UTIL ==================
def sign(body: bytes) -> str:
    return hmac.new(SECRET, body, hashlib.sha256).hexdigest()

def parse_weight(line: str):
    """Dukung 2 format:
       1) JSON: {"weight": 12.34}
       2) Teks: "Weight : 12.34" -> ambil angka pertama
       return float atau None kalau tidak ada angka.
    """
    # coba JSON
    try:
        obj = json.loads(line)
        if isinstance(obj, dict) and 'weight' in obj:
            return float(obj['weight'])
    except Exception:
        pass

    # regex angka pertama
    m = re.search(r'[-+]?\d*\.?\d+', line)
    if m:
        try:
            return float(m.group())
        except ValueError:
            return None
    return None

def post_weight_avg(session: requests.Session, avg_weight: float, count: int):
    payload = {'weight': avg_weight}
    body = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'X-Signature' : sign(body),
    }
    r = session.post(SERVER, data=body, headers=headers,
                     timeout=POST_TIMEOUT_S, verify=VERIFY_TLS)
    print(f"[HTTP] avg({count})={avg_weight:.3f} -> {r.status_code} {r.text}")

# ================== MAIN ==================
def open_serial_with_retry():
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=READ_TIMEOUT_S)
            print(f"[SERIAL] Terhubung ke {SERIAL_PORT} @ {BAUD_RATE}")
            return ser
        except Exception as e:
            print(f"[SERIAL] Gagal buka {SERIAL_PORT}: {e}. Retry 2s...")
            time.sleep(2)

def main():
    ser = open_serial_with_retry()
    session = requests.Session()

    bucket = []                   # tampung nilai selama interval
    last_window_ts = time.time()  # awal window

    while True:
        try:
            raw = ser.readline()
            if not raw:
                # cek window walau tak ada data masuk
                pass
            else:
                line = raw.decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"[SERIAL] {line}")
                    w = parse_weight(line)
                    if w is not None:
                        bucket.append(w)

            now = time.time()
            if now - last_window_ts >= SEND_INTERVAL_S:
                if bucket:
                    avg = sum(bucket) / len(bucket)
                    try:
                        post_weight_avg(session, avg, len(bucket))
                    except Exception as http_err:
                        print("[HTTP ERROR]", http_err)
                    bucket.clear()
                else:
                    print("[INFO] Tidak ada sampel pada window ini.")
                last_window_ts = now

        except serial.SerialException as e:
            print("[SERIAL TERPUTUS]", e)
            try:
                ser.close()
            except Exception:
                pass
            time.sleep(2)
            ser = open_serial_with_retry()
        except KeyboardInterrupt:
            print("\n[EXIT] Dihentikan pengguna.")
            break
        except Exception as e:
            print("[ERROR]", e)

if __name__ == '__main__':
    main()
