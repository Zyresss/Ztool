# this contains loading and saving data to a file, and also the data structure for the project
import json
from ztool.project_st import Project
from pathlib import Path
from dataclasses import asdict

class Storage:
    def __init__(self, path_file: Path):
        self.path_file = path_file
    def load(self) -> list[Project]:
        if not self.path_file.exists():
            return []
        try:
            raw = json.loads(self.path_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(raw,list):
            return []
        projects: list[Project] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip() #strip removes leading and trailing whitespace characters from the name string, ensuring that the project name is clean and does not contain any unintended spaces.
            path = str(item.get("path", "")).strip()
            icon = str(item.get("icon", "")).strip()
            if name and path:
                projects.append(Project(name=name, path=path, icon=icon))
        return projects
    
    def save(self, projects: list[Project]) -> None:
        data = [asdict(project) for project in projects] # asdict 
        self.path_file.write_text(
            json.dumps(data, indent=4, ensure_ascii=False), # ensure_ascii=False allows the JSON encoder to output non-ASCII characters as they are, instead of escaping them with Unicode escape sequences. This is particularly useful when dealing with project names or paths that may contain characters from various languages, ensuring that the data is stored in a human-readable format without losing any information.
            encoding="utf-8",
        )