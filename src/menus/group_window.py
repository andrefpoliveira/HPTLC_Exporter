import customtkinter as ctk
from functools import partial

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgba_to_hex(rgba):
    alpha = rgba[3]
    rgb = [int((1 - alpha) * 255 + alpha * x) for x in rgba[:3]]
    return rgb_to_hex(tuple(rgb))

colors = [
    (68, 84, 106),
    (91, 155, 213),
    (237, 125, 49),
    (165, 165, 165),
    (255, 192, 0),
    (68, 114, 196),
    (112, 173, 71),
    (255, 0, 0),
    (255, 255, 0),
    (146, 208, 80),
    (0, 176, 240),
    (0, 112, 192),
    (112, 48, 160)
]

class GroupWindow(ctk.CTk):

    def __init__(self, main_app, previous_values, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.id = None
        self.group_name = ""
        self.group_acronym = ""
        self.selected_color = 0
        self.previous_color = -1

        if previous_values:
            self.id = previous_values[0]
            self.group_name = previous_values[1]["name"]
            self.group_acronym = previous_values[1]["acronym"]
            self.selected_color = colors.index(hex_to_rgb(previous_values[1]["base_color"]))

        self.main_app = main_app


        self.WIDTH = 300
        self.HEIGHT = 250

        self.title("HPTLC - New Group")
        self.iconbitmap("assets/favicon.ico")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        container = ctk.CTkFrame(self, width=self.WIDTH, height=self.HEIGHT)
        container.place(x=0, y=0)

        group_label = ctk.CTkLabel(container, text="Group Name:", font=("Arial", 14))
        group_label.place(x=10, y=5)

        self.group_entry = ctk.CTkEntry(container, width=280, height=26, border_width=1, border_color="white", placeholder_text="Group 1")
        if self.group_name != "":
            self.group_entry.insert(0, self.group_name)
        self.group_entry.place(x=10, y=35)

        acronym_label = ctk.CTkLabel(container, text="Group Acronym:", font=("Arial", 14))
        acronym_label.place(x=10, y=65)

        self.acronym_entry = ctk.CTkEntry(container, width=280, height=26, border_width=1, border_color="white", placeholder_text="G")
        if self.group_acronym != "":
            self.acronym_entry.insert(0, self.group_acronym)
        self.acronym_entry.place(x=10, y=95)

        color_label = ctk.CTkLabel(container, text="Group Color:", font=("Arial", 14))
        color_label.place(x=10, y=125)

        self.draw_colors(container)

        self.save_button = ctk.CTkButton(container, text="Save", width=100, height=20, fg_color="#2663c4", hover_color="#0048ba", command=self.send_information, state="disabled")
        self.save_button.place(x=100, y=self.HEIGHT-30)

        self.after(100, partial(self.draw_colors, container))
        self.after(100, self.check_fields)

    def check_fields(self):
        self.group_name = self.group_entry.get()
        self.group_acronym = self.acronym_entry.get()

        if self.group_name != "" and self.group_acronym != "":
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")

        self.after(100, self.check_fields)

    def draw_colors(self, container):
        if self.previous_color != self.selected_color:
            self.previous_color = self.selected_color
            for id, c in enumerate(colors):
                color_button = ctk.CTkButton(container, text="", corner_radius=0, width=20, height=20, fg_color=rgb_to_hex(c), hover_color=rgb_to_hex(c), border_color="grey" if id != self.selected_color else "white", border_width=1, command=lambda id=id: self.change_color(id))
                color_button.place(x=10+(id*21), y=155)

        self.after(100, partial(self.draw_colors, container))

    def change_color(self, id):
        self.selected_color = id

    def send_information(self):
        color = colors[self.selected_color]
        self.main_app.save_group(self, {
            "name": self.group_name,
            "acronym": self.group_acronym,
            "base_color": rgb_to_hex(color)[1:],
            "main_color": rgba_to_hex((*color, 0.6))[1:],
            "secondary_color": rgba_to_hex((*color, 0.4))[1:],
            "tertiary_color": rgba_to_hex((*color, 0.2))[1:]
        }, self.id)


