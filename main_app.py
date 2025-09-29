import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import time

from views import MainPage, LocationPage, TypePage, WeighPage
# Pastikan is_server_online diimpor dari model
from model import TrashDataModel, is_server_online

class TrashSortingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.model = TrashDataModel()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FrameClass in (MainPage, LocationPage, TypePage, WeighPage):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

        self.bind("<Escape>", self.quit_app)

        self.sync_thread_running = True
        self._start_sync_thread()

    def show_frame(self, frame_class):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[frame_class]
        if hasattr(frame, 'update_display'):
            frame.update_display()
        frame.grid()
        frame.tkraise()
        if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
            frame.start_auto_update()
        elif hasattr(frame, 'stop_auto_update'):
            frame.stop_auto_update()

    def quit_app(self, event=None):
        print("[APP] Aplikasi sedang ditutup, menghentikan background thread...")
        self.sync_thread_running = False
        self.destroy()

    # --- Handlers ---
    def set_category_and_next(self, category):
        self.model.trash_data["flow"] = category
        self.show_frame(LocationPage)

    def set_location_and_next(self, location_code, location_name):
        self.model.set_source(location_code)
        self.model.trash_data["source_name"] = location_name
        self.show_frame(TypePage)

    def set_type_and_next(self, type_code, type_name):
        self.model.set_type(type_code)
        self.model.trash_data["type_name"] = type_name
        self.show_frame(WeighPage)

    def handle_weigh(self):
        self.model.update_bag_data()
        self.frames[WeighPage].update_display()

    def handle_finish(self):
        self.model.send_all_data()
        self.model.reset_data()
        self.show_frame(MainPage)

    def handle_reset(self):
        self.model.reset_data()
        self.frames[WeighPage].update_display()

    def handle_undo(self):
        self.model.undo_bag_data()
        self.frames[WeighPage].update_display()

    def handle_tare(self):
        self.model.tare()
        self.frames[WeighPage].update_display()
    
    # --- INILAH ALUR KERJA YANG BENAR UNTUK USB ---
    def handle_fetch_to_usb(self):
        """
        Tahap 1: Dijalankan oleh Kasir (Main Thread).
        Menampilkan notif "loading" dan mendelegasikan tugas.
        """
        main_page = self.frames[MainPage]
        # Tampilkan notifikasi "loading" yang akan tetap ada sampai diperbarui
        main_page.show_notification("Menyalin ke USB, harap tunggu...", color="blue", duration=0)
        
        # Suruh Staf Gudang (thread baru) untuk mulai bekerja
        copy_thread = threading.Thread(target=self._execute_usb_copy, daemon=True)
        copy_thread.start()

    def _execute_usb_copy(self):
        """
        Tahap 2: Dijalankan oleh Staf Gudang (Background Thread).
        Melakukan pekerjaan berat.
        """
        # Panggil fungsi yang butuh waktu lama di sini
        success, message = self.model.export_csv_to_usb()
        
        # Setelah selesai, lapor kembali ke Kasir dengan aman
        self.after(0, self._update_ui_after_copy, success, message)

    def _update_ui_after_copy(self, success, message):
        """
        Tahap 3: Dijalankan kembali oleh Kasir (Main Thread).
        Memperbarui tampilan dengan hasil akhir.
        """
        main_page = self.frames[MainPage]
        if success:
            main_page.show_notification(f"{message}. Silakan cabut USB.", color="green", duration=5000)
        else:
            main_page.show_notification(message, color="red", duration=5000)
        
        # SOLUSI: Memaksa Tkinter untuk segera memproses pembaruan UI
        main_page.update_idletasks()
    # ---------------------------------------------------

    # --- Background Sync Logic ---
    def _start_sync_thread(self):
        sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        sync_thread.start()
        print("[SYNC THREAD] Agen sinkronisasi background telah dimulai.")

    def _sync_loop(self):
        time.sleep(5)
        while self.sync_thread_running:
            try:
                if is_server_online():
                    self.model.sync_offline_data()
                else:
                    print("[SYNC THREAD] Server offline, akan dicek lagi nanti.")
            except Exception as e:
                print(f"[SYNC THREAD] Terjadi error di loop sinkronisasi: {e}")
            
            print("[SYNC THREAD] Tidur selama 30 detik...")
            time.sleep(30)

if __name__ == "__main__":
    app = TrashSortingApp()
    app.title("Timbangan Sampah Digital - MVC Integrated")
    app.geometry("1024x600")
    #app.attributes('-fullscreen', True) # Dinonaktifkan untuk testing
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()
