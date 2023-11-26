import customtkinter as ctk

from src.menus.main_page import MainPage
from src.menus.new_project_page import NewProjectPage
from src.menus.submit_pdf_page import SubmitPdfPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.WIDTH = 800
        self.HEIGHT = 500

        self.title("HPTLC Excel Generator")
        self.iconbitmap("assets/favicon.ico")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ctk.CTkFrame(self, width=self.WIDTH, height=self.HEIGHT)
        container.place(x=0, y=0)

        self.frames = {}
        for F in (MainPage, NewProjectPage, SubmitPdfPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, width=self.WIDTH, height=self.HEIGHT)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.place(x=0, y=0)

        self.show_frame("MainPage")

    def open_project(self, project):
        self.frames["SubmitPdfPage"].set_project(project)
        self.show_frame("SubmitPdfPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.reset()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()