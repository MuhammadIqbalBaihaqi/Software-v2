# MultipleFiles/recv.py
import serial
import threading
import time
import re # Import the regular expression module

class ArduinoSensorReader:
    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=9600):
        self.SERIAL_PORT = serial_port
        self.BAUD_RATE = baud_rate
        self.ser = None
        self.latest_data = 0.0  # Variabel untuk menyimpan data terakhir dari Arduino
        self.is_running = False
        self.read_thread = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
            print(f"Terhubung ke Arduino di {self.SERIAL_PORT}")
            self.is_running = True
            self.read_thread = threading.Thread(target=self._read_from_arduino, daemon=True)
            self.read_thread.start()
            return True
        except serial.SerialException as e:
            print(f"Error koneksi ke Arduino: {e}")
            return False

    def _read_from_arduino(self):
        while self.is_running:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    # Gunakan regex untuk mengekstrak angka dari string "Weight = X.Y"
                    match = re.search(r"Weight\s*:\s*(\d+\.?\d*)", line)
                    if match:
                        try:
                            self.latest_data = float(match.group(1))
                            print(f"Data dari Arduino: {self.latest_data}") # Untuk debugging
                        except ValueError:
                            print(f"Data angka tidak valid dari Arduino: {match.group(1)}")
                    else:
                        print(f"Format data tidak dikenali: {line}")
                time.sleep(0.01) # Sedikit delay agar tidak terlalu membebani CPU
            except Exception as e:
                print(f"Error membaca dari Arduino: {e}")
                self.is_running = False # Hentikan thread jika ada error
                break

    def get_latest_weight(self):
        """Mengembalikan data berat terakhir yang dibaca dari Arduino."""
        return self.latest_data

    def disconnect(self):
        self.is_running = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=1) # Tunggu thread selesai
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Koneksi Arduino ditutup.")

# Contoh penggunaan (opsional, untuk pengujian mandiri recv.py)
if __name__ == '__main__':
    reader = ArduinoSensorReader()
    if reader.connect():
        try:
            while True:
                print(f"Berat saat ini: {reader.get_latest_weight()} kg")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Program dihentikan oleh pengguna.")
        finally:
            reader.disconnect()


