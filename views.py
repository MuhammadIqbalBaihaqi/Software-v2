import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # Simpen controller kanggo ngakses method
        canvas = tk.Canvas(self, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.canvas = canvas

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame0")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        # --- WIDGET BARU: NOTIFIKASI ING MAINPAGE ---
        self.notification_id = canvas.create_text(
            512, 15, anchor="n", text="", font=("OpenSans Bold", 14), fill="blue"
        )
        self.notification_job = None
        # ---------------------------------------------

        try:
            image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.create_image(512.0, 50.0, image=image_image_1)
            self.image_1 = image_image_1
        except:
            canvas.create_rectangle(0, 0, 1024, 100, fill="#1e3a8a", outline="")
            canvas.create_text(90, 30, anchor="nw", text="Timbangan Sampah Digital", fill="white", font=("Arial", 18, "bold"))
        
        canvas.create_text(1024 // 2, 130.0, anchor="n", text="Pilih Kategori Sampah", fill="#343434", font=("OpenSans Bold", 26 * -1))
        
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: controller.set_category_and_next(0))
        button_1.place(x=110.0, y=200.0, width=350.0, height=300.0)
        
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: controller.set_category_and_next(1))
        button_2.place(x=564.0, y=200.0, width=350.0, height=300.0)

        # --- TOMBOL BARU: SALIN MENYANG USB ING MAINPAGE ---
        # Diselehke nang pojok tengen ndhuwur
        self.usb_button = tk.Button(
            self, text="Salin menyang USB", font=("Arial", 10, "bold"), 
            bg="#2563eb", fg="white", relief="flat",
            command=self.controller.handle_fetch_to_usb # Manggil controller
        )
        self.usb_button.place(x=860, y=20, width=140, height=40)
        # ------------------------------------------------

    # --- METHOD BARU: KANGGO NOTIFIKASI ING MAINPAGE ---
    def show_notification(self, message, color="blue", duration=4000):
        self.canvas.itemconfig(self.notification_id, text=message, fill=color)
        if self.notification_job:
            self.after_cancel(self.notification_job)
        if duration > 0:
            self.notification_job = self.after(duration, self.hide_notification)

    def hide_notification(self):
        self.canvas.itemconfig(self.notification_id, text="")
        self.notification_job = None
    # ----------------------------------------------------

# ... (kode LocationPage lan TypePage tetep padha) ...
class LocationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas( self, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame1")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        canvas.create_text(1024 // 2, 20.0, anchor="n", text="Pilih Asal Sampah", fill="#343434", font=("OpenSans Bold", 26 * -1))
        try:
            back_img = PhotoImage(file=relative_to_assets("back.png")).subsample(4, 4)
            back_btn = tk.Button(self, image=back_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: controller.show_frame(MainPage))
            back_btn.place(x=20, y=20, width=50, height=50)
            self.back_img = back_img
        except Exception:
            back_btn = tk.Button(self, text="Kembali", command=lambda: controller.show_frame(MainPage))
            back_btn.place(x=20, y=20, width=50, height=50)
        
        button_width, button_height, col_gap, row_gap = 306.0, 100.0, 40.0, 24.0
        margin_x = (1024.0 - (3 * button_width + 2 * col_gap)) / 2
        margin_y = 90.0
        configs = []
        locations = ["KPFT", "DTNTF", "DTETI", "DTMI", "DTK", "DTAP", "DTGD", "DTSL", "DTGL"]
        for i in range(9):
            row, col = i // 3, i % 3
            x, y = margin_x + col * (button_width + col_gap), margin_y + row * (button_height + row_gap)
            configs.append({"asset": f"button_{i+1}.png", "x": x, "y": y, "location": locations[i], "code": i+1})
        
        x_ltm, y_ltm = margin_x + (button_width + col_gap), margin_y + 3 * (button_height + row_gap)
        configs.append({"asset": "button_10.png", "x": x_ltm, "y": y_ltm, "location": "LTM", "code": 10})
        
        self.button_images = []
        for cfg in configs:
            img = PhotoImage(file=relative_to_assets(cfg["asset"]))
            btn = tk.Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda c=cfg["code"], n=cfg["location"]: controller.set_location_and_next(c, n))
            btn.place(x=cfg["x"], y=cfg["y"], width=button_width, height=button_height)
            self.button_images.append(img)

class TypePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = tk.Canvas(self, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.canvas = canvas
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame2")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        self.title_text_id = canvas.create_text(1024 // 2, 20.0, anchor="n", text="", fill="#343434", font=("OpenSans Bold", 26 * -1))
        
        try:
            back_img = PhotoImage(file=relative_to_assets("back.png")).subsample(4, 4)
            back_btn = tk.Button(self, image=back_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: controller.show_frame(LocationPage))
            back_btn.place(x=20, y=20, width=50, height=50)
            self.back_img = back_img
        except Exception:
            back_btn = tk.Button(self, text="Kembali", command=lambda: controller.show_frame(LocationPage))
            back_btn.place(x=20, y=20, width=50, height=50)
            
        button_width, button_height, x_gap, y_gap = 480.0, 230.0, 40.0, 40.0
        total_width, total_height = 2 * button_width + x_gap, 2 * button_height + y_gap
        margin_x, margin_y = (1024.0 - total_width) / 2, (600.0 - total_height) / 2 + 30
        x1, x2, y1, y2 = margin_x, margin_x + button_width + x_gap, margin_y, margin_y + button_height + y_gap
        
        configs = [
            {"asset": "button_1.png", "x": x1, "y": y1, "type": "Sapuan", "code": 1},
            {"asset": "button_2.png", "x": x2, "y": y1, "type": "Anorganik Kering/Rosok", "code": 2},
            {"asset": "button_3.png", "x": x1, "y": y2, "type": "Residu", "code": 3},
            {"asset": "button_4.png", "x": x2, "y": y2, "type": "Sisa Makanan", "code": 4},
        ]
        self.button_images = []
        for cfg in configs:
            img = PhotoImage(file=relative_to_assets(cfg["asset"]))
            btn = tk.Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda c=cfg["code"], n=cfg["type"]: controller.set_type_and_next(c, n))
            btn.place(x=cfg["x"], y=cfg["y"], width=button_width, height=button_height)
            self.button_images.append(img)
            
    def update_display(self):
        data = self.controller.model.get_trash_data()
        flow_name = self.controller.model.get_flow_name(data.get("flow", ""))
        self.canvas.itemconfig(self.title_text_id, text=f"Pilih Jenis Sampah ({flow_name})")

import tkinter as tk
from pathlib import Path
from tkinter import PhotoImage

class WeighPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = tk.Canvas(self, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.canvas = canvas
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame3")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # --- Latar belakang dan label ---
        canvas.create_rectangle(30.0, 30.0, 994.0, 430.0, fill="#BEBEBE", outline="")
        label_x, colon_x, value_x, y_gap, start_y = 110, 500, 520, 60, 60
        texts = ["Tempat", "Jenis", "Kantong", "Bobot Kantong (kg)", "Total Bobot (kg)"]
        self.labels = {}
        for i, text in enumerate(texts):
            canvas.create_text(label_x, start_y + i*y_gap, anchor="nw", text=text, fill="#343434", font=("OpenSans Bold", 22, "bold"))
            canvas.create_text(colon_x, start_y + i*y_gap, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
            self.labels[text] = canvas.create_text(value_x, start_y + i*y_gap, anchor="nw", text="", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # --- Tombol Horizontal (Timbang, Selesai) ---
        button_configs = [
            {"asset": "button_1.png", "text": "Timbang", "command": self.controller.handle_weigh},
            {"asset": "button_3.png", "text": "Selesai", "command": self.controller.handle_finish}
        ]
        button_width, button_height, button_gap = 180.0, 99.0, 60.0
        total_width = len(button_configs) * button_width + (len(button_configs) - 1) * button_gap
        start_x, y_pos = (1024.0 - total_width) / 2, 470.0
        self.button_images = []
        for i, config in enumerate(button_configs):
            x = start_x + i * (button_width + button_gap)
            try:
                img = PhotoImage(file=relative_to_assets(config["asset"]))
                btn = tk.Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat", command=config["command"])
                btn.place(x=x, y=y_pos, width=button_width, height=button_height)
                self.button_images.append(img)
            except Exception:
                btn = tk.Button(self, text=config["text"], command=config["command"])
                btn.place(x=x, y=y_pos, width=button_width, height=button_height)
        
        # --- Tombol Vertikal (Undo, Restart, Tare) ---
        x_center = 974
        
        # Tombol paling atas: Undo
        try:
            undo_icon = PhotoImage(file=relative_to_assets("undo.png")).subsample(5, 5)
            # Menambahkan teks dan opsi compound
            undo_btn = tk.Button(
                self, 
                image=undo_icon, 
                text="Undo", 
                compound=tk.TOP, # Menempatkan gambar di atas teks
                font=("OpenSans", 10),
                fg="#343434",
                borderwidth=0, 
                highlightthickness=0, 
                relief="flat", 
                command=self.controller.handle_undo
            )
            undo_btn.place(x=x_center - 35, y=30, width=70, height=65) # Lebar dan tinggi disesuaikan
            self.undo_icon = undo_icon
        except:
            pass

        # Tombol tengah: Restart
        try:
            restart_icon = PhotoImage(file=relative_to_assets("restart.png")).subsample(5, 5)
            # Menambahkan teks dan opsi compound
            restart_btn = tk.Button(
                self, 
                image=restart_icon, 
                text="Restart", 
                compound=tk.TOP, # Menempatkan gambar di atas teks
                font=("OpenSans", 10),
                fg="#343434",
                borderwidth=0, 
                highlightthickness=0, 
                relief="flat", 
                command=self.controller.handle_reset
            )
            restart_btn.place(x=x_center - 35, y=105, width=70, height=65) # Posisi Y diubah
            self.restart_icon = restart_icon
        except:
            pass
        
        # Tombol bawah: Tare (button_5.png)
        try:
            tare_img = PhotoImage(file=relative_to_assets("button_5.png"))
            tare_btn = tk.Button(self, image=tare_img, borderwidth=0, highlightthickness=0, relief="flat", command=self.controller.handle_tare)
            tare_btn.place(x=x_center - (180.0/2), y=180, width=180.0, height=99.0) # Posisi Y diubah
            self.button_images.append(tare_img)
        except Exception:
            tare_btn = tk.Button(self, text="Tare", command=self.controller.handle_tare)
            tare_btn.place(x=x_center - (180.0/2), y=180, width=180.0, height=99.0)
        
        # --- Tombol Status Server ---
        self.status_btn = tk.Label(self, text="?", bg="white")
        self.status_btn.place(x=20, y=20, width=30, height=30)
        try:
            self.online_icon = PhotoImage(file=relative_to_assets("online.png")).subsample(6, 6)
            self.offline_icon = PhotoImage(file=relative_to_assets("offline.png")).subsample(6, 6)
            self.status_btn.config(image=self.offline_icon)
        except Exception:
            pass
        
        self.auto_update_job = None
        self.status_update_job = None
        
    def start_auto_update(self):
        self.stop_auto_update()
        self.auto_update()
        self.update_server_status()
    
    def stop_auto_update(self):
        if self.auto_update_job: self.after_cancel(self.auto_update_job)
        if self.status_update_job: self.after_cancel(self.status_update_job)
        self.auto_update_job, self.status_update_job = None, None
        
    def auto_update(self):
        self.controller.model.update_weight()
        self.update_display()
        self.auto_update_job = self.after(100, self.auto_update)

    def update_server_status(self):
        from model import is_server_online
        if is_server_online(): self.status_btn.config(image=self.online_icon)
        else: self.status_btn.config(image=self.offline_icon)
        self.status_update_job = self.after(2000, self.update_server_status)
    
    def update_display(self):
        data = self.controller.model.get_trash_data()
        self.canvas.itemconfig(self.labels["Tempat"], text=self.controller.model.get_location_name(data.get("source", "")))
        type_name = self.controller.model.get_type_name(data.get("type", ""))
        flow_name = self.controller.model.get_flow_name(data.get("flow", ""))
        self.canvas.itemconfig(self.labels["Jenis"], text=f"{type_name} ({flow_name})")
        self.canvas.itemconfig(self.labels["Kantong"], text=str(data.get("bag_count", 1)))
        self.canvas.itemconfig(self.labels["Bobot Kantong (kg)"], text=str(round(self.controller.model.beratSementara, 2)))
        self.canvas.itemconfig(self.labels["Total Bobot (kg)"], text=str(round(data.get("weight", 0), 2)))

