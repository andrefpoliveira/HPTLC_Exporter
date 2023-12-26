import customtkinter as ctk

from src.general.utils.utils import resource_path
from src.general.enum.project_type_enum import ProjectTypeEnum

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Iterate the enum and add the values to the dropdown
DROPDOWN_OPTIONS = ProjectTypeEnum.get_dropdown_options()

class ProjectTypeWindow(ctk.CTk):
    def __init__(self, main_app, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.main_app = main_app
        self.WIDTH = 350
        self.HEIGHT = 100

        self.option_selected = 0

        self.title("HPTLC - Choose Project Type")
        self.iconbitmap(resource_path("assets/favicon.ico"))
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        container = ctk.CTkFrame(self, width=self.WIDTH, height=self.HEIGHT)
        container.place(x=0, y=0)

        label = ctk.CTkLabel(container, text="Choose your project type:", font=("Arial", 14))
        label.place(x=10, y=5)

        option_menu = ctk.CTkOptionMenu(container, width=330, height=26, values=DROPDOWN_OPTIONS, dynamic_resizing=False, command=self.optionmenu_callback)
        option_menu.place(x=10, y=35)

        button = ctk.CTkButton(container, text="Continue", fg_color="#2663c4", hover_color="#0048ba", width=50, height=20, command=self.continue_button_clicked)
        button.place(x=150, y=70)

    def optionmenu_callback(self, value):
        self.option_selected = DROPDOWN_OPTIONS.index(value)

    def continue_button_clicked(self):
        self.main_app.create_project(list(ProjectTypeEnum.__members__.keys())[self.option_selected])