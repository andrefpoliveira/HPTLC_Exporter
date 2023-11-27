import json, os
import customtkinter as ctk
import tkinter as tk

from datetime import datetime
from functools import partial
from openpyxl import Workbook

from src.menus.group_window import GroupWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NewProjectPage(ctk.CTkFrame):

    def __init__(self, parent, controller, width, height):
        ctk.CTkFrame.__init__(self, parent, width=width, height=height)

        self.controller = controller
        self.width = width
        self.height = height

        self.groups = []

        self.create_window()

    def reset(self):
        self.create_window()

    def get_directory(self):
        folder = tk.filedialog.askdirectory()

        self.path_box.configure(state="normal")
        self.path_box.delete(0, "end")
        self.path_box.insert(0, folder)
        self.path_box.configure(state="disabled")

    def cancel_button_clicked(self):
        self.controller.show_frame("MainPage")

    def finish_button_clicked(self):
        title = self.title_box.get().strip()
        folder = self.path_box.get().strip()

        if os.path.exists(folder + "/" + title + ".xlsx"):
            result = tk.messagebox.askyesno("File already exists", "A file with this name already exists.\nDo you want to overwrite it?")
            if result:
                self.save_project()
            else:
                return
        else:
            self.save_project()

    def save_project(self):
        title = self.title_box.get()
        folder = self.path_box.get()
        modification_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        samples = int(self.samples_box.get())

        with open(self.controller.projects_path, encoding="utf8") as f:
            projects = json.load(f)

        info = {
            "title": title,
            "folder": folder,
            "modification": modification_date,
            "configuration": {
                "samples": samples,
                "groups": self.groups
            }
        }

        for id, p in enumerate(projects):
            if p["title"] == title and p["folder"] == folder:
                projects[id] = info
                break
        else:
            projects.append(info)

        with open(self.controller.projects_path, "w", encoding="utf8") as f:
            json.dump(projects, f, indent=4, ensure_ascii=False)

        wb = Workbook()
        wb.save(folder + "/" + title + ".xlsx")

        self.groups = []

        self.controller.show_frame("MainPage")

    def save_group(self, window, group, id):
        self.after(100, window.destroy)

        if id is None:
            self.groups.append(group)
        else:
            self.groups[id] = group
            
        self.create_groups()

    def open_group_window(self, args = []):
        window = GroupWindow(self, args)
        window.mainloop()

    def delete_group(self, id):
        self.groups.pop(id)
        self.reset()

    def create_groups(self):
        self.scrollable_groups = ctk.CTkScrollableFrame(self, width=757, height=230, border_width=1, border_color="grey")
        self.scrollable_groups.place(x=10, y=215)

        for id, group in enumerate(self.groups):
            frame = ctk.CTkFrame(self.scrollable_groups, width=757, height=40, border_color="white", border_width=1)
            frame.grid(row=id, column=0, pady=2)

            l = ctk.CTkLabel(frame, text="Name:", font=("Arial", 12))
            l.place(x=10, y=5)
            name_label = ctk.CTkLabel(frame, text=group["name"], font=("Arial", 12, "bold"))
            name_label.place(x=55, y=5)

            l = ctk.CTkLabel(frame, text="Acronym:", font=("Arial", 12))
            l.place(x=250, y=5)
            acronym_label = ctk.CTkLabel(frame, text=group["acronym"], font=("Arial", 12, "bold"))
            acronym_label.place(x=308, y=5)

            l = ctk.CTkLabel(frame, text="Color:", font=("Arial", 12))
            l.place(x=458, y=5)
            color_label = ctk.CTkButton(frame, text="", width=20, height=20, fg_color="#" + group["base_color"], hover_color="#" + group["base_color"], border_width=1, border_color="white")
            color_label.place(x=500, y=9)

            edit_button = ctk.CTkButton(frame, text="Edit", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=partial(self.open_group_window, (id, group)))
            edit_button.place(x=630, y=10)

            delete_button = ctk.CTkButton(frame, text="Delete", fg_color="#ff2424", hover_color="#ff0000", width=50, height=20, command=lambda id=id: self.delete_group(id))
            delete_button.place(x=690, y=10)

    def create_window(self):
        title = ctk.CTkLabel(self, text="Choose the file name:", font=("Arial", 14))
        title.place(x=10, y=5)

        title_box = ctk.CTkEntry(self, width=780, height=26, border_width=1, border_color="white", placeholder_text="HPTLC_Results")
        title_box.place(x=10, y=35)
        self.title_box = title_box

        path = ctk.CTkLabel(self, text="Choose a directory to store the file:", font=("Arial", 14))
        path.place(x=10, y=75)

        path_button = ctk.CTkButton(self, text="Browse", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.get_directory)
        path_button.place(x=733, y=79)

        path_box = ctk.CTkEntry(self, width=780, height=26, border_width=1, border_color="grey", state="disabled")
        path_box.place(x=10, y=105)
        self.path_box = path_box

        samples_label = ctk.CTkLabel(self, text="Number of samples:", font=("Arial", 14))
        samples_label.place(x=10, y=145)

        samples_box = ctk.CTkEntry(self, width=50, height=26, border_width=1, border_color="white", placeholder_text="8")
        samples_box.place(x=140, y=145)
        self.samples_box = samples_box

        groups_label = ctk.CTkLabel(self, text="Groups:", font=("Arial", 14))
        groups_label.place(x=10, y=185)

        groups_button = ctk.CTkButton(self, text="Add Group", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.open_group_window)
        groups_button.place(x=718, y=188)

        self.create_groups()

        cancel_button = ctk.CTkButton(self, text="Cancel", fg_color="#ff2424", hover_color="#ff0000", width=50, command=self.cancel_button_clicked)
        cancel_button.place(x=self.width - 120, y=self.height - 34)

        self.finish_button = ctk.CTkButton(self, text="Finish", fg_color="#2663c4", hover_color="#0048ba", width=50, command=self.finish_button_clicked, state="disabled")
        self.finish_button.place(x=self.width - 60, y=self.height - 34)

        self.after(100, self.check_fields)

    def check_fields(self):
        self.after(100, self.check_fields)

        if len(self.groups) == 0: return

        title = self.title_box.get().strip()
        if title == "" or any(char in title for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
            return
        
        folder = self.path_box.get().strip()
        if folder == "":
            return
        
        samples = self.samples_box.get().strip()
        if samples == "" or not samples.isdigit():
            return
        
        self.finish_button.configure(state="normal")

