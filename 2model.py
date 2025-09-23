# MultipleFiles/model.py
#from asyncio import timeout
import requests
from requests.exceptions import Timeout
import subprocess
import shutil
import os
import time
from random import uniform
import csv
from datetime import datetime

# Import ArduinoSensorReader dari modul recv
from recv import ArduinoSensorReader
url_health = "http://10.46.7.51:8000/api/connection/status" # Pindahkan ke sini
def is_server_online(url_health, timeout=2): # Jadikan method dari class
    """Mengecek apakah server utama online."""
    try:
        print(f"--> [DEBUG] Mengirim request ke: {url_health}")
        response = requests.get(url_health, timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"!!! [DEBUG] GAGAL mengirim request: {e} !!!")
        return False  

# Optional: If you plan to use the HX711 sensor, uncomment and ensure it's installed
# import RPi.GPIO as GPIO
# from hx711 import HX711

class TrashDataModel:
    listBerat = []
    def __init__(self):
        self.beratSementara = 0.0
        self.trash_data = {
            "flow":0,
            "source": 0,
            "type": 0,
            "bag_count": 0,
            "weight": 0,
            "current_weight": 0
        }
        self.flow = {
            0:"Masuk", 1:"Keluar"
        }
        self.location_map = {
            0:"Mulai", 1:"KPFT", 2:"DTNTF", 3:"DTETI",
            4:"DTMI", 5:"DTK", 6:"DTAP", 7:"DTGD",
            8:"DTSL", 9:"DTGL", 10:"LTM"
        }
        self.type_map = {
            0:"Mulai", 1:"Sapuan", 2:"Anorganik Kering/Rosok",
            3:"Residu", 4:"Sisa Makanan"
        }
        self.url_kirim = "http://10.46.7.51:8000/api/sensor/data"
        self.url_csv = "http://192.168.215.174:3000/api/sensor/data" # Assuming this URL is active
        self.url_kirim1 = "http://192.168.215.174:3000/api/sensor/data" # Assuming this URL is active
    
        # Inisialisasi ArduinoSensorReader
        self.arduino_reader = ArduinoSensorReader()
        self.arduino_reader.connect() # Coba koneksi saat inisialisasi model

            # Initialize HX711 if EMULATE_HX711 is False
            # if not EMULATE_HX711:
            #     self.hx = HX711(5, 6)
            #     self.hx.set_reading_format("MSB", "MSB")
            #     self.hx.reset()
            #     self.hx.tare()

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
        # Mengambil data berat dari ArduinoSensorReader
        val_A = self.arduino_reader.get_latest_weight()

        # Jika berat sangat kecil (mendekati nol), anggap nol
        # Ini untuk menghindari pembacaan noise kecil saat tidak ada beban
        if abs((val_A/1000)) < 0.05: # Ambang batas 0.05 kg (50 gram)
            val_A = 0.0
        
        # Karena Arduino sudah mengirim dalam kg, tidak perlu konversi lagi
        return round((val_A/1000), 3)

    def update_bag_data(self):
        current_weight = round(self.beratSementara, 1)
        self.listBerat.append(current_weight)
        self.trash_data["current_weight"] = current_weight
        self.trash_data["bag_count"] += 1
        self.trash_data["weight"] += current_weight
        return self.trash_data

    def reset_data(self):
        self.trash_data["bag_count"] = 0
        self.trash_data["weight"] = 0
        self.trash_data["current_weight"] = 0
        self.listBerat.clear()
        return self.trash_data
    
    def undo_bag_data(self):
        if self.trash_data["bag_count"] == 1 or self.trash_data["bag_count"] == 0:
            self.trash_data["bag_count"] = 0
            current_weight = 0
            self.trash_data["weight"] = 0
            self.trash_data["current_weight"] = 0
            if self.listBerat: # Pastikan list tidak kosong sebelum pop
                self.listBerat.pop()
            return self.trash_data
        self.trash_data["bag_count"] -= 1
        current_weight = self.listBerat[self.trash_data["bag_count"]]
        self.trash_data["weight"] -= current_weight
        self.trash_data["current_weight"] = self.listBerat[self.trash_data["bag_count"] - 1] if self.trash_data["bag_count"] > 0 else 0
        if self.listBerat: # Pastikan list tidak kosong sebelum pop
            self.listBerat.pop()
        return self.trash_data

    def _fd_backup(self, file, mount_path='/mnt/usb'):
        os.makedirs(mount_path, exist_ok=True)
        try:
            mount_command = ['sudo', 'mount', '/dev/sda1', mount_path]
            subprocess.run(mount_command, check=True)
            destination_path = os.path.join(mount_path, os.path.basename(file))
            shutil.copy(file, destination_path)
        except subprocess.CalledProcessError as e:
            print(f"Error during USB mount/copy: {e}")
        finally:
            umount_command = ['sudo', 'umount', mount_path]
            subprocess.run(umount_command, check=True)

    def _simpan_csv(self):
        try:
            data_csv = requests.get(self.url_csv)
            with open("/home//azsig/Documents/magang/sampah_FT.csv", mode="wb") as file:
                for chunk in data_csv.iter_content():
                    file.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching CSV: {e}")

    # def send_all_data(self):
    #     try:
    #         requests.post(self.url_kirim, json=self.trash_data)
    #    #     self._simpan_csv()
    #         print("send data")
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error sending data to main server: {e}")
    
    # Di dalam class TrashDataModel di model.py

    def send_all_data(self):
        """
        Mencoba mengirim data ke server, lalu mencatat hasilnya (online/offline)
        ke log CSV lokal.
        """
        try:
            # Coba kirim data dengan timeout 5 detik
            requests.post(self.url_kirim, json=self.trash_data, timeout=5)
            
            # Jika berhasil, catat log dengan status 'online'
            print("--> [ONLINE] Data berhasil dikirim ke server.")
            self._simpan_log_lokal_csv(self.trash_data, 'online')

        except requests.exceptions.RequestException as e:
            # Jika gagal, catat log dengan status 'offline'
            print(f"!!! [OFFLINE] Gagal mengirim data: {e}. Mencatat sebagai offline.")
            self._simpan_log_lokal_csv(self.trash_data, 'offline')    
        #try:
        #    self._fd_backup("/home/pi/hx711py/sampah_FT.csv")
        #except Exception as e:
        #    print(f"Error during USB backup: {e}")
    
    # Di dalam class TrashDataModel di model.py

    def _simpan_log_lokal_csv(self, data_transaksi, status):
        """
        Mencatat SETIAP transaksi (online/offline) ke file CSV lokal.
        """
        nama_file = 'riwayat_transaksi.csv'
        data_untuk_disimpan = data_transaksi.copy()

        # 1. Tambahkan informasi tambahan (status dan timestamp)
        data_untuk_disimpan['timestamp'] = datetime.now().isoformat()
        data_untuk_disimpan['status_pengiriman'] = status
        
        # 2. Tentukan header untuk file CSV
        # Pastikan urutannya konsisten
        fieldnames = [
            'timestamp', 'flow', 'source', 'type', 
            'bag_count', 'weight', 'status_pengiriman'
        ]

        try:
            file_sudah_ada = os.path.exists(nama_file)
            
            with open(nama_file, mode='a', newline='') as csvfile:
                # Gunakan DictWriter untuk menulis berdasarkan nama kolom
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                
                if not file_sudah_ada:
                    writer.writeheader()
                
                writer.writerow(data_untuk_disimpan)
                
            print(f"--> [LOG] Transaksi berhasil dicatat ke {nama_file} dengan status '{status}'")

        except Exception as e:
            print(f"!!! [ERROR] Gagal mencatat log lokal: {e} !!!")

    
    def tare(self):
        # Panggil fungsi tare dari Arduino jika ada, atau kirim sinyal ke Arduino
        self.send_signal_tare() # Ini akan memanggil fungsi di Arduino
        self.beratSementara = 0.0 # Reset berat sementara di Python
        print("Tare operation completed.")

    def update_weight(self):
        # Memanggil measure_mass untuk mendapatkan berat terbaru dari Arduino
        self.beratSementara = self.measure_mass()
        return self.beratSementara
    
    def send_signal_tare(self):
        # Fungsi ini akan mengirim sinyal 'tare' ke Arduino
        # Anda perlu menambahkan logika pengiriman serial di sini
        # Contoh: self.arduino_reader.ser.write(b'T\n')
        # Namun, karena recv.py hanya membaca, Anda mungkin perlu menambahkan
        # metode `send_command` di ArduinoSensorReader atau langsung di sini
        if self.arduino_reader.ser and self.arduino_reader.ser.is_open:
            try:
                self.arduino_reader.ser.write(b'T\n') # Kirim karakter 'T' diikuti newline
                print("Sinyal 'Tare' dikirim ke Arduino.")
            except Exception as e:
                print(f"Gagal mengirim sinyal 'Tare' ke Arduino: {e}")
        else:
            print("Arduino tidak terhubung, tidak bisa mengirim sinyal 'Tare'.")


