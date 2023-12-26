import json, os
import customtkinter as ctk
import tkinter as tk

from datetime import datetime
from functools import partial
from openpyxl import Workbook

from src.general.gui.group_window import GroupWindow
from src.projects.other.gui.sample_window import SampleWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NewProjectPage(ctk.CTkFrame):

    def __init__(self, parent, controller, width, height):
        ctk.CTkFrame.__init__(self, parent, width=width, height=height)

        self.controller = controller
        self.width = width
        self.height = height

        self.groups = []
        self.samples = []

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
        self.controller.pop_frame()

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

        with open(self.controller.projects_path, encoding="utf8") as f:
            projects = json.load(f)

        info = {
            "title": title,
            "folder": folder,
            "modification": modification_date,
            "configuration": {
                "samples": sorted(self.samples),
                "groups": self.groups
            },
            "type": "other"
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

        self.controller.pop_frame()

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

    def open_sample_window(self, args = []):
        window = SampleWindow(self, args)
        window.mainloop()

    def save_sample(self, window, sample, id):
        self.after(100, window.destroy)

        if id is None:
            self.samples.append(sample)
        else:
            self.samples[id] = sample

        self.create_samples()

    def delete_group(self, id):
        self.groups.pop(id)
        self.reset()

    def delete_sample(self, id):
        self.samples.pop(id)
        self.reset()

    def create_groups(self):
        self.scrollable_groups = ctk.CTkScrollableFrame(self, width=500, height=270, border_width=1, border_color="grey")
        self.scrollable_groups.place(x=10, y=175)

        for id, group in enumerate(self.groups):
            frame = ctk.CTkFrame(self.scrollable_groups, width=500, height=65, border_color="white", border_width=1)
            frame.grid(row=id, column=0, pady=2)

            l = ctk.CTkLabel(frame, text="Name:", font=("Arial", 12))
            l.place(x=10, y=5)
            name_label = ctk.CTkLabel(frame, text=group["name"], font=("Arial", 12, "bold"))
            name_label.place(x=55, y=5)

            l = ctk.CTkLabel(frame, text="Acronym:", font=("Arial", 12))
            l.place(x=10, y=30)
            acronym_label = ctk.CTkLabel(frame, text=group["acronym"], font=("Arial", 12, "bold"))
            acronym_label.place(x=68, y=30)

            l = ctk.CTkLabel(frame, text="Color:", font=("Arial", 12))
            l.place(x=180, y=18)
            color_label = ctk.CTkButton(frame, text="", width=20, height=20, fg_color="#" + group["base_color"], hover_color="#" + group["base_color"], border_width=1, border_color="white")
            color_label.place(x=220, y=22)

            edit_button = ctk.CTkButton(frame, text="Edit", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=partial(self.open_group_window, (id, group)))
            edit_button.place(x=440, y=10)

            delete_button = ctk.CTkButton(frame, text="Delete", fg_color="#ff2424", hover_color="#ff0000", width=50, height=20, command=lambda id=id: self.delete_group(id))
            delete_button.place(x=440, y=35)

    def create_samples(self):
        self.scrollable_samples = ctk.CTkScrollableFrame(self, width=220, height=270, border_width=1, border_color="grey")
        self.scrollable_samples.place(x=545, y=175)

        for id, sample in enumerate(self.samples):
            frame = ctk.CTkFrame(self.scrollable_samples, width=220, height=65, border_color="white", border_width=1)
            frame.grid(row=id, column=0, pady=2)

            l = ctk.CTkLabel(frame, text="Name:", font=("Arial", 12))
            l.place(x=10, y=18)
            name_label = ctk.CTkLabel(frame, text=sample, font=("Arial", 12, "bold"))
            name_label.place(x=55, y=18)

            edit_button = ctk.CTkButton(frame, text="Edit", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=partial(self.open_sample_window, (id, sample)))
            edit_button.place(x=160, y=10)

            delete_button = ctk.CTkButton(frame, text="Delete", fg_color="#ff2424", hover_color="#ff0000", width=50, height=20, command=lambda id=id: self.delete_sample(id))
            delete_button.place(x=160, y=35)

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

        groups_label = ctk.CTkLabel(self, text="Groups:", font=("Arial", 14))
        groups_label.place(x=10, y=145)

        groups_button = ctk.CTkButton(self, text="Add Group", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.open_group_window)
        groups_button.place(x=448, y=148)

        self.create_groups()

        samples_label = ctk.CTkLabel(self, text="Samples:", font=("Arial", 14))
        samples_label.place(x=545, y=145)

        samples_button = ctk.CTkButton(self, text="Add Sample", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.open_sample_window)
        samples_button.place(x=700, y=148)

        self.create_samples()

        cancel_button = ctk.CTkButton(self, text="Cancel", fg_color="#ff2424", hover_color="#ff0000", width=50, command=self.cancel_button_clicked)
        cancel_button.place(x=self.width - 120, y=self.height - 34)

        self.finish_button = ctk.CTkButton(self, text="Finish", fg_color="#2663c4", hover_color="#0048ba", width=50, command=self.finish_button_clicked, state="disabled")
        self.finish_button.place(x=self.width - 60, y=self.height - 34)

        self.after(100, self.check_fields)

    def check_fields(self):
        self.after(100, self.check_fields)

        self.finish_button.configure(state="disabled")

        if len(self.groups) == 0: return
        if len(self.samples) == 0: return

        title = self.title_box.get().strip()
        if title == "" or any(char in title for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
            return
        
        folder = self.path_box.get().strip()
        if folder == "":
            return
        
        self.finish_button.configure(state="normal")

