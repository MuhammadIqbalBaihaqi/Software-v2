# import tkinter as tk
# from tkinter import ttk
# from pathlib import Path
# from views import MainPage, LocationPage, TypePage, WeighPage
# from model import TrashDataModel  # pastikan model.py di path yang sama

# # Import PhotoImage
# from tkinter import PhotoImage

# class TrashSortingApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.model = TrashDataModel()  # Model integrasi
#         # # Load icon status server
#         # self.icon_online = PhotoImage(file="build/assets/online.png")
#         # self.icon_offline = PhotoImage(file="build/assets/offline.png")

#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
#         for FrameClass in (MainPage, LocationPage, TypePage, WeighPage):
#             frame = FrameClass(container, self)
#             self.frames[FrameClass] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame(MainPage)

#     def show_frame(self, frame_class):
#         for frame in self.frames.values():
#             frame.grid_remove()
#         frame = self.frames[frame_class]
#         # Update status icon kalau page punya method update_status_icon
#         if hasattr(frame, 'update_status_icon'):
#             frame.update_status_icon()
#         # Update display jika frame punya method update_display
#         if hasattr(frame, 'update_display'):
#             frame.update_display()
#         frame.grid()
#         frame.tkraise()
#         if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
#             frame.start_auto_update()
#     # Stop auto update jika bukan WeighPage
#         elif hasattr(frame, 'stop_auto_update'):
#             frame.stop_auto_update()

#     # ---- Navigation logic ----
#     def set_category_and_next(self, category):
#         self.model.trash_data["flow"] = category
#         self.show_frame(LocationPage)

#     def set_location_and_next(self, location_code, location_name):
#         self.model.set_source(location_code)
#         self.model.trash_data["source_name"] = location_name
#         self.show_frame(TypePage)

#     def set_type_and_next(self, type_code, type_name):
#         self.model.set_type(type_code)
#         self.model.trash_data["type_name"] = type_name
#         self.show_frame(WeighPage)

#     def handle_weigh(self):
#         updated_data = self.model.update_bag_data()
#         # Update display pada WeighPage
#         self.frames[WeighPage].update_display()

#     def handle_finish(self):
#         self.model.send_all_data()
#         print("udah")
#         self.model.reset_data()
#         self.show_frame(MainPage)

#     def handle_reset(self):
#         self.model.reset_data()
#         #self.show_frame(MainPage)
#         self.frames[WeighPage].update_display()
#     def handle_undo(self):
#         self.model.undo_bag_data()
#         # Update display pada WeighPage
#         self.frames[WeighPage].update_display() 

#     def handle_tare(self):
#         self.model.tare()
#         # Update display pada WeighPage
#         self.frames[WeighPage].update_display()


# if __name__ == "__main__":
#     app = TrashSortingApp()
#     app.title("Timbangan Sampah Digital - MVC Integrated")
#     app.geometry("1024x600")
#     app.resizable(False, False)
#     app.attributes('-fullscreen', True)
#     # app.overrideredirect(True)
#     app.mainloop()


# import tkinter as tk
# from tkinter import ttk
# from pathlib import Path
# from views import MainPage, LocationPage, TypePage, WeighPage
# from model import TrashDataModel, is_server_online
# import threading
# import time

# # Import PhotoImage
# from tkinter import PhotoImage

# class TrashSortingApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.model = TrashDataModel()  # Model integrasi
        
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
#         for FrameClass in (MainPage, LocationPage, TypePage, WeighPage):
#             frame = FrameClass(container, self)
#             self.frames[FrameClass] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame(MainPage)

#         # ---- TAMBAHAN BARU: Mulai background thread untuk sinkronisasi ----
#         self._start_sync_thread()
#         self.protocol("WM_DELETE_WINDOW", self._on_closing) # Handle penutupan window

#     def _start_sync_thread(self):
#         """Membuat dan memulai thread background untuk sinkronisasi."""
#         self.sync_thread_running = True
#         # daemon=True memastikan thread berhenti saat program utama berhenti
#         self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
#         self.sync_thread.start()
#         print("[SYNC THREAD] Agen sinkronisasi background telah dimulai.")

#     def _sync_loop(self):
#         """Loop yang berjalan di background untuk mengecek dan sinkronisasi data."""
#         # Beri jeda 5 detik saat start-up sebelum pengecekan pertama
#         time.sleep(5) 
#         while self.sync_thread_running:
#             try:
#                 # Cek koneksi ke server
#                 if is_server_online():
#                     # Jika online, coba jalankan proses sinkronisasi
#                     self.model.sync_offline_data()
#                 else:
#                     print("[SYNC THREAD] Server offline, akan dicek lagi nanti.")
#             except Exception as e:
#                 print(f"[SYNC THREAD] Terjadi error di loop sinkronisasi: {e}")
            
#             # Tunggu 60 detik sebelum mencoba lagi
#             print("[SYNC THREAD] Tidur selama 60 detik...")
#             time.sleep(30)

#     def _on_closing(self):
#         """Fungsi yang dipanggil saat aplikasi ditutup."""
#         print("[APP] Aplikasi sedang ditutup, menghentikan background thread...")
#         self.sync_thread_running = False
#         self.destroy()

#     def show_frame(self, frame_class):
#         for frame in self.frames.values():
#             frame.grid_remove()
#         frame = self.frames[frame_class]
#         if hasattr(frame, 'update_display'):
#             frame.update_display()
#         frame.grid()
#         frame.tkraise()
#         if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
#             frame.start_auto_update()
#         elif hasattr(frame, 'stop_auto_update'):
#             frame.stop_auto_update()

#     # ---- Navigation logic ----
#     def set_category_and_next(self, category):
#         self.model.trash_data["flow"] = category
#         self.show_frame(LocationPage)

#     def set_location_and_next(self, location_code, location_name):
#         self.model.set_source(location_code)
#         self.model.trash_data["source_name"] = location_name
#         self.show_frame(TypePage)

#     def set_type_and_next(self, type_code, type_name):
#         self.model.set_type(type_code)
#         self.model.trash_data["type_name"] = type_name
#         self.show_frame(WeighPage)

#     def handle_weigh(self):
#         self.model.update_bag_data()
#         self.frames[WeighPage].update_display()

#     def handle_finish(self):
#         self.model.send_all_data()
#         self.model.reset_data()
#         self.show_frame(MainPage)

#     def handle_reset(self):
#         self.model.reset_data()
#         self.frames[WeighPage].update_display()
        
#     def handle_undo(self):
#         self.model.undo_bag_data()
#         self.frames[WeighPage].update_display() 

#     def handle_tare(self):
#         self.model.tare()
#         self.frames[WeighPage].update_display()


# if __name__ == "__main__":
#     app = TrashSortingApp()
#     app.title("Timbangan Sampah Digital - MVC Integrated")
#     app.geometry("1024x600")
#     app.resizable(False, False)
#     # app.attributes('-fullscreen', True) # Aktifkan saat deployment
#     app.mainloop()


# import tkinter as tk
# from tkinter import ttk
# from pathlib import Path
# from views import MainPage, LocationPage, TypePage, WeighPage
# from model import TrashDataModel, is_server_online
# import threading
# import time

# from tkinter import PhotoImage

# class TrashSortingApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self.model = TrashDataModel()
        
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
#         for FrameClass in (MainPage, LocationPage, TypePage, WeighPage):
#             frame = FrameClass(container, self)
#             self.frames[FrameClass] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame(MainPage)
#         self._start_sync_thread()
#         self.protocol("WM_DELETE_WINDOW", self._on_closing)

#     def _start_sync_thread(self):
#         self.sync_thread_running = True
#         self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
#         self.sync_thread.start()

#     def _sync_loop(self):
#         time.sleep(5) 
#         while self.sync_thread_running:
#             try:
#                 if is_server_online():
#                     self.model.sync_offline_data()
#             except Exception:
#                 pass
#             time.sleep(30)

#     def _on_closing(self):
#         self.sync_thread_running = False
#         self.destroy()

#     def show_frame(self, frame_class):
#         for frame in self.frames.values(): frame.grid_remove()
#         frame = self.frames[frame_class]
#         if hasattr(frame, 'update_display'): frame.update_display()
#         frame.grid()
#         frame.tkraise()
#         if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
#             frame.start_auto_update()
#         elif hasattr(frame, 'stop_auto_update'):
#             frame.stop_auto_update()

#     def set_category_and_next(self, category):
#         self.model.trash_data["flow"] = category
#         self.show_frame(LocationPage)

#     def set_location_and_next(self, location_code, location_name):
#         self.model.set_source(location_code)
#         self.show_frame(TypePage)

#     def set_type_and_next(self, type_code, type_name):
#         self.model.set_type(type_code)
#         self.show_frame(WeighPage)

#     def handle_weigh(self):
#         self.model.update_bag_data()
#         self.frames[WeighPage].update_display()

#     def handle_finish(self):
#         self.model.send_all_data()
#         self.model.reset_data()
#         self.show_frame(MainPage)

#     def handle_reset(self):
#         self.model.reset_data()
#         self.frames[WeighPage].update_display()
        
#     def handle_undo(self):
#         self.model.undo_bag_data()
#         self.frames[WeighPage].update_display() 

#     def handle_tare(self):
#         self.model.tare()
#         self.frames[WeighPage].update_display()

#     def handle_fetch_to_usb(self):
#         # Nuduhake notifikasi "Loading" nang MainPage
#         main_page = self.frames[MainPage]
#         main_page.show_notification("Nyalin menyang USB, tulung dienteni...", color="blue", duration=0)
        
#         copy_thread = threading.Thread(target=self._execute_usb_copy, daemon=True)
#         copy_thread.start()

#     def _execute_usb_copy(self):
#         success, message = self.model.export_csv_to_usb()
#         self.after(0, self._update_ui_after_copy, success, message)

#     def _update_ui_after_copy(self, success, message):
#         """
#         Method iki mlaku ing main thread.
#         Aman kanggo nganyari UI nganggo hasil saka background task.
#         """
#         # --- IKI OWAH-OWAHANE ---
#         # Saiki ngirim notifikasi menyang MainPage, dudu WeighPage maneh
#         main_page = self.frames[MainPage]
#         if success:
#             final_message = f"{message}. Monggo USB dicabut."
#             main_page.show_notification(final_message, color="green", duration=10000)
#         else:
#             main_page.show_notification(message, color="red", duration=10000)
            
# if __name__ == "__main__":
#     app = TrashSortingApp()
#     app.title("Timbangan Sampah Digital - MVC Integrated")
#     app.geometry("1024x600")
#     # app.attributes('-fullscreen', True)
#     app.mainloop()


import tkinter as tk
from tkinter import ttk
from pathlib import Path
from views import MainPage, LocationPage, TypePage, WeighPage
from model import TrashDataModel, is_server_online
import threading
import time

# Import PhotoImage (sanajan ora digunakake langsung ing kene, luwih becik tetep ana)
from tkinter import PhotoImage

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
        self._start_sync_thread()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _start_sync_thread(self):
        self.sync_thread_running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        print("[SYNC THREAD] Agen sinkronisasi background wis diwiwiti.")

    def _sync_loop(self):
        time.sleep(5) 
        while self.sync_thread_running:
            try:
                if is_server_online():
                    self.model.sync_offline_data()
                else:
                    print("[SYNC THREAD] Server offline, bakal dicek maneh mengko.")
            except Exception as e:
                print(f"[SYNC THREAD] Ana error ing loop sinkronisasi: {e}")
            
            print("[SYNC THREAD] Turu sedhela 30 detik...")
            time.sleep(30)

    def _on_closing(self):
        print("[APP] Aplikasi arep ditutup, mandhegake background thread...")
        self.sync_thread_running = False
        self.destroy()

    def show_frame(self, frame_class):
        for frame in self.frames.values(): frame.grid_remove()
        frame = self.frames[frame_class]
        if hasattr(frame, 'update_display'): frame.update_display()
        frame.grid()
        frame.tkraise()
        if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
            frame.start_auto_update()
        elif hasattr(frame, 'stop_auto_update'):
            frame.stop_auto_update()

    # --- Logika Navigasi ---
    def set_category_and_next(self, category):
        self.model.trash_data["flow"] = category
        self.show_frame(LocationPage)

    def set_location_and_next(self, location_code, location_name):
        self.model.set_source(location_code)
        self.show_frame(TypePage)

    def set_type_and_next(self, type_code, type_name):
        self.model.set_type(type_code)
        self.show_frame(WeighPage)

    # --- Penanganan Aksi Tombol ---
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

    # --- BAGIAN PENTING: Penanganan Ekspor USB ---
    def handle_fetch_to_usb(self):
        """
        Miwiti proses nyalin menyang USB ing background thread
        supados GUI ora macet.
        """
        print("--> [USB EXPORT] Tombol diklik. Nampilake notifikasi 'loading'...")
        # 1. Tampilake notifikasi "Loading" langsung nang GUI
        main_page = self.frames[MainPage]
        main_page.show_notification("Nyalin menyang USB, tulung dienteni...", color="blue", duration=0)
        
        # 2. Gawe lan wiwiti "Pelari Background" kanggo tugas abot
        copy_thread = threading.Thread(target=self._execute_usb_copy, daemon=True)
        copy_thread.start()

    def _execute_usb_copy(self):
        """
        Method iki mlaku ing background. Aman kanggo tugas sing suwe.
        """
        print("--> [USB EXPORT] Background thread mlaku. Miwiti proses ekspor...")
        success, message = self.model.export_csv_to_usb()
        
        # 3. Kirim hasil bali menyang "Pelari Utama" kanthi aman
        self.after(0, self._update_ui_after_copy, success, message)

    def _update_ui_after_copy(self, success, message):
        """
        Method iki mlaku ing main thread.
        Aman kanggo nganyari UI nganggo hasil saka background task.
        """
        print(f"--> [USB EXPORT] Tugas rampung. Hasil: {message}. Nganyari GUI...")
        # 4. Tampilake notifikasi hasil akhir nang GUI
        main_page = self.frames[MainPage]
        if success:
            final_message = f"{message}. Monggo USB dicabut."
            main_page.show_notification(final_message, color="green", duration=10000)
        else:
            main_page.show_notification(message, color="red", duration=10000)
            
if __name__ == "__main__":
    app = TrashSortingApp()
    app.title("Timbangan Sampah Digital - MVC Integrated")
    app.geometry("1024x600")
    # app.attributes('-fullscreen', True)
    app.mainloop()

