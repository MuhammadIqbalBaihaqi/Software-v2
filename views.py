import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
import requests


# endpoint khusus untuk health check
url_health = "http://10.46.7.51:8000/api/connection/status"
def is_server_online(url_health, timeout=2):
    try:
        response = requests.get(url_health, timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
class MainPage(tk.Frame):
    def __init__(self, parent, controller):

        # Inisialisasi frame utama
        tk.Frame.__init__(self, parent)

        # Set up canvas and its position
        canvas = tk.Canvas(
            self, 
            bg="#FFFFFF", 
            height=600, 
            width=1024, 
            bd=0, 
            highlightthickness=0, 
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Load assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame0")

        # Function to resolve relative paths
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Header background image
        try:
            image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.create_image(512.0, 50.0, image=image_image_1)
            self.image_1 = image_image_1
        except:
            canvas.create_rectangle(0, 0, 1024, 100, fill="#1e3a8a", outline="")
            canvas.create_oval(30, 20, 70, 60, fill="white", outline="")
            canvas.create_text(50, 40, text="UGM", fill="#1e3a8a", font=("Arial", 12, "bold"))
            canvas.create_text(90, 30, anchor="nw", text="Timbangan Sampah Digital Berbasis IoT", fill="white", font=("Arial", 18, "bold"))
            canvas.create_text(90, 60, anchor="nw", text="Fakultas Teknik", fill="white", font=("Arial", 14))
            canvas.create_text(90, 80, anchor="nw", text="Universitas Gadjah Mada", fill="white", font=("Arial", 14))

        # Main title text
        canvas.create_text(
            1024 // 2,
            130.0,
            anchor="n",
            text="Pilih Kategori Sampah",
            fill="#343434",
            font=("OpenSans Bold", 26 * -1)
        )

        # Button Sampah Masuk
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: controller.set_category_and_next(0)
        )
        button_1.place(
            x=110.0,
            y=200.0,
            width=350.0,
            height=300.0
        )

        # Button Sampah Keluar
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: controller.set_category_and_next(1)
        )
        button_2.place(
            x=564.0,
            y=200.0,
            width=350.0,
            height=300.0
        )

class LocationPage(tk.Frame):
    def __init__(self, parent, controller):

        # Inisialisasi frame
        tk.Frame.__init__(self, parent)

        # Set up canvas and its position
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF", 
            height=600,
            width=1024, bd=0, 
            highlightthickness=0, 
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Load assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame1")

        # Function to resolve relative paths
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Title text
        canvas.create_text(
            1024 // 2,
            20.0,
            anchor="n",
            text="Pilih Asal Sampah",
            fill="#343434",
            font=("OpenSans Bold", 26 * -1)
        )

        # Tombol Back di pojok kiri atas
        try:
            back_img = PhotoImage(file=relative_to_assets("back.png")).subsample(4, 4)
            back_btn = tk.Button(self, image=back_img, borderwidth=0, highlightthickness=0, relief="flat",
                                command=lambda: controller.show_frame(MainPage))
            back_btn.place(x=20, y=20, width=50, height=50)
            self.back_img = back_img
        except Exception as e:
            print(f"Error loading back.png: {e}")
            back_btn = tk.Button(self, text="Kembali", font=("Arial", 10, "bold"), bg="#e5e7eb", fg="#1e3a8a", relief="flat",
                                command=lambda: controller.show_frame(MainPage))
            back_btn.place(x=20, y=20, width=50, height=50)
        # Button configurations (10 tombol, ukuran 306x100 pixel, penempatan absolut)
        # Ukuran tombol kembali ke 306x100 pixel, posisi y disesuaikan agar proporsional
        button_width = 306.0
        button_height = 100.0
        col_gap = 40.0
        row_gap = 24.0
        margin_x = (1024.0 - (3 * button_width + 2 * col_gap)) / 2
        margin_y = 90.0
        configs = []
        # 3 kolom x 3 baris untuk 9 tombol pertama
        for i in range(9):
            row = i // 3
            col = i % 3
            x = margin_x + col * (button_width + col_gap)
            y = margin_y + row * (button_height + row_gap)
            configs.append({
                "asset": f"button_{i+1}.png",
                "x": x,
                "y": y,
                "location": ["KPFT", "DTNTF", "DTETI", "DTMI", "DTK", "DTAP", "DTGD", "DTSL", "DTGL"][i],
                "code": i+1
            })
        # Tombol ke-10 (LTM) di tengah bawah
        x_ltm = margin_x + (button_width + col_gap)
        y_ltm = margin_y + 3 * (button_height + row_gap)
        configs.append({
            "asset": "button_10.png",
            "x": x_ltm,
            "y": y_ltm,
            "location": "LTM",
            "code": 10
        })

        # Create buttons with absolute placement and fixed size
        self.button_images = []
        for cfg in configs:
            img = PhotoImage(file=relative_to_assets(cfg["asset"]))
            btn = tk.Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat",
                            command=lambda c=cfg["code"], n=cfg["location"]: controller.set_location_and_next(c, n))
            btn.place(x=cfg["x"], y=cfg["y"], width=button_width, height=button_height)
            self.button_images.append(img)

class TypePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = tk.Canvas(
            self, 
            bg="#FFFFFF", 
            height=600, 
            width=1024, 
            bd=0, 
            highlightthickness=0, 
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        self.canvas = canvas

        # Load assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame2")
        
        # Function to resolve relative paths
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        # Title text (simpan ID)
        self.title_text_id = canvas.create_text(
            1024 // 2,
            20.0,
            anchor="n",
            text="",  # kosong dulu
            fill="#343434",
            font=("OpenSans Bold", 26 * -1)
        )

        # Tombol Back di pojok kiri atas
        try:
            back_img = PhotoImage(file=relative_to_assets("back.png")).subsample(4, 4)
            back_btn = tk.Button(self, image=back_img, borderwidth=0, highlightthickness=0, relief="flat",
                                command=lambda: controller.show_frame(LocationPage))
            back_btn.place(x=20, y=20, width=50, height=50)
            self.back_img = back_img
        except Exception as e:
            print(f"Error loading back.png: {e}")
            back_btn = tk.Button(self, text="Kembali", font=("Arial", 10, "bold"), bg="#e5e7eb", fg="#1e3a8a", relief="flat",
                                command=lambda: controller.show_frame(LocationPage))
            back_btn.place(x=20, y=20, width=50, height=50)
        # Button configurations (2 kolom x 2 baris)
        # Ukuran tombol diubah menjadi 440x200 pixel, posisi disesuaikan agar proporsional
        # Button configurations (2 kolom x 2 baris), margin proporsional
        button_width = 480.0
        button_height = 230.0
        x_gap = 40.0
        y_gap = 40.0
        total_width = 2 * button_width + x_gap
        total_height = 2 * button_height + y_gap
        margin_x = (1024.0 - total_width) / 2
        margin_y = (600.0 - total_height) / 2 + 30
        x1 = margin_x
        x2 = x1 + button_width + x_gap
        y1 = margin_y
        y2 = y1 + button_height + y_gap
        configs = [
            {"asset": "button_1.png", "x": x1, "y": y1, "type": "Sapuan", "code": 1},
            {"asset": "button_2.png", "x": x2, "y": y1, "type": "Anorganik Kering/Rosok", "code": 2},
            {"asset": "button_3.png", "x": x1, "y": y2, "type": "Residu", "code": 3},
            {"asset": "button_4.png", "x": x2, "y": y2, "type": "Sisa Makanan", "code": 4},
        ]
        self.button_images = []

        # Create buttons dynamically based on configurations
        for cfg in configs:
            img = PhotoImage(file=relative_to_assets(cfg["asset"]))
            btn = tk.Button(self, image=img, borderwidth=0, highlightthickness=0, relief="flat",
                command=lambda c=cfg["code"], n=cfg["type"]: controller.set_type_and_next(c, n))
            btn.place(x=cfg["x"], y=cfg["y"], width=button_width, height=button_height)
            self.button_images.append(img)

    def update_display(self):
        data = self.controller.model.get_trash_data()
        flow_name = self.controller.model.get_flow_name(data.get("flow", ""))
        self.canvas.itemconfig(self.title_text_id, text=f"Pilih Jenis Sampah ({flow_name})")
        # ...tambahkan update lain jika perlu...

class WeighPage(tk.Frame):
    def __init__(self, parent, controller):

        # Inisialisasi frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Set up canvas and it's position
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=600,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Load assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame3")

        # Function to resolve relative paths
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Create UI elements
        # Rectangle background (diperlebar agar tulisan panjang muat)
        canvas.create_rectangle(30.0, 30.0, 994.0, 430.0, fill="#BEBEBE", outline="")

        # Text elements
        label_x = 110
        colon_x = 500
        value_x = 520
        y_gap = 60
        start_y = 60

        # Lokasi
        canvas.create_text(label_x, start_y, anchor="nw", text="Tempat", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        canvas.create_text(colon_x, start_y, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        self.loc_label = canvas.create_text(value_x, start_y, anchor="nw", text="", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # Jenis
        canvas.create_text(label_x, start_y + y_gap, anchor="nw", text="Jenis", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        canvas.create_text(colon_x, start_y + y_gap, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        self.type_label = canvas.create_text(value_x, start_y + y_gap, anchor="nw", text="", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # Kantong
        canvas.create_text(label_x, start_y + 2*y_gap, anchor="nw", text="Kantong", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        canvas.create_text(colon_x, start_y + 2*y_gap, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        self.bag_label = canvas.create_text(value_x, start_y + 2*y_gap, anchor="nw", text="1", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # Bobot Kantong (kg)
        canvas.create_text(label_x, start_y + 3*y_gap, anchor="nw", text="Bobot Kantong (kg)", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        canvas.create_text(colon_x, start_y + 3*y_gap, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        self.weight_label = canvas.create_text(value_x, start_y + 3*y_gap, anchor="nw", text="0", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # Total Bobot (kg)
        canvas.create_text(label_x, start_y + 4*y_gap, anchor="nw", text="Total Bobot (kg)", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        canvas.create_text(colon_x, start_y + 4*y_gap, anchor="nw", text=":", fill="#343434", font=("OpenSans Bold", 22, "bold"))
        self.total_weight_label = canvas.create_text(value_x, start_y + 4*y_gap, anchor="nw", text="0", fill="#343434", font=("OpenSans Bold", 22, "bold"))

        # Button configurations
        button_width = 160.0
        button_height = 60.0
        button_gap = 20
        start_x = 120.0
        y_pos = 480.0

        # Button utama di bawah (hanya Timbang, Tare, Selesai)
        button_configs = [
            {"asset": "button_1.png", "text": "Timbang", "command": lambda: self.handle_weigh()},
            {"asset": "button_5.png", "text": "Tare", "command": lambda: self.handle_tare() if hasattr(self, 'handle_tare') else None},
            {"asset": "button_3.png", "text": "Selesai", "command": lambda: self.handle_finish()}
        ]

        button_width = 180.0
        button_height = 99.0
        button_gap = 60.0  # Lebih lebar agar seimbang
        total_width = len(button_configs) * button_width + (len(button_configs) - 1) * button_gap
        start_x = (1024.0 - total_width) / 2
        y_pos = 470.0

        self.button_images = []
        for i, config in enumerate(button_configs):
            config["x"] = start_x + i * (button_width + button_gap)
            config["y"] = y_pos
            config["width"] = button_width
            config["height"] = button_height
            try:
                button_image = PhotoImage(file=relative_to_assets(config["asset"]))
                button = tk.Button(
                    self,
                    image=button_image,
                    borderwidth=0,
                    highlightthickness=0,
                    relief="flat",
                    command=config["command"]
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )
                self.button_images.append(button_image)
            except Exception as e:
                print(f"Error loading {config['asset']}: {e}")
                colors = ["#10b981", "#f59e0b", "#ef4444"]
                color = colors[i]
                button = tk.Button(
                    self,
                    text=config["text"],
                    font=("Arial", 14, "bold"),
                    bg=color,
                    fg="white",
                    relief="flat",
                    command=config["command"]
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )

        # Tombol restart dan undo di pojok kanan atas
        try:
            restart_icon = PhotoImage(file=relative_to_assets("restart.png")).subsample(5, 5)
            restart_btn = tk.Button(self, image=restart_icon, borderwidth=0, highlightthickness=0, relief="flat",
                                    command=lambda: self.handle_reset())
            restart_btn.place(x=1024-120, y=30, width=40, height=40)
            self.restart_icon = restart_icon
            canvas.create_text(1024-100, 75, text="Restart", font=("Arial", 10), fill="#343434")
        except Exception as e:
            print(f"Error loading restart.png: {e}")
            restart_btn = tk.Button(self, text="Restart", font=("Arial", 10), bg="#e5e7eb", fg="#1e3a8a", relief="flat",
                                    command=lambda: self.handle_reset())
            restart_btn.place(x=1024-120, y=30, width=40, height=40)
            canvas.create_text(1024-100, 75, text="Restart", font=("Arial", 10), fill="#343434")

        try:
            undo_icon = PhotoImage(file=relative_to_assets("undo.png")).subsample(5, 5)
            undo_btn = tk.Button(self, image=undo_icon, borderwidth=0, highlightthickness=0, relief="flat",
                                 command=lambda: self.handle_undo())
            undo_btn.place(x=1024-65, y=30, width=40, height=40)
            self.undo_icon = undo_icon
            canvas.create_text(1024-45, 75, text="Undo", font=("Arial", 10), fill="#343434")
        except Exception as e:
            print(f"Error loading undo.png: {e}")
            undo_btn = tk.Button(self, text="Undo", font=("Arial", 10), bg="#e5e7eb", fg="#1e3a8a", relief="flat",
                                 command=lambda: self.handle_undo())
            undo_btn.place(x=1024-65, y=30, width=40, height=40)
            canvas.create_text(1024-45, 75, text="Undo", font=("Arial", 10), fill="#343434")

        self.canvas = canvas
        self.auto_update_job = None
        # >>>> TAMBAHKAN BAGIAN STATUS ICON DI SINI <<<<
        self.auto_update_job = None
        self.status_update_job = None  # buat status server

        try:
            self.online_icon = PhotoImage(file=relative_to_assets("online.png")).subsample(6, 6)
            self.offline_icon = PhotoImage(file=relative_to_assets("offline.png")).subsample(6, 6)

            # tombol status (pojok kiri atas)
            self.status_btn = tk.Label(self, image=self.offline_icon, bg="white")
            self.status_btn.place(x=20, y=20, width=30, height=30)

        except Exception as e:
            print(f"Error loading status icons: {e}")
            self.status_btn = tk.Label(self, text="?", bg="white")
            self.status_btn.place(x=20, y=20, width=30, height=30)

        self.canvas = canvas
    def start_auto_update(self):
        # stop dulu biar ga double loop
        if self.auto_update_job is not None:
            self.after_cancel(self.auto_update_job)
        if self.status_update_job is not None:
            self.after_cancel(self.status_update_job)

        self.auto_update()
        self.update_server_status()

        print("Auto update + server status started.")
    
    def stop_auto_update(self):
        if self.auto_update_job is not None:
            self.after_cancel(self.auto_update_job)
            self.auto_update_job = None
        if self.status_update_job is not None:
            self.after_cancel(self.status_update_job)
            self.status_update_job = None
    
    def auto_update(self):
        self.controller.model.update_weight()
        self.update_display()
        self.auto_update_job = self.after(100, self.auto_update)  # 100 ms

    def update_server_status(self):
        #from model import is_server_online  # pastikan import benar
        if is_server_online("http://10.46.7.51:8000/api/connection/status"):
            self.status_btn.config(image=self.online_icon)
        else:
            self.status_btn.config(image=self.offline_icon)
        # cek ulang tiap 2 detik
        self.status_update_job = self.after(2000, self.update_server_status)    

    def update_display(self):
        data = self.controller.model.get_trash_data()
        berat = self.controller.model.beratSementara
        list_berat = self.controller.model.listBerat
        self.canvas.itemconfig(self.loc_label, text=self.controller.model.get_location_name(data.get("source", "")))
        type_name = self.controller.model.get_type_name(data.get("type", ""))
        flow_name = self.controller.model.get_flow_name(data.get("flow", ""))
        self.canvas.itemconfig(self.type_label, text=f"{type_name} ({flow_name})")
        self.canvas.itemconfig(self.bag_label, text=str(data.get("bag_count", 1)))
        self.canvas.itemconfig(self.weight_label, text=str(round(berat, 2)))
        self.canvas.itemconfig(self.total_weight_label, text=str(round(data.get("weight", 0), 2)))

    def handle_weigh(self):
        self.controller.handle_weigh()

    def handle_finish(self):
        self.stop_auto_update()
        self.controller.handle_finish()

    def handle_reset(self):
        self.controller.handle_reset()

    def handle_undo(self):
        self.controller.handle_undo()
    
    def handle_tare(self):
        self.controller.handle_tare()
