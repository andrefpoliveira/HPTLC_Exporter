import importlib, requests, webbrowser
from sys import exit

import tkinter as tk
import customtkinter as ctk

from src.general.gui.main_page import MainPage
from src.general.utils.utils import resource_path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VERSION = "1.2.0"

class App(ctk.CTk):

    def __init__(self, projects_path, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.WIDTH = 800
        self.HEIGHT = 500

        self.projects_path = projects_path

        self.title(f"HPTLC Excel Generator - v{VERSION}")
        self.iconbitmap(resource_path("assets/favicon.ico"))
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = ctk.CTkFrame(self, width=self.WIDTH, height=self.HEIGHT)
        self.container.place(x=0, y=0)

        self.frame_stack = [
            MainPage(parent=self.container, controller=self, width=self.WIDTH, height=self.HEIGHT)
        ]

        self.show_frame()
        self.check_version()

    def get_latest_version(self):
        url = "https://api.github.com/repos/andrefpoliveira/hptlc_exporter/releases/latest"
        response = requests.get(url)
        return response.json()["tag_name"][1:]
    
    def check_version(self):
        latest_version = self.get_latest_version()
        if any([int(latest_version.split(".")[i]) > int(VERSION.split(".")[i]) for i in range(3)]):
            response = requests.get("https://api.github.com/repos/andrefpoliveira/hptlc_exporter/releases/latest")
            assets = response.json()["assets"]
            for asset in assets:
                if asset["name"] == "hptlc_exporter.exe":
                    url = asset["browser_download_url"]
                    break

            response = tk.messagebox.askyesno("Update available", f"An update is available (v{latest_version}). Please download it. Do you want to open the download page?")
            if response:
                webbrowser.open(url)

            exit()

    def add_frame(self, frame):
        self.frame_stack.append(frame)
        self.show_frame()

    def pop_frame(self):
        self.frame_stack.pop()
        self.show_frame()

    def create_project(self, project_type):
        folder = project_type.lower()
        module = importlib.import_module(f"src.projects.{folder}.gui.new_project_page")
        self.add_frame(
            module.NewProjectPage(parent=self.container, controller=self, width=self.WIDTH, height=self.HEIGHT)
        )

    def open_project(self, project):
        folder = project["type"].lower()
        module = importlib.import_module(f"src.projects.{folder}.gui.submit_pdf_page")
        frame = module.SubmitPdfPage(parent=self.container, controller=self, width=self.WIDTH, height=self.HEIGHT, project=project)
        self.add_frame(frame)

    def show_frame(self):
        '''Show a frame for the given page name'''
        frame = self.frame_stack[-1]
        frame.place(x=0, y=0)
        frame.reset()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()