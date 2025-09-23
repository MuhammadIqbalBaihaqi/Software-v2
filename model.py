import requests
from requests.exceptions import RequestException
import os
import csv
from datetime import datetime
from recv import ArduinoSensorReader

# --- Fungsi Utilitas dan Variabel Global ---
URL_HEALTH = "http://10.46.7.51:8000/api/connection/status"

def is_server_online(timeout=2):
    """Mengecek apakah server utama online."""
    try:
        print(f"--> [DEBUG] Mengirim request ke: {URL_HEALTH}")
        response = requests.get(URL_HEALTH, timeout=timeout)
        return response.status_code == 200
    except RequestException as e:
        print(f"!!! [DEBUG] GAGAL mengirim request: {e} !!!")
        return False
# -------------------------------------------

class TrashDataModel:
    listBerat = []
    def __init__(self):
        self.beratSementara = 0.0
        self.trash_data = {
            "flow": 0, "source": 0, "type": 0,
            "bag_count": 0, "weight": 0, "current_weight": 0
        }
        self.flow = {0: "Masuk", 1: "Keluar"}
        self.location_map = {
            0: "Mulai", 1: "KPFT", 2: "DTNTF", 3: "DTETI",
            4: "DTMI", 5: "DTK", 6: "DTAP", 7: "DTGD",
            8: "DTSL", 9: "DTGL", 10: "LTM"
        }
        self.type_map = {
            0: "Mulai", 1: "Sapuan", 2: "Anorganik Kering/Rosok",
            3: "Residu", 4: "Sisa Makanan"
        }
        
        self.url_kirim = "http://10.46.7.51:8000/api/sensor/data"
        
        self.arduino_reader = ArduinoSensorReader()
        self.arduino_reader.connect()

    def get_trash_data(self):
        return self.trash_data

    def set_flow(self, flow_code):
        self.trash_data["flow"] = flow_code

    def get_flow_name(self, code):
        return self.flow.get(code, "Unknown Flow")

    def set_source(self, source_code):
        self.trash_data["source"] = source_code

    def get_location_name(self, code):
        return self.location_map.get(code, "Unknown Location")

    def set_type(self, type_code):
        self.trash_data["type"] = type_code

    def get_type_name(self, code):
        return self.type_map.get(code, "Unknown Type")

    def measure_mass(self):
        val_A = self.arduino_reader.get_latest_weight()
        if abs((val_A / 1000)) < 0.05:
            val_A = 0.0
        return round((val_A / 1000), 3)

    def update_bag_data(self):
        current_weight = round(self.beratSementara, 1)
        self.listBerat.append(current_weight)
        self.trash_data["current_weight"] = current_weight
        self.trash_data["bag_count"] += 1
        self.trash_data["weight"] += current_weight
        return self.trash_data

    def reset_data(self):
        self.trash_data = { "flow": 0, "source": 0, "type": 0, "bag_count": 0, "weight": 0, "current_weight": 0 }
        self.listBerat.clear()
        return self.trash_data

    def undo_bag_data(self):
        if not self.listBerat:
            return self.reset_data()
        
        bobot_terakhir_yang_dihapus = self.listBerat.pop()
        self.trash_data["weight"] -= bobot_terakhir_yang_dihapus
        self.trash_data["bag_count"] -= 1
        self.trash_data["current_weight"] = self.listBerat[-1] if self.listBerat else 0
        return self.trash_data

    def _simpan_log_lokal_csv(self, data_transaksi, status):
        nama_file = 'riwayat_transaksi.csv'
        data_untuk_disimpan = data_transaksi.copy()
        data_untuk_disimpan['timestamp'] = datetime.now().isoformat()
        data_untuk_disimpan['status_pengiriman'] = status
        
        fieldnames = ['timestamp', 'flow', 'source', 'type', 'bag_count', 'weight', 'status_pengiriman']

        try:
            file_sudah_ada = os.path.exists(nama_file)
            with open(nama_file, mode='a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                if not file_sudah_ada:
                    writer.writeheader()
                writer.writerow(data_untuk_disimpan)
            print(f"--> [LOG] Transaksi dicatat ke {nama_file} dengan status '{status}'")
        except Exception as e:
            print(f"!!! [ERROR] Gagal mencatat log lokal: {e} !!!")

    def send_all_data(self):
        try:
            requests.post(self.url_kirim, json=self.trash_data, timeout=5)
            print("--> [ONLINE] Data berhasil dikirim ke server.")
            self._simpan_log_lokal_csv(self.trash_data, 'online')
        except RequestException as e:
            print(f"!!! [OFFLINE] Gagal mengirim data: {e}. Mencatat sebagai offline.")
            self._simpan_log_lokal_csv(self.trash_data, 'offline')

    # --- INI METODE YANG HILANG ---
    def sync_offline_data(self):
        """
        Membaca log CSV, mengirim semua data berstatus 'offline', 
        dan memperbarui statusnya menjadi 'synced' setelah berhasil.
        """
        nama_file = 'riwayat_transaksi.csv'
        if not os.path.exists(nama_file):
            return # Jika file tidak ada, tidak ada yang perlu disinkronkan

        print("--> [SYNC] Memulai pengecekan data offline...")
        
        semua_baris = []
        baris_untuk_dikirim = []

        # 1. Baca semua data dan pisahkan yang perlu dikirim
        with open(nama_file, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                semua_baris.append(row)
                if row.get('status_pengiriman') == 'offline':
                    baris_untuk_dikirim.append(row)

        if not baris_untuk_dikirim:
            print("--> [SYNC] Tidak ada data offline yang perlu dikirim.")
            return

        print(f"--> [SYNC] Ditemukan {len(baris_untuk_dikirim)} data untuk disinkronkan.")
        
        berhasil_disinkronkan = False
        # 2. Loop dan kirim data yang offline satu per satu
        for data_offline in baris_untuk_dikirim:
            try:
                # Siapkan payload JSON dengan tipe data yang benar
                payload = {
                    "flow": int(data_offline['flow']),
                    "source": int(data_offline['source']),
                    "type": int(data_offline['type']),
                    "bag_count": int(data_offline['bag_count']),
                    "weight": float(data_offline['weight']),
                    "timestamp_offline": data_offline['timestamp'] # Kirim timestamp asli
                }
                
                requests.post(self.url_kirim, json=payload, timeout=10)
                
                # Jika berhasil, update status di memori
                print(f"--> [SYNC] Berhasil mengirim data timestamp: {data_offline['timestamp']}")
                data_offline['status_pengiriman'] = 'synced'
                berhasil_disinkronkan = True

            except RequestException as e:
                print(f"!!! [SYNC] Koneksi terputus saat sinkronisasi. Berhenti sementara. Error: {e}")
                break # Hentikan loop jika koneksi gagal
            except (ValueError, KeyError) as e:
                print(f"!!! [SYNC] Error memproses baris (mungkin data korup): {data_offline}. Error: {e}")
                data_offline['status_pengiriman'] = 'sync_error' # Tandai sebagai error
                berhasil_disinkronkan = True

        # 3. Tulis ulang seluruh file CSV dengan status yang sudah diperbarui
        if berhasil_disinkronkan:
            print("--> [SYNC] Menulis ulang file log dengan status baru...")
            try:
                with open(nama_file, mode='w', newline='') as csvfile:
                    if semua_baris:
                        fieldnames = semua_baris[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(semua_baris)
                print("--> [SYNC] File log berhasil diperbarui.")
            except Exception as e:
                print(f"!!! [SYNC] Gagal menulis ulang file log: {e}")

    def tare(self):
        self.send_signal_tare()
        self.beratSementara = 0.0
        print("Tare operation completed.")

    def update_weight(self):
        self.beratSementara = self.measure_mass()
        return self.beratSementara

    def send_signal_tare(self):
        if self.arduino_reader.ser and self.arduino_reader.ser.is_open:
            try:
                self.arduino_reader.ser.write(b'T\n')
                print("Sinyal 'Tare' dikirim ke Arduino.")
            except Exception as e:
                print(f"Gagal mengirim sinyal 'Tare' ke Arduino: {e}")
        else:
            print("Arduino tidak terhubung, tidak bisa mengirim sinyal 'Tare'.")

