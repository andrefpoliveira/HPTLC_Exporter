import os, json

from src.menus.app import App

if __name__ == "__main__":
    if not os.path.exists("projects.json"):
        with open("projects.json", "w", encoding="utf8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
            
    app = App()
    app.mainloop()