import json
import os

from src.menus.app import App

def renovate_projects_file():
    current_file_path = os.path.realpath(__file__)
    dir = current_file_path.replace("\\", "/").split("/")[0] + "/hptlc_creator"
    new_dir = current_file_path.replace("\\", "/").split("/")[0] + "/hptlc_exporter"

    if os.path.isdir(dir):
        os.rename(dir, new_dir)

def create_projects_file():
    current_file_path = os.path.realpath(__file__)
    dir = current_file_path.replace("\\", "/").split("/")[0] + "/hptlc_exporter"

    if not os.path.isdir(dir):
        os.mkdir(dir)

    if not os.path.exists(dir + "/projects.json"):
        with open(dir + "/projects.json", "w", encoding="utf8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    return dir + "/projects.json"

if __name__ == "__main__":
    try:
        renovate_projects_file()
        projects_path = create_projects_file()
    except:
        raise Exception("Cannot create necessary files. Please contact the developer.")
            
    app = App(projects_path)
    app.mainloop()