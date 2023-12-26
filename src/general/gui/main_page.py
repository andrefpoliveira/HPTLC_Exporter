import json
import os
import webbrowser
from PIL import Image

from src.general.utils.utils import resource_path
from src.general.gui.project_type_window import ProjectTypeWindow

import tkinter as tk

import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainPage(ctk.CTkFrame):

    def __init__(self, parent, controller, width, height):
        ctk.CTkFrame.__init__(self, parent, width=width, height=height)

        self.controller = controller
        
        self.SIDEBAR_WIDTH = 200
        self.button_selected = 0
        self.buttons = ["Projects"]
        self.create_window()

    def reset(self):
        self.create_window()

    def open_project_type_window(self):
        self.window = ProjectTypeWindow(self)
        self.window.mainloop()

    def create_project(self, project_type):
        self.after(100, self.window.destroy)
        self.controller.create_project(project_type)
        
    def generate_projects_list(self, text = ""):
        with open(self.controller.projects_path, encoding="utf8") as f:
            projects = json.load(f)

        projects = sorted(projects, key=lambda k: k["modification"], reverse=True)

        scrollable_frame = ctk.CTkScrollableFrame(self, width = 560, height = 420)

        for id, p in enumerate(projects):
            if text != "" and text.lower() not in p["title"].lower():
                continue

            button = ctk.CTkButton(scrollable_frame, text="", fg_color="transparent", border_width=1, border_color="white", width=560, height=70, command=lambda p=p: self.controller.open_project(p))
            button.grid(row=id, column=0, pady=2)

            title = ctk.CTkLabel(button, text=p["title"], fg_color="transparent", font=("Arial", 12, "bold"))
            title.place(x=10, y=1)

            folder = ctk.CTkLabel(button, text=p["folder"], fg_color="transparent", font=("Arial", 10))
            folder.place(x=10, y=21)

            modification_date = ctk.CTkLabel(button, text=p["modification"], fg_color="transparent", font=("Arial", 10))
            modification_date.place(x=10, y=41)

            delete_button = ctk.CTkButton(button, text="Delete", fg_color="#ff2424", hover_color="#ff0000", width=50, height=20, command=lambda p=p: self.delete_project(p))
            delete_button.place(x=500, y=25)

        scrollable_frame.place(x=self.SIDEBAR_WIDTH + 10, y=60)

    def delete_project(self, project):
        confirm = tk.messagebox.askyesno("Delete Project", "Are you sure you want to delete this project?")
        if not confirm: return

        with open(self.controller.projects_path, encoding="utf8") as f:
            projects = json.load(f)

        projects = [
            x for x in projects if x["folder"] + "/" + x["title"] + ".xlsx" != project["folder"] + "/" + project["title"] + ".xlsx"
        ]

        os.remove(project["folder"] + "/" + project["title"] + ".xlsx")

        with open(self.controller.projects_path, "w", encoding="utf8") as f:
            json.dump(projects, f, indent=4, ensure_ascii=False)

        self.generate_projects_list()

    def check_input_changed(self):
        if self.search_box.edit_modified():
            new_text = self.search_box.get("1.0", "end-1c")
            self.generate_projects_list(new_text)
            self.search_box.edit_modified(False)

        self.after(200, self.check_input_changed)

    def create_window(self):
        frame = ctk.CTkFrame(self, width=self.SIDEBAR_WIDTH, height=600, fg_color="#2b2b2b")
        frame.place(x=0, y=-50)

        for id, button in enumerate(self.buttons):
            button = ctk.CTkButton(
                self, 
                text=button, 
                fg_color="#2b2b2b" if self.button_selected != id else "#2663c4", 
                hover_color="#2663c4",
                width=self.SIDEBAR_WIDTH - 10
            )
            button.place(x = 5, y = 20 + 35 * id)

        search_icon = ctk.CTkImage(Image.open(resource_path("assets/search.png")))
        search_label = ctk.CTkLabel(self, image=search_icon, text="")
        search_label.place(x=self.SIDEBAR_WIDTH + 10, y=20)

        text_box = ctk.CTkTextbox(self, width=400, height=26, border_width=1, border_color="white")
        text_box.place(x=self.SIDEBAR_WIDTH + 40, y=20)
        self.search_box = text_box

        self.after(200, self.check_input_changed)

        new_project_button = ctk.CTkButton(self, height=30, text="New Project", fg_color="#2663c4", hover_color="#0048ba", command=lambda: self.open_project_type_window())
        new_project_button.place(x=self.SIDEBAR_WIDTH + 450, y=20)

        self.generate_projects_list()

        developed_label = ctk.CTkLabel(self, text="Developed by André Oliveira", fg_color="#2b2b2b", font=("Arial", 12))
        developed_label.place(x=20, y=450)

        contact_label = ctk.CTkLabel(self, text="Click here to contact me", fg_color="#2b2b2b", font=("Arial", 12, "underline"))
        contact_label.place(x=30, y=470)
        contact_label.bind("<Button-1>", lambda e: webbrowser.open_new("mailto:andre_pinto_oliveira@outlook.pt"))