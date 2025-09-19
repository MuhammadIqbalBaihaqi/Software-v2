import tkinter as tk
from tkinter import ttk
from pathlib import Path
from views import MainPage, LocationPage, TypePage, WeighPage
from model import TrashDataModel  # pastikan model.py di path yang sama

# Import PhotoImage
from tkinter import PhotoImage

class TrashSortingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.model = TrashDataModel()  # Model integrasi

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

    def show_frame(self, frame_class):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[frame_class]
        # Update display jika frame punya method update_display
        if hasattr(frame, 'update_display'):
            frame.update_display()
        frame.grid()
        frame.tkraise()
        if frame_class == WeighPage and hasattr(frame, 'start_auto_update'):
            frame.start_auto_update()
    # Stop auto update jika bukan WeighPage
        elif hasattr(frame, 'stop_auto_update'):
            frame.stop_auto_update()

    # ---- Navigation logic ----
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
        updated_data = self.model.update_bag_data()
        # Update display pada WeighPage
        self.frames[WeighPage].update_display()

    def handle_finish(self):
        self.model.send_all_data()
        print("udah")
        self.model.reset_data()
        self.show_frame(MainPage)

    def handle_reset(self):
        self.model.reset_data()
        #self.show_frame(MainPage)
        self.frames[WeighPage].update_display()
    def handle_undo(self):
        self.model.undo_bag_data()
        # Update display pada WeighPage
        self.frames[WeighPage].update_display() 

    def handle_tare(self):
        self.model.tare()
        # Update display pada WeighPage
        self.frames[WeighPage].update_display()


if __name__ == "__main__":
    app = TrashSortingApp()
    app.title("Timbangan Sampah Digital - MVC Integrated")
    app.geometry("1024x600")
    app.resizable(False, False)
    app.attributes('-fullscreen', True)
    # app.overrideredirect(True)
    app.mainloop()
