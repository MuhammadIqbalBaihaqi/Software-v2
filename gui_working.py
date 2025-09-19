import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Tambahkan import untuk PhotoImage
from tkinter import PhotoImage

class WorkingTrashApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Data yang akan dibagikan antar halaman
        self.trash_data = {
            "source": 0,
            "type": 0,
            "bag_count": 0,
            "weight": 0,
            "current_weight": 0,
            "category": "",
            "source_name": "",
            "type_name": ""
        }
        
        # Setup container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Buat semua frame
        for FrameClass in (MainPage, LocationPage, TypePage, WeighPage):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # PENTING: Mulai dari MainPage
        self.show_frame(MainPage)
    
    def show_frame(self, frame_class):
        # Sembunyikan semua frame dulu
        for frame in self.frames.values():
            frame.grid_remove()
        
        # Tampilkan frame yang dipilih
        frame = self.frames[frame_class]
        frame.grid()
        frame.tkraise()
    
    def next_page(self, current_page):
        if current_page == MainPage:
            self.show_frame(LocationPage)
        elif current_page == LocationPage:
            self.show_frame(TypePage)
        elif current_page == TypePage:
            self.show_frame(WeighPage)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Setup canvas
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Gunakan asset yang sama dengan gui.py
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame0")
        
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Header background image (sama dengan gui.py)
        try:
            image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.create_image(640.0, 61.0, image=image_image_1)
            # Simpan referensi gambar agar tidak dihapus oleh garbage collector
            self.image_1 = image_image_1
        except:
            # Fallback jika gambar tidak ditemukan
            canvas.create_rectangle(0, 0, 1280, 120, fill="#1e3a8a", outline="")
            canvas.create_oval(50, 30, 90, 70, fill="white", outline="")
            canvas.create_text(70, 50, text="UGM", fill="#1e3a8a", font=("Arial", 12, "bold"))
            canvas.create_text(120, 40, anchor="nw", text="Timbangan Sampah Digital Berbasis IoT", 
                              fill="white", font=("Arial", 24, "bold"))
            canvas.create_text(120, 70, anchor="nw", text="Fakultas Teknik", 
                              fill="white", font=("Arial", 18))
            canvas.create_text(120, 95, anchor="nw", text="Universitas Gadjah Mada", 
                              fill="white", font=("Arial", 18))
        
        # Title (sama dengan gui.py)
        canvas.create_text(464.0, 171.0, anchor="nw", text="Pilih Kategori Sampah", 
                          fill="#343434", font=("OpenSans Bold", 32 * -1))
        
        # Button 1 - Sampah Masuk (gunakan asset yang sama)
        try:
            button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
            button_1 = tk.Button(
                self,
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                command=lambda: self.go_to_location(controller, "masuk")
            )
            button_1.place(x=139.0, y=246.0, width=468.0, height=400.0)
            # Simpan referensi gambar
            self.button_image_1 = button_image_1
        except:
            # Fallback jika gambar tidak ditemukan
            button_1 = tk.Button(
                self,
                text="Sampah\nMasuk",
                font=("Arial", 24, "bold"),
                bg="#10b981",
                fg="white",
                relief="flat",
                command=lambda: self.go_to_location(controller, "masuk")
            )
            button_1.place(x=139, y=246, width=468, height=400)
        
        # Button 2 - Sampah Keluar (gunakan asset yang sama)
        try:
            button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
            button_2 = tk.Button(
                self,
                image=button_image_2,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                command=lambda: self.go_to_location(controller, "keluar")
            )
            button_2.place(x=674.0, y=246.0, width=468.0, height=400.0)
            # Simpan referensi gambar
            self.button_image_2 = button_image_2
        except:
            # Fallback jika gambar tidak ditemukan
            button_2 = tk.Button(
                self,
                text="Sampah\nKeluar",
                font=("Arial", 24, "bold"),
                bg="#3b82f6",
                fg="white",
                relief="flat",
                command=lambda: self.go_to_location(controller, "keluar")
            )
            button_2.place(x=674, y=246, width=468, height=400)
    
    def go_to_location(self, controller, category):
        controller.trash_data["category"] = category
        controller.next_page(MainPage)

class LocationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Setup canvas
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Gunakan asset yang sama dengan gui1.py
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame1")
        
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Title (sama dengan gui1.py)
        canvas.create_text(498.0, 30.0, anchor="nw", text="Pilih Asal Sampah", 
                          fill="#343434", font=("OpenSans Bold", 32))
        
        # Location buttons (10 buttons) - gunakan asset yang sama dengan gui1.py
        locations = ["KPFT", "DTNTF", "DTETI", "DTMI", "DTK", "DTAP", "DTGD", "DTSL", "DTGL", "LTM"]
        
        # Button positions dan asset sesuai gui1.py
        button_configs = [
            # Row 1
            {"asset": "button_1.png", "x": 63.0, "y": 108.0, "width": 367.0315246582031, "height": 120.26593017578125, "location": "KPFT", "index": 1},
            {"asset": "button_2.png", "x": 456.4842529296875, "y": 108.0, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTNTF", "index": 2},
            {"asset": "button_3.png", "x": 849.968505859375, "y": 108.0, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTETI", "index": 3},
            # Row 2
            {"asset": "button_4.png", "x": 456.4842529296875, "y": 254.7186279296875, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTMI", "index": 4},
            {"asset": "button_5.png", "x": 849.968505859375, "y": 254.7186279296875, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTK", "index": 5},
            {"asset": "button_6.png", "x": 63.0, "y": 254.7186279296875, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTAP", "index": 6},
            # Row 3
            {"asset": "button_7.png", "x": 63.0, "y": 401.4372863769531, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTGD", "index": 7},
            {"asset": "button_8.png", "x": 456.4842529296875, "y": 401.4372863769531, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTSL", "index": 8},
            {"asset": "button_9.png", "x": 849.968505859375, "y": 401.4372863769531, "width": 367.0315246582031, "height": 120.26593017578125, "location": "DTGL", "index": 9},
            # Row 4 - LTM di tengah
            {"asset": "button_10.png", "x": 456.4842529296875, "y": 548.1559448242188, "width": 367.0315246582031, "height": 120.26593017578125, "location": "LTM", "index": 10}
        ]
        
        # Simpan referensi gambar
        self.button_images = []
        
        for config in button_configs:
            try:
                # Load asset gambar
                button_image = PhotoImage(file=relative_to_assets(config["asset"]))
                
                # Buat button dengan asset
                button = tk.Button(
                    self,
                    image=button_image,
                    borderwidth=0,
                    highlightthickness=0,
                    relief="flat",
                    command=lambda loc=config["location"], idx=config["index"]: self.set_location(controller, idx, loc)
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )
                
                # Simpan referensi gambar
                self.button_images.append(button_image)
                
            except Exception as e:
                # Fallback jika gambar tidak ditemukan
                print(f"Error loading {config['asset']}: {e}")
                button = tk.Button(
                    self,
                    text=config["location"],
                    font=("Arial", 18, "bold"),
                    bg="#3b82f6",
                    fg="white",
                    relief="flat",
                    command=lambda loc=config["location"], idx=config["index"]: self.set_location(controller, idx, loc)
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )

    def set_location(self, controller, location_code, location_name):
        controller.trash_data["source"] = location_code
        controller.trash_data["source_name"] = location_name
        controller.next_page(LocationPage)

class TypePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Setup canvas
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Gunakan asset yang sama dengan gui2.py
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame2")
        
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Title (sama dengan gui2.py)
        canvas.create_text(494.0, 44.0, anchor="nw", text="Pilih Jenis Sampah", 
                          fill="#343434", font=("OpenSans Bold", 32 * -1))
        
        # Type buttons (4 buttons) - gunakan asset yang sama dengan gui2.py
        types = ["Sapuan", "Anorganik Kering/Rosok", "Residu", "Sisa Makanan"]
        
        # Button positions dan asset sesuai gui2.py
        button_configs = [
            # Top-left button - Sapuan (Hijau)
            {"asset": "button_1.png", "x": 97.0, "y": 141.0, "width": 523.7931518554688, "height": 236.9420928955078, "type": "Sapuan", "index": 1},
            # Top-right button - Anorganik Kering/Rosok (Oranye)
            {"asset": "button_2.png", "x": 658.544189453125, "y": 141.0, "width": 523.7931518554688, "height": 236.9420928955078, "type": "Anorganik Kering/Rosok", "index": 2},
            # Bottom-left button - Residu (Merah)
            {"asset": "button_3.png", "x": 97.0, "y": 430.0, "width": 523.7931518554688, "height": 236.9420928955078, "type": "Residu", "index": 3},
            # Bottom-right button - Sisa Makanan (Abu-abu)
            {"asset": "button_4.png", "x": 658.544189453125, "y": 430.0578918457031, "width": 523.7931518554688, "height": 236.9420928955078, "type": "Sisa Makanan", "index": 4}
        ]
        
        # Simpan referensi gambar
        self.button_images = []
        
        for config in button_configs:
            try:
                # Load asset gambar
                button_image = PhotoImage(file=relative_to_assets(config["asset"]))
                
                # Buat button dengan asset
                button = tk.Button(
                    self,
                    image=button_image,
                    borderwidth=0,
                    highlightthickness=0,
                    relief="flat",
                    command=lambda type_idx=config["index"], type_name=config["type"]: self.set_type(controller, type_idx, type_name)
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )
                
                # Simpan referensi gambar
                self.button_images.append(button_image)
                
            except Exception as e:
                # Fallback jika gambar tidak ditemukan
                print(f"Error loading {config['asset']}: {e}")
                # Gunakan warna yang sesuai dengan asset asli
                colors = ["#10b981", "#f59e0b", "#ef4444", "#6b7280"]
                color = colors[config["index"] - 1]
                
                button = tk.Button(
                    self,
                    text=config["type"],
                    font=("Arial", 20, "bold"),
                    bg=color,
                    fg="white",
                    relief="flat",
                    command=lambda type_idx=config["index"], type_name=config["type"]: self.set_type(controller, type_idx, type_name)
                )
                button.place(
                    x=config["x"],
                    y=config["y"],
                    width=config["width"],
                    height=config["height"]
                )
        
    def set_type(self, controller, type_code, type_name):
        controller.trash_data["type"] = type_code
        controller.trash_data["type_name"] = type_name
        controller.next_page(TypePage)

class WeighPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Setup canvas
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Gunakan asset yang sama dengan gui3.py
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame3")
        
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        # Background rectangle (sama dengan gui3.py)
        canvas.create_rectangle(149.0, 50.0, 1131.0, 557.0, fill="#BEBEBE", outline="")
    
        # Display labels dengan posisi yang sama dengan gui3.py
        canvas.create_text(200, 87, anchor="nw", text="Tempat                             :", 
                          fill="#343434", font=("OpenSans Bold", 24, "bold"))
        self.loc_label = canvas.create_text(600.0, 87.0, anchor="nw", text="", 
                                          fill="#343434", font=("OpenSans Bold", 41 * -1))
        
        canvas.create_text(200, 180, anchor="nw", text="Jenis                               :", 
                          fill="#343434", font=("OpenSans Bold", 24, "bold"))
        self.type_label = canvas.create_text(600.0, 180.0, anchor="nw", text="", 
                                           fill="#343434", font=("OpenSans Bold", 41 * -1), width= 50000)
        
        canvas.create_text(200, 273, anchor="nw", text="Kantong Ke-                   :", 
                          fill="#343434", font=("OpenSans Bold", 24, "bold"))
        self.bag_label = canvas.create_text(600.0, 273.0, anchor="nw", text="1", 
                                          fill="#343434", font=("OpenSans Bold", 41 * -1))
        
        canvas.create_text(200, 366, anchor="nw", text="Bobot Kantong (kg)       :", 
                          fill="#343434", font=("OpenSans Bold", 24, "bold"))
        self.weight_label = canvas.create_text(600.0, 366.0, anchor="nw", text="0", 
                                            fill="#343434", font=("OpenSans Bold", 41 * -1))
        
        canvas.create_text(200, 459, anchor="nw", text="Total Bobot (kg)            :", 
                          fill="#343434", font=("OpenSans Bold", 24, "bold"))
        self.total_weight_label = canvas.create_text(600.0, 459.0, anchor="nw", text="0", 
                                                  fill="#343434", font=("OpenSans Bold", 41 * -1))
        
        # Action buttons dengan asset yang sama dengan gui3.py
        # Konfigurasi tombol agar rata dan ukuran sama
        button_width = 232.5
        button_height = 84.0
        button_gap = 19
        start_x = 149.0
        y_pos = 587.94

        button_configs = [
            # Timbang button (Hijau)
            {"asset": "button_1.png", "text": "Timbang", "command": lambda: self.timbang(controller)},
            # Ulangi Proses button (Oranye)
            {"asset": "button_2.png", "text": "Ulangi\nProses", "command": lambda: self.ulangi_proses(controller)},
            # Undo Button (abu-abu)
            {"asset": "button_4.png", "text": "Undo", "command": lambda: self.ulangi_proses(controller)},
            # Selesai button (Merah)
            {"asset": "button_3.png", "text": "Selesai", "command": lambda: self.selesai(controller)}
        ]

        # Hitung posisi x setiap tombol agar rata
        for i, config in enumerate(button_configs):
            config["x"] = start_x + i * (button_width + button_gap)
            config["y"] = y_pos
            config["width"] = button_width
            config["height"] = button_height
        # Simpan referensi gambar
        self.button_images = []
        
        for config in button_configs:
            try:
                # Load asset gambar
                button_image = PhotoImage(file=relative_to_assets(config["asset"]))
                
                # Buat button dengan asset
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
                
                # Simpan referensi gambar
                self.button_images.append(button_image)
                
            except Exception as e:
                # Fallback jika gambar tidak ditemukan
                print(f"Error loading {config['asset']}: {e}")
                # Gunakan warna yang sesuai dengan asset asli
                colors = ["#10b981", "#f59e0b", "#ef4444"]
                color = colors[len(self.button_images)]
                
                button = tk.Button(
                    self,
                    text=config["text"],
                    font=("Arial", 18, "bold"),
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

        # Update display
        self.update_display(controller)
    
    def update_display(self, controller):
        canvas = self.winfo_children()[0]
        canvas.itemconfig(self.loc_label, text=controller.trash_data.get("source_name", ""))
        canvas.itemconfig(self.type_label, text=controller.trash_data.get("type_name", ""))
        canvas.itemconfig(self.bag_label, text=str(controller.trash_data.get("bag_count", 1)))
        canvas.itemconfig(self.weight_label, text=str(controller.trash_data.get("current_weight", 0)))
        canvas.itemconfig(self.total_weight_label, text=str(controller.trash_data.get("weight", 0)))
    
    def timbang(self, controller):
        import random
        weight = random.uniform(5.0, 15.0)
        controller.trash_data["current_weight"] = round(weight, 1)
        controller.trash_data["bag_count"] += 1
        controller.trash_data["weight"] += controller.trash_data["current_weight"]
        self.update_display(controller)
    
    def ulangi_proses(self, controller):
        controller.trash_data["bag_count"] = 0
        controller.trash_data["weight"] = 0
        controller.trash_data["current_weight"] = 0
        controller.show_frame(MainPage)
    
    def selesai(self, controller):
        print("Data dikirim:", controller.trash_data)
        controller.trash_data["bag_count"] = 0
        controller.trash_data["weight"] = 0
        controller.trash_data["current_weight"] = 0
        controller.show_frame(MainPage)

# Main application
if __name__ == "__main__":
    app = WorkingTrashApp()
    app.title("Timbangan Sampah Digital - Working Version")
    app.geometry("1280x720")
    app.resizable(False, False)
    app.mainloop()
