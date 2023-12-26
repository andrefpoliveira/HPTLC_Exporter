import customtkinter as ctk
from functools import partial

from src.general.utils.utils import resource_path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SampleWindow(ctk.CTk):

    def __init__(self, main_app, previous_values, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.id = None
        self.sample_name = ""

        if previous_values:
            self.id = previous_values[0]
            self.sample_name = previous_values[1]

        self.main_app = main_app

        self.WIDTH = 300
        self.HEIGHT = 100

        self.title("HPTLC - New Sample")
        self.iconbitmap(resource_path("assets/favicon.ico"))
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        container = ctk.CTkFrame(self, width=self.WIDTH, height=self.HEIGHT)
        container.place(x=0, y=0)

        sample_label = ctk.CTkLabel(container, text="Sample Name:", font=("Arial", 14))
        sample_label.place(x=10, y=5)

        self.sample_entry = ctk.CTkEntry(container, width=280, height=26, border_width=1, border_color="white", placeholder_text="Sample 1")
        if self.sample_name:
            self.sample_entry.insert(0, self.sample_name)
        self.sample_entry.place(x=10, y=35)

        self.save_button = ctk.CTkButton(container, text="Save", width=100, height=20, fg_color="#2663c4", hover_color="#0048ba", command=self.send_information, state="disabled")
        self.save_button.place(x=100, y=self.HEIGHT-30)

        self.after(100, self.check_fields)

    def check_fields(self):
        self.sample_name = self.sample_entry.get().strip()

        if self.sample_name:
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")

        self.after(100, self.check_fields)

    def send_information(self):
        self.main_app.save_sample(self, self.sample_name, self.id)


