import json, os, re
import threading
import subprocess
import customtkinter as ctk
import tkinter as tk

from datetime import datetime

from src.hptlc import HptlcReader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SubmitPdfPage(ctk.CTkFrame):

    def __init__(self, parent, controller, width, height):
        ctk.CTkFrame.__init__(self, parent, width=width, height=height)

        self.controller = controller
        self.width = width
        self.height = height

        self.project = None

        self.create_window()

    def set_project(self, project):
        self.project = project

    def reset(self):
        self.create_window()

    def create_window(self):
        if self.project is None: return

        project_title = ctk.CTkLabel(self, text="Project:", font=("Arial", 15, "bold"))
        project_title.place(x=10, y=5)

        project_entry = ctk.CTkEntry(self, width=400, border_width=1, border_color="grey")
        project_entry.insert(0, self.project["title"])
        project_entry.configure(state="disabled")
        project_entry.place(x=70, y=5)

        project_folder_title = ctk.CTkLabel(self, text="Folder:", font=("Arial", 15, "bold"))
        project_folder_title.place(x=10, y=35)

        project_folder_entry = ctk.CTkEntry(self, width=400, border_width=1, border_color="grey")
        project_folder_entry.insert(0, self.project["folder"])
        project_folder_entry.configure(state="disabled")
        project_folder_entry.place(x=70, y=35)

        samples_title = ctk.CTkLabel(self, text="Samples:", font=("Arial", 15, "bold"))
        samples_title.place(x=500, y=5)

        samples_entry = ctk.CTkEntry(self, width=50, border_width=1, border_color="grey")
        samples_entry.insert(0, self.project["configuration"]["samples"])
        samples_entry.configure(state="disabled")
        samples_entry.place(x=570, y=5)

        groups_title = ctk.CTkLabel(self, text="Groups:", font=("Arial", 15, "bold"))
        groups_title.place(x=500, y=35)

        groups_scrollable_frame = ctk.CTkScrollableFrame(self, width = 200, height = 400, border_color="grey", border_width=1)
        groups_scrollable_frame.place(x=570, y=35)

        for id, g in enumerate(self.project["configuration"]["groups"]):
            frame = ctk.CTkFrame(groups_scrollable_frame, width=200, height=25)
            frame.grid(row=id, column=0, pady=2)

            group_label = ctk.CTkLabel(frame, text=f'{g["name"]} ({g["acronym"]})', font=("Arial", 12))
            group_label.place(x=10, y=5)


        self.file_frame = ctk.CTkFrame(self, width=550, height=369, border_color="white", border_width=1)
        self.file_frame.place(x=10, y=80)

        pdf_file_title = ctk.CTkLabel(self.file_frame, text="PDF File:", font=("Arial", 14))
        pdf_file_title.place(x=10, y=5)

        self.pdf_file_entry = ctk.CTkEntry(self.file_frame, width=530, border_width=1, border_color="grey", state="disabled")
        self.pdf_file_entry.place(x=10, y=30)

        browse_button = ctk.CTkButton(self.file_frame, text="Browse", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.choose_file)
        browse_button.place(x=484, y=6)

        tracks_label = ctk.CTkLabel(self.file_frame, text="Tracks:", font=("Arial", 14))
        tracks_label.place(x=10, y=65)

        self.load_tracks_button = ctk.CTkButton(self.file_frame, text="Load Tracks", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, state="disabled", command=self.load_tracks)
        self.load_tracks_button.place(x=456, y=66)

        self.build_tracks_scrollable()

        self.update_button = ctk.CTkButton(self.file_frame, text="Update", fg_color="#2663c4", hover_color="#0048ba", width=50, command=self.update_excel, state="disabled")
        self.update_button.place(x=550 - 60, y=369 - 34)

        open_file = ctk.CTkButton(self, text="Open File", fg_color="#2663c4", hover_color="#0048ba", width=50, command=self.open_file)
        open_file.place(x=self.width - 140, y=self.height - 34)

        self.finish_button = ctk.CTkButton(self, text="Done", fg_color="#2663c4", hover_color="#0048ba", width=50, command=lambda: self.controller.show_frame("MainPage"))
        self.finish_button.place(x=self.width - 60, y=self.height - 34)

    def open_file(self):
        os.startfile(f"{self.project['folder']}/{self.project['title']}.xlsx")

    def choose_file(self):
        file_path = tk.filedialog.askopenfilename(title = "Select file",filetypes = (("PDF Files","*.pdf"), ("All Files","*.*")))

        if file_path == "" or file_path == self.pdf_file_entry.get():
            return

        self.tracks_scrollable.destroy()
        self.build_tracks_scrollable()
        self.load_tracks_button.configure(state="normal")
        self.update_button.configure(state="disabled")

        self.pdf_file_entry.configure(state="normal")
        self.pdf_file_entry.delete(0, "end")
        self.pdf_file_entry.insert(0, file_path)
        self.pdf_file_entry.configure(state="disabled")

    def build_tracks_scrollable(self):
        self.tracks_scrollable = ctk.CTkScrollableFrame(self.file_frame, width = 507, height = 220, border_color="grey", border_width=1)
        self.tracks_scrollable.place(x=10, y=90)

    def most_frequent_number(self, l):
        counter = 0
        num = l[0]

        for i in l:
            curr_frequency = l.count(i)
            if(curr_frequency > counter):
                counter = curr_frequency
                num = i
        return num

    def load_tracks(self):
        self.load_tracks_button.configure(state="disabled")
        self.load_tracks_button.configure(text="Loading...")
        self.load_tracks_button.place(x=470, y=66)

        self.reader = HptlcReader(self.pdf_file_entry.get(), self.project["folder"] + "/" + self.project["title"] + ".xlsx")
        self.tables = self.reader.extract_info()

        substances_count = [len(self.tables[t]) for t in self.tables]
        most_frequent_substances_count = self.most_frequent_number(substances_count)

        checked = [False for t in self.tables]

        for id, k in enumerate(self.tables):
            m = re.findall("Track (\d+), ID: (.*) (.*) \(.*", k)
            if len(m) == 0: continue
            if len(self.tables[k]) != most_frequent_substances_count: continue
            if any(len(re.findall(r"\d", x[0])) == 0 for x in self.tables[k]): continue
            checked[id] = True

        self.checkboxes = []

        for id, k in enumerate(self.tables):
            frame = ctk.CTkFrame(self.tracks_scrollable, width=507, height=30)
            frame.grid(row=id, column=0, pady=2)

            check_var = ctk.BooleanVar(value=checked[id])
            checkbox = ctk.CTkCheckBox(frame, text="", variable=check_var, onvalue=True, offvalue=False, border_width=1, border_color="white", checkbox_width=18, checkbox_height=18)
            checkbox.place(x=10, y=3)
            self.checkboxes.append(check_var)

            track_name = ctk.CTkLabel(frame, text=k, font=("Arial", 12))
            track_name.place(x=40, y=0)

        self.load_tracks_button.configure(text="Load Tracks")
        self.load_tracks_button.configure(state="normal")
        self.load_tracks_button.place(x=456, y=66)

        self.update_button.configure(state="normal")

    def update_excel(self):
        table_keys = list(self.tables.keys())
        new_tables = {}

        for id, k in enumerate(table_keys):
            if self.checkboxes[id].get():
                new_tables[k] = self.tables[k]
                
        try:
            self.reader.build_excel(new_tables, self.project["configuration"])
            tk.messagebox.showinfo("Success", "The excel file was successfully updated.")
        except PermissionError:
            tk.messagebox.showerror("Error", "Please close the excel file before updating it.")
            return

        with open(self.controller.projects_path) as f:
            projects = json.load(f)

        for id, p in enumerate(projects):
            if p["title"] == self.project["title"] and p["folder"] == self.project["folder"]:
                projects[id]["modification"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                break

        with open(self.controller.projects_path, "w", encoding="utf8") as f:
            json.dump(projects, f, indent=4, ensure_ascii=False)