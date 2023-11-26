import json
import os
from sys import platform

from src.menus.app import App

if __name__ == "__main__":
    if platform.startswith("win"):
        if not os.path.isdir("C:/HPTLC_Excel_Creator"):
            os.mkdir("C:/HPTLC_Excel_Creator")

        if not os.path.exists("C:/HPTLC_Excel_Creator/projects.json"):
            with open("C:/HPTLC_Excel_Creator/projects.json", "w", encoding="utf8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
    else:
        raise Exception("This program only works on Windows.")
            
    app = App()
    app.mainloop()