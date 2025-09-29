# # import requests
# # from requests.exceptions import RequestException
# # import os
# # import csv
# # from datetime import datetime
# # from recv import ArduinoSensorReader

# # # --- Fungsi Utilitas dan Variabel Global ---
# # URL_HEALTH = "http://10.46.7.51:8000/api/connection/status"

# # def is_server_online(timeout=2):
# #     """Mengecek apakah server utama online."""
# #     try:
# #         print(f"--> [DEBUG] Mengirim request ke: {URL_HEALTH}")
# #         response = requests.get(URL_HEALTH, timeout=timeout)
# #         return response.status_code == 200
# #     except RequestException as e:
# #         print(f"!!! [DEBUG] GAGAL mengirim request: {e} !!!")
# #         return False
# # # -------------------------------------------

# # class TrashDataModel:
# #     listBerat = []
# #     def __init__(self):
# #         self.beratSementara = 0.0
# #         self.trash_data = {
# #             "flow": 0, "source": 0, "type": 0,
# #             "bag_count": 0, "weight": 0, "current_weight": 0
# #         }
# #         self.flow = {0: "Masuk", 1: "Keluar"}
# #         self.location_map = {
# #             0: "Mulai", 1: "KPFT", 2: "DTNTF", 3: "DTETI",
# #             4: "DTMI", 5: "DTK", 6: "DTAP", 7: "DTGD",
# #             8: "DTSL", 9: "DTGL", 10: "LTM"
# #         }
# #         self.type_map = {
# #             0: "Mulai", 1: "Sapuan", 2: "Anorganik Kering/Rosok",
# #             3: "Residu", 4: "Sisa Makanan"
# #         }
        
# #         self.url_kirim = "http://10.46.7.51:8000/api/sensor/data"
        
# #         self.arduino_reader = ArduinoSensorReader()
# #         self.arduino_reader.connect()

# #     def get_trash_data(self):
# #         return self.trash_data

# #     def set_flow(self, flow_code):
# #         self.trash_data["flow"] = flow_code

# #     def get_flow_name(self, code):
# #         return self.flow.get(code, "Unknown Flow")

# #     def set_source(self, source_code):
# #         self.trash_data["source"] = source_code

# #     def get_location_name(self, code):
# #         return self.location_map.get(code, "Unknown Location")

# #     def set_type(self, type_code):
# #         self.trash_data["type"] = type_code

# #     def get_type_name(self, code):
# #         return self.type_map.get(code, "Unknown Type")

# #     def measure_mass(self):
# #         val_A = self.arduino_reader.get_latest_weight()
# #         if abs((val_A / 1000)) < 0.05:
# #             val_A = 0.0
# #         return round((val_A / 1000), 3)

# #     def update_bag_data(self):
# #         current_weight = round(self.beratSementara, 1)
# #         self.listBerat.append(current_weight)
# #         self.trash_data["current_weight"] = current_weight
# #         self.trash_data["bag_count"] += 1
# #         self.trash_data["weight"] += current_weight
# #         return self.trash_data

# #     def reset_data(self):
# #         self.trash_data = { "flow": 0, "source": 0, "type": 0, "bag_count": 0, "weight": 0, "current_weight": 0 }
# #         self.listBerat.clear()
# #         return self.trash_data

# #     def undo_bag_data(self):
# #         if not self.listBerat:
# #             return self.reset_data()
        
# #         bobot_terakhir_yang_dihapus = self.listBerat.pop()
# #         self.trash_data["weight"] -= bobot_terakhir_yang_dihapus
# #         self.trash_data["bag_count"] -= 1
# #         self.trash_data["current_weight"] = self.listBerat[-1] if self.listBerat else 0
# #         return self.trash_data

# #     def _simpan_log_lokal_csv(self, data_transaksi, status):
# #         nama_file = 'riwayat_transaksi.csv'
# #         data_untuk_disimpan = data_transaksi.copy()
# #         data_untuk_disimpan['timestamp'] = datetime.now().isoformat()
# #         data_untuk_disimpan['status_pengiriman'] = status
        
# #         fieldnames = ['timestamp', 'flow', 'source', 'type', 'bag_count', 'weight', 'status_pengiriman']

# #         try:
# #             file_sudah_ada = os.path.exists(nama_file)
# #             with open(nama_file, mode='a', newline='') as csvfile:
# #                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
# #                 if not file_sudah_ada:
# #                     writer.writeheader()
# #                 writer.writerow(data_untuk_disimpan)
# #             print(f"--> [LOG] Transaksi dicatat ke {nama_file} dengan status '{status}'")
# #         except Exception as e:
# #             print(f"!!! [ERROR] Gagal mencatat log lokal: {e} !!!")

# #     def send_all_data(self):
# #         try:
# #             requests.post(self.url_kirim, json=self.trash_data, timeout=5)
# #             print("--> [ONLINE] Data berhasil dikirim ke server.")
# #             self._simpan_log_lokal_csv(self.trash_data, 'online')
# #         except RequestException as e:
# #             print(f"!!! [OFFLINE] Gagal mengirim data: {e}. Mencatat sebagai offline.")
# #             self._simpan_log_lokal_csv(self.trash_data, 'offline')

# #     # --- INI METODE YANG HILANG ---
# #     def sync_offline_data(self):
# #         """
# #         Membaca log CSV, mengirim semua data berstatus 'offline', 
# #         dan memperbarui statusnya menjadi 'synced' setelah berhasil.
# #         """
# #         nama_file = 'riwayat_transaksi.csv'
# #         if not os.path.exists(nama_file):
# #             return # Jika file tidak ada, tidak ada yang perlu disinkronkan

# #         print("--> [SYNC] Memulai pengecekan data offline...")
        
# #         semua_baris = []
# #         baris_untuk_dikirim = []

# #         # 1. Baca semua data dan pisahkan yang perlu dikirim
# #         with open(nama_file, mode='r', newline='') as csvfile:
# #             reader = csv.DictReader(csvfile)
# #             for row in reader:
# #                 semua_baris.append(row)
# #                 if row.get('status_pengiriman') == 'offline':
# #                     baris_untuk_dikirim.append(row)

# #         if not baris_untuk_dikirim:
# #             print("--> [SYNC] Tidak ada data offline yang perlu dikirim.")
# #             return

# #         print(f"--> [SYNC] Ditemukan {len(baris_untuk_dikirim)} data untuk disinkronkan.")
        
# #         berhasil_disinkronkan = False
# #         # 2. Loop dan kirim data yang offline satu per satu
# #         for data_offline in baris_untuk_dikirim:
# #             try:
# #                 # Siapkan payload JSON dengan tipe data yang benar
# #                 payload = {
# #                     "flow": int(data_offline['flow']),
# #                     "source": int(data_offline['source']),
# #                     "type": int(data_offline['type']),
# #                     "bag_count": int(data_offline['bag_count']),
# #                     "weight": float(data_offline['weight']),
# #                     "timestamp_offline": data_offline['timestamp'] # Kirim timestamp asli
# #                 }
                
# #                 requests.post(self.url_kirim, json=payload, timeout=10)
                
# #                 # Jika berhasil, update status di memori
# #                 print(f"--> [SYNC] Berhasil mengirim data timestamp: {data_offline['timestamp']}")
# #                 data_offline['status_pengiriman'] = 'synced'
# #                 berhasil_disinkronkan = True

# #             except RequestException as e:
# #                 print(f"!!! [SYNC] Koneksi terputus saat sinkronisasi. Berhenti sementara. Error: {e}")
# #                 break # Hentikan loop jika koneksi gagal
# #             except (ValueError, KeyError) as e:
# #                 print(f"!!! [SYNC] Error memproses baris (mungkin data korup): {data_offline}. Error: {e}")
# #                 data_offline['status_pengiriman'] = 'sync_error' # Tandai sebagai error
# #                 berhasil_disinkronkan = True

# #         # 3. Tulis ulang seluruh file CSV dengan status yang sudah diperbarui
# #         if berhasil_disinkronkan:
# #             print("--> [SYNC] Menulis ulang file log dengan status baru...")
# #             try:
# #                 with open(nama_file, mode='w', newline='') as csvfile:
# #                     if semua_baris:
# #                         fieldnames = semua_baris[0].keys()
# #                         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #                         writer.writeheader()
# #                         writer.writerows(semua_baris)
# #                 print("--> [SYNC] File log berhasil diperbarui.")
# #             except Exception as e:
# #                 print(f"!!! [SYNC] Gagal menulis ulang file log: {e}")

# #     def tare(self):
# #         self.send_signal_tare()
# #         self.beratSementara = 0.0
# #         print("Tare operation completed.")

# #     def update_weight(self):
# #         self.beratSementara = self.measure_mass()
# #         return self.beratSementara

# #     def send_signal_tare(self):
# #         if self.arduino_reader.ser and self.arduino_reader.ser.is_open:
# #             try:
# #                 self.arduino_reader.ser.write(b'T\n')
# #                 print("Sinyal 'Tare' dikirim ke Arduino.")
# #             except Exception as e:
# #                 print(f"Gagal mengirim sinyal 'Tare' ke Arduino: {e}")
# #         else:
# #             print("Arduino tidak terhubung, tidak bisa mengirim sinyal 'Tare'.")


# import requests
# from requests.exceptions import RequestException
# import os
# import csv
# from datetime import datetime
# from recv import ArduinoSensorReader
# import subprocess
# import shutil
# import time

# # --- Fungsi Utilitas dan Variabel Global ---
# URL_HEALTH = "http://10.46.7.51:8000/api/connection/status"

# def is_server_online(timeout=2):
#     """Mengecek apakah server utama online."""
#     try:
#         response = requests.get(URL_HEALTH, timeout=timeout)
#         return response.status_code == 200
#     except RequestException:
#         return False
# # -------------------------------------------

# class TrashDataModel:
#     # ... (semua metode yang sudah ada dari __init__ sampai send_signal_tare tetap sama) ...
#     listBerat = []
#     def __init__(self):
#         self.beratSementara = 0.0
#         self.trash_data = {
#             "flow": 0, "source": 0, "type": 0,
#             "bag_count": 0, "weight": 0, "current_weight": 0
#         }
#         self.flow = {0: "Masuk", 1: "Keluar"}
#         self.location_map = {
#             0: "Mulai", 1: "KPFT", 2: "DTNTF", 3: "DTETI",
#             4: "DTMI", 5: "DTK", 6: "DTAP", 7: "DTGD",
#             8: "DTSL", 9: "DTGL", 10: "LTM"
#         }
#         self.type_map = {
#             0: "Mulai", 1: "Sapuan", 2: "Anorganik Kering/Rosok",
#             3: "Residu", 4: "Sisa Makanan"
#         }
        
#         self.url_kirim = "http://10.46.7.51:8000/api/sensor/data"
        
#         self.arduino_reader = ArduinoSensorReader()
#         self.arduino_reader.connect()

#     def get_trash_data(self):
#         return self.trash_data

#     def set_flow(self, flow_code):
#         self.trash_data["flow"] = flow_code

#     def get_flow_name(self, code):
#         return self.flow.get(code, "Unknown Flow")

#     def set_source(self, source_code):
#         self.trash_data["source"] = source_code

#     def get_location_name(self, code):
#         return self.location_map.get(code, "Unknown Location")

#     def set_type(self, type_code):
#         self.trash_data["type"] = type_code

#     def get_type_name(self, code):
#         return self.type_map.get(code, "Unknown Type")

#     def measure_mass(self):
#         val_A = self.arduino_reader.get_latest_weight()
#         if abs((val_A / 1000)) < 0.05:
#             val_A = 0.0
#         return round((val_A / 1000), 3)

#     def update_bag_data(self):
#         current_weight = round(self.beratSementara, 1)
#         self.listBerat.append(current_weight)
#         self.trash_data["current_weight"] = current_weight
#         self.trash_data["bag_count"] += 1
#         self.trash_data["weight"] += current_weight
#         return self.trash_data

#     def reset_data(self):
#         self.trash_data = { "flow": 0, "source": 0, "type": 0, "bag_count": 0, "weight": 0, "current_weight": 0 }
#         self.listBerat.clear()
#         return self.trash_data

#     def undo_bag_data(self):
#         if not self.listBerat:
#             return self.reset_data()
        
#         bobot_terakhir_yang_dihapus = self.listBerat.pop()
#         self.trash_data["weight"] -= bobot_terakhir_yang_dihapus
#         self.trash_data["bag_count"] -= 1
#         self.trash_data["current_weight"] = self.listBerat[-1] if self.listBerat else 0
#         return self.trash_data

#     def _simpan_log_lokal_csv(self, data_transaksi, status):
#         nama_file = 'riwayat_transaksi.csv'
#         data_untuk_disimpan = data_transaksi.copy()
#         data_untuk_disimpan['timestamp'] = datetime.now().isoformat()
#         data_untuk_disimpan['status_pengiriman'] = status
        
#         fieldnames = ['timestamp', 'flow', 'source', 'type', 'bag_count', 'weight', 'status_pengiriman']

#         try:
#             file_sudah_ada = os.path.exists(nama_file)
#             with open(nama_file, mode='a', newline='') as csvfile:
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
#                 if not file_sudah_ada:
#                     writer.writeheader()
#                 writer.writerow(data_untuk_disimpan)
#             print(f"--> [LOG] Transaksi dicatat ke {nama_file} dengan status '{status}'")
#         except Exception as e:
#             print(f"!!! [ERROR] Gagal mencatat log lokal: {e} !!!")

#     def send_all_data(self):
#         try:
#             requests.post(self.url_kirim, json=self.trash_data, timeout=5)
#             print("--> [ONLINE] Data berhasil dikirim ke server.")
#             self._simpan_log_lokal_csv(self.trash_data, 'online')
#         except RequestException as e:
#             print(f"!!! [OFFLINE] Gagal mengirim data: {e}. Mencatat sebagai offline.")
#             self._simpan_log_lokal_csv(self.trash_data, 'offline')

#     def sync_offline_data(self):
#         nama_file = 'riwayat_transaksi.csv'
#         if not os.path.exists(nama_file):
#             return
        
#         semua_baris = []
#         baris_untuk_dikirim = []

#         with open(nama_file, mode='r', newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 semua_baris.append(row)
#                 if row.get('status_pengiriman') == 'offline':
#                     baris_untuk_dikirim.append(row)

#         if not baris_untuk_dikirim:
#             return

#         berhasil_disinkronkan = False
#         for data_offline in baris_untuk_dikirim:
#             try:
#                 payload = {
#                     "flow": int(data_offline['flow']),
#                     "source": int(data_offline['source']),
#                     "type": int(data_offline['type']),
#                     "bag_count": int(data_offline['bag_count']),
#                     "weight": float(data_offline['weight']),
#                     "timestamp_offline": data_offline['timestamp']
#                 }
#                 requests.post(self.url_kirim, json=payload, timeout=10)
#                 data_offline['status_pengiriman'] = 'synced'
#                 berhasil_disinkronkan = True
#             except RequestException:
#                 break
#             except (ValueError, KeyError):
#                 data_offline['status_pengiriman'] = 'sync_error'
#                 berhasil_disinkronkan = True

#         if berhasil_disinkronkan:
#             try:
#                 with open(nama_file, mode='w', newline='') as csvfile:
#                     if semua_baris:
#                         fieldnames = semua_baris[0].keys()
#                         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                         writer.writeheader()
#                         writer.writerows(semua_baris)
#             except Exception:
#                 pass

#     def tare(self):
#         self.send_signal_tare()
#         self.beratSementara = 0.0

#     def update_weight(self):
#         self.beratSementara = self.measure_mass()
#         return self.beratSementara

#     def send_signal_tare(self):
#         if self.arduino_reader.ser and self.arduino_reader.ser.is_open:
#             try:
#                 self.arduino_reader.ser.write(b'T\n')
#             except Exception:
#                 pass
    
#     # --- FITUR BARU DIMULAI DARI SINI ---
#     # def export_csv_to_usb(self, mount_path='/mnt/usb_flash_drive'):
#     #     """
#     #     Mencoba mount, menyalin file riwayat, dan unmount flash drive.
#     #     Mengembalikan tuple (boolean_sukses, pesan_status).
#     #     """
#     #     sumber_file = 'riwayat_transaksi.csv'
        
#     #     # 1. Cek apakah file sumber ada
#     #     if not os.path.exists(sumber_file):
#     #         return (False, "File riwayat.csv tidak ditemukan.")
            
#     #     # Buat nama file tujuan dengan timestamp
#     #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     #     nama_file_tujuan = f"riwayat_transaksi_{timestamp}.csv"
#     #     tujuan_file = os.path.join(mount_path, nama_file_tujuan)
        
#     #     # Variabel untuk melacak status mount
#     #     mount_berhasil = False
        
#     #     try:
#     #         # 2. Buat folder mount jika belum ada (dummy)
#     #         print(f"--> [USB] Membuat direktori dummy: {mount_path}")
#     #         os.makedirs(mount_path, exist_ok=True)
            
#     #         # Di sini seharusnya ada 'sudo mount /dev/sda1 ...' di Raspi asli
#     #         # Untuk sekarang kita asumsikan ini berhasil
#     #         print("--> [USB] (Simulasi) Mount flash drive berhasil.")
#     #         mount_berhasil = True

#     #         # 3. Salin file
#     #         print(f"--> [USB] Menyalin {sumber_file} ke {tujuan_file}")
#     #         shutil.copy(sumber_file, tujuan_file)
#     #         print("--> [USB] Penyalinan file berhasil.")
            
#     #         return (True, f"Berhasil! Data diekspor ke {nama_file_tujuan}")

#     #     except Exception as e:
#     #         # Menangkap semua jenis error (IOError, permission error, dll)
#     #         print(f"!!! [USB ERROR] Terjadi kesalahan: {e}")
#     #         return (False, f"Error: {e}")
            
#     #     finally:
#     #         # 4. Unmount (Eject) flash drive JIKA sebelumnya berhasil di-mount
#     #         if mount_berhasil:
#     #             # Di sini seharusnya ada 'sudo umount ...'
#     #             print(f"--> [USB] (Simulasi) Unmount flash drive dari {mount_path}.")
#     #             # Kita bisa coba hapus folder dummy untuk simulasi unmount
#     #             try:
#     #                 os.rmdir(mount_path)
#     #             except OSError:
#     #                 # Folder tidak kosong, biarkan saja untuk simulasi ini
#     #                 pass
#     # def export_csv_to_usb(self, device_path='/dev/sda1', mount_path='/mnt/usb_drive'):
#     #     """
#     #     Menjalankan proses mount, copy, dan unmount flash drive di lingkungan Linux/Raspi.
#     #     Mengembalikan tuple (boolean_sukses, pesan_status).
#     #     """
#     #     sumber_file = 'riwayat_transaksi.csv'
        
#     #     if not os.path.exists(sumber_file):
#     #         return (False, "File riwayat.csv tidak ditemukan.")
            
#     #     timestamp = datetime.now().strftime("%Y%m%d_%H%MS")
#     #     nama_file_tujuan = f"riwayat_{timestamp}.csv"
#     #     tujuan_file = os.path.join(mount_path, nama_file_tujuan)
        
#     #     mount_berhasil = False
        
#     #     try:
#     #         # 1. Buat folder mount jika belum ada
#     #         if not os.path.exists(mount_path):
#     #             print(f"--> [USB] Membuat direktori mount point: {mount_path}")
#     #             # Perintah 'mkdir -p' aman untuk dijalankan meski folder sudah ada
#     #             subprocess.run(['sudo', 'mkdir', '-p', mount_path], check=True)

#     #         # 2. Mount flash drive
#     #         print(f"--> [USB] Mencoba me-mount {device_path} ke {mount_path}")
#     #         # 'check=True' akan memunculkan error jika mount gagal (misal: flashdisk tidak ada)
#     #         subprocess.run(['sudo', 'mount', device_path, mount_path], check=True, timeout=10)
#     #         mount_berhasil = True
#     #         print("--> [USB] Mount flash drive berhasil.")

#     #         # 3. Salin file
#     #         print(f"--> [USB] Menyalin {sumber_file} ke {tujuan_file}")
#     #         shutil.copy(sumber_file, tujuan_file)
#     #         print("--> [USB] Penyalinan file berhasil.")
            
#     #         # 'sync' memastikan semua data benar-benar tertulis ke flashdisk sebelum unmount
#     #         subprocess.run(['sync'], check=True)
            
#     #         return (True, f"Berhasil! Data diekspor ke {nama_file_tujuan}")

#     #     except FileNotFoundError:
#     #         return (False, "Perintah 'sudo' tidak ditemukan. Pastikan berjalan di Raspi.")
#     #     except subprocess.CalledProcessError as e:
#     #         # Error ini paling sering muncul jika mount gagal
#     #         print(f"!!! [USB ERROR] Perintah sistem gagal: {e}")
#     #         return (False, "Gagal me-mount. Pastikan USB terpasang dengan benar.")
#     #     except Exception as e:
#     #         print(f"!!! [USB ERROR] Terjadi kesalahan tak terduga: {e}")
#     #         return (False, f"Error: {str(e)}")
            
#     #     finally:
#     #         # 4. Unmount flash drive, APAPUN YANG TERJADI (jika sudah termount)
#     #         if mount_berhasil:
#     #             print(f"--> [USB] Unmount (eject) flash drive dari {mount_path}.")
#     #             try:
#     #                 # 'lazy unmount' lebih aman jika ada proses yang masih berjalan
#     #                 subprocess.run(['sudo', 'umount', '-l', mount_path], check=True)
#     #             except Exception as e:
#     #                 print(f"!!! [USB ERROR] Gagal melakukan unmount: {e}")


# # ... (Semua kode di atas metode ini tetap sama) ...
#     # --- GANTI METODE LAMA DENGAN VERSI INI ---
# # ... (Semua kode di atas metode ini tetap sama) ...
#     # --- GANTI METODE LAMA DENGAN VERSI INI ---
#     def export_csv_to_usb(self, device_path='/dev/sda1', mount_path='/mnt/usb_drive'):
#         """
#         Menjalankan proses mount, copy, dan unmount, dengan perbaikan izin.
#         Mengembalikan tuple (boolean_sukses, pesan_status).
#         """
#         sumber_file = 'riwayat_transaksi.csv'
        
#         if not os.path.exists(sumber_file):
#             return (False, "File riwayat.csv tidak ditemukan.")
            
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         nama_file_tujuan = f"riwayat_{timestamp}.csv"
#         tujuan_file = os.path.join(mount_path, nama_file_tujuan)
        
#         mount_berhasil = False
        
#         try:
#             # LANGKAH 1: Unmount dulu jika perlu (mengatasi auto-mount)
#             self._unmount_dulu_jika_perlu(device_path)

#             # LANGKAH 2: Buat folder mount jika belum ada
#             if not os.path.exists(mount_path):
#                 subprocess.run(['sudo', 'mkdir', '-p', mount_path], check=True)

#             # LANGKAH 3A: Mount flash drive ke lokasi standar kita
#             print(f"--> [USB] Mencoba me-mount {device_path} ke {mount_path}")
#             subprocess.run(['sudo', 'mount', device_path, mount_path], check=True, timeout=10)
#             mount_berhasil = True
#             print("--> [USB] Mount flash drive berhasil.")

#             # --- INI BAGIAN PENTINGNYA ---
#             # LANGKAH 3B: Ganti kepemilikan folder ke user saat ini agar bisa menulis file
#             current_user = os.getlogin()
#             print(f"--> [USB] Memberikan izin tulis ke user: {current_user}")
#             subprocess.run(['sudo', 'chown', f"{current_user}:{current_user}", mount_path], check=True)
#             # -----------------------------

#             # LANGKAH 4: Salin file (sekarang sudah punya izin)
#             print(f"--> [USB] Menyalin {sumber_file} ke {tujuan_file}")
#             shutil.copy(sumber_file, tujuan_file)
#             print("--> [USB] Penyalinan file berhasil.")
            
#             subprocess.run(['sync'], check=True)
            
#             return (True, f"Berhasil! Data diekspor ke {nama_file_tujuan}")

#         except FileNotFoundError:
#             return (False, "Perintah 'sudo' tidak ditemukan. Pastikan berjalan di Raspi.")
#         except subprocess.CalledProcessErorr as e:
#             print(f"!!! [USB ERROR] Perintah sistem gagal: {e}")
#             return (False, "Gagal. Pastikan USB terpasang & user punya hak sudo.")
#         except Exception as e:
#             print(f"!!! [USB ERROR] Terjadi kesalahan tak terduga: {e}")
#             return (False, f"Error: {str(e)}")
            
#         finally:
#             # LANGKAH 5: Selalu unmount dari lokasi standar kita
#             if mount_berhasil:
#                 print(f"--> [USB] Unmount (eject) flash drive dari {mount_path}.")
#                 try:
#                     subprocess.run(['sudo', 'umount', '-l', mount_path], check=True)
#                 except Exception as e:
#                     print(f"!!! [USB ERROR] Gagal melakukan unmount: {e}")

#     # ... (Metode _unmount_dulu_jika_perlu dan sisa kode lainnya tetap sama) ...



#     def _unmount_dulu_jika_perlu(self, device_path):
#         """Metode pembantu untuk unmount perangkat sebelum me-mount ulang."""
#         print(f"--> [USB] Memastikan {device_path} tidak sedang ter-mount (mengatasi auto-mount)...")
#         try:
#             # check=False agar tidak error jika perangkat memang belum ter-mount
#             # Pipa stdout dan stderr ke DEVNULL agar tidak ada output di terminal
#             subprocess.run(
#                 ['sudo', 'umount', device_path], 
#                 check=False, 
#                 stdout=subprocess.DEVNULL, 
#                 stderr=subprocess.DEVNULL
#             )
#         except Exception as e:
#             print(f"--> [USB] Info: Gagal unmount awal (mungkin tidak apa-apa): {e}")

# # ... (Sisa kode di model.py tetap sama) ...




# MultipleFiles/model.py
import requests
from requests.exceptions import RequestException
import subprocess
import shutil
import os
import time
from random import uniform
import csv
from datetime import datetime
from recv import ArduinoSensorReader

# --- Fungsi Utilitas dan Variabel Global ---
URL_HEALTH = "http://10.46.7.51:8000/api/connection/status"

def is_server_online(timeout=2):
    """Mengecek apakah server utama online."""
    try:
        response = requests.get(URL_HEALTH, timeout=timeout)
        return response.status_code == 200
    except RequestException:
        return False
# -------------------------------------------

class TrashDataModel:
    def __init__(self):
        self.beratSementara = 0.0
        self.trash_data = {
            "flow": 0, "source": 0, "type": 0,
            "bag_count": 0, "weight": 0, "current_weight": 0
        }
        self.flow = {0: "Masuk", 1: "Keluar"}
        self.location_map = {
            0: "Mulai", 1: "KPFT", 2: "DTNTF", 3: "DTETI", 4: "DTMI", 5: "DTK",
            6: "DTAP", 7: "DTGD", 8: "DTSL", 9: "DTGL", 10: "LTM"
        }
        self.type_map = {
            0: "Mulai", 1: "Sapuan", 2: "Anorganik Kering/Rosok",
            3: "Residu", 4: "Sisa Makanan"
        }
        self.url_kirim = "http://10.46.7.51:8000/api/sensor/data"
        self.arduino_reader = ArduinoSensorReader()
        self.arduino_reader.connect()
        self.listBerat = []

    def get_trash_data(self):
        return self.trash_data
    
    def set_flow(self, flow_code):
        self.trash_data["flow"] = flow_code
        
    def get_flow_name(self, code):
        return self.flow.get(code,"Unknown Flow")
        
    def set_source(self, source_code):
        self.trash_data["source"] = source_code

    def set_type(self, type_code):
        self.trash_data["type"] = type_code

    def get_location_name(self, code):
        return self.location_map.get(code, "Unknown Location")

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
        self.trash_data = {k: 0 for k in self.trash_data}
        self.listBerat.clear()
        return self.trash_data
    
    def undo_bag_data(self):
        if not self.listBerat:
            return self.reset_data()
        
        last_weight = self.listBerat.pop()
        self.trash_data["weight"] -= last_weight
        self.trash_data["bag_count"] -= 1
        self.trash_data["current_weight"] = self.listBerat[-1] if self.listBerat else 0
        return self.trash_data

    def send_all_data(self):
        try:
            requests.post(self.url_kirim, json=self.trash_data, timeout=5)
            print("--> [ONLINE] Data berhasil dikirim ke server.")
            self._simpan_log_lokal_csv(self.trash_data, 'online')
        except RequestException as e:
            print(f"!!! [OFFLINE] Gagal mengirim data: {e}. Mencatat sebagai offline.")
            self._simpan_log_lokal_csv(self.trash_data, 'offline')

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
            print(f"--> [LOG] Transaksi berhasil dicatat ke {nama_file} dengan status '{status}'")
        except Exception as e:
            print(f"!!! [ERROR] Gagal mencatat log lokal: {e} !!!")

    def sync_offline_data(self):
        nama_file = 'riwayat_transaksi.csv'
        if not os.path.exists(nama_file):
            return
        
        semua_data = []
        data_untuk_disinkronkan = []
        try:
            with open(nama_file, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    semua_data.append(row)
                    if row.get('status_pengiriman') == 'offline':
                        data_untuk_disinkronkan.append(row)
            
            if not data_untuk_disinkronkan:
                print("--> [SYNC] Tidak ada data offline yang perlu dikirim.")
                return

            print(f"--> [SYNC] Ditemukan {len(data_untuk_disinkronkan)} data untuk disinkronkan.")
            
            berhasil_sync = 0
            for data_offline in data_untuk_disinkronkan:
                try:
                    payload = {
                        "flow": int(data_offline['flow']),
                        "source": int(data_offline['source']),
                        "type": int(data_offline['type']),
                        "bag_count": int(data_offline['bag_count']),
                        "weight": float(data_offline['weight']),
                        "timestamp_offline": data_offline['timestamp']
                    }
                    requests.post(self.url_kirim, json=payload, timeout=10)
                    for data in semua_data:
                        if data['timestamp'] == data_offline['timestamp']:
                            data['status_pengiriman'] = 'synced'
                            break
                    print(f"--> [SYNC] Berhasil mengirim data timestamp: {data_offline['timestamp']}")
                    berhasil_sync += 1
                except RequestException as e:
                    print(f"!!! [SYNC ERROR] Gagal mengirim data {data_offline['timestamp']}: {e}. Akan dicoba lagi nanti.")
                    break
                except (ValueError, KeyError) as e:
                    print(f"!!! [SYNC ERROR] Format data salah untuk {data_offline['timestamp']}: {e}. Menandai sebagai 'corrupt'.")
                    for data in semua_data:
                        if data['timestamp'] == data_offline['timestamp']:
                            data['status_pengiriman'] = 'corrupt'
                            break

            if berhasil_sync > 0:
                print("--> [SYNC] Menulis ulang file log dengan status baru...")
                with open(nama_file, mode='w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=semua_data[0].keys())
                    writer.writeheader()
                    writer.writerows(semua_data)
                print("--> [SYNC] File log berhasil diperbarui.")

        except Exception as e:
            print(f"!!! [SYNC ERROR] Terjadi kesalahan saat proses sinkronisasi: {e}")

    def tare(self):
        # ... (implementasi tare)
        pass

    def update_weight(self):
        self.beratSementara = self.measure_mass()
        return self.beratSementara

    def _unmount_dulu_jika_perlu(self, device_path):
        """Metode pembantu untuk unmount perangkat sebelum me-mount ulang."""
        print(f"--> [USB] Memastikan {device_path} tidak sedang ter-mount (mengatasi auto-mount)...")
        try:
            subprocess.run(['sudo', 'umount', device_path], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"--> [USB] Info: Gagal unmount awal (mungkin tidak apa-apa): {e}")

    def export_csv_to_usb(self, device_path='/dev/sda1', mount_path='/mnt/usb_drive'):
        """
        Menjalankan proses mount, copy, dan unmount, dengan perbaikan izin.
        """
        sumber_file = 'riwayat_transaksi.csv'
        if not os.path.exists(sumber_file):
            return (False, "File riwayat.csv tidak ditemukan.")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nama_file_tujuan = f"riwayat_{timestamp}.csv"
        tujuan_file = os.path.join(mount_path, nama_file_tujuan)
        mount_berhasil = False
        
        try:
            self._unmount_dulu_jika_perlu(device_path)
            
            if not os.path.exists(mount_path):
                subprocess.run(['sudo', 'mkdir', '-p', mount_path], check=True)

            # --- INI ADALAH PERBAIKAN UTAMANYA ---
            # Dapatkan ID user dan group yang sedang menjalankan skrip
            current_uid = str(os.getuid())
            current_gid = str(os.getgid())
            mount_options = f'uid={current_uid},gid={current_gid}'
            
            # Mount dengan opsi untuk memberikan izin tulis secara otomatis
            print(f"--> [USB] Mencoba me-mount {device_path} ke {mount_path} dengan izin untuk user {current_uid}")
            subprocess.run(
                ['sudo', 'mount', '-o', mount_options, device_path, mount_path], 
                check=True, 
                timeout=10
            )
            mount_berhasil = True
            print("--> [USB] Mount flash drive berhasil.")
            # ---------------------------------------------

            print(f"--> [USB] Menyalin {sumber_file} ke {tujuan_file}")
            shutil.copy(sumber_file, tujuan_file)
            print("--> [USB] Penyalinan file berhasil.")
            
            # 'sync' memastikan semua data benar-benar tertulis ke flashdisk
            subprocess.run(['sync'], check=True)
            
            return (True, f"Berhasil! Data diekspor ke {nama_file_tujuan}")

        except FileNotFoundError:
            return (False, "Perintah 'sudo' tidak ditemukan. Pastikan berjalan di Raspi.")
        except subprocess.CalledProcessError as e: # <-- TYPO SUDAH DIPERBAIKI
            print(f"!!! [USB ERROR] Perintah sistem gagal: {e}")
            return (False, "Gagal. Pastikan USB terpasang & user punya hak sudo.")
        except Exception as e:
            print(f"!!! [USB ERROR] Terjadi kesalahan tak terduga: {e}")
            return (False, f"Error: {str(e)}")
            
        finally:
            if mount_berhasil:
                print(f"--> [USB] Unmount (eject) flash drive dari {mount_path}.")
                try:
                    subprocess.run(['sudo', 'umount', '-l', mount_path], check=True)
                except Exception as e:
                    print(f"!!! [USB ERROR] Gagal melakukan unmount: {e}")

