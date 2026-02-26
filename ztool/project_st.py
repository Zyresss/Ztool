from dataclasses import dataclass

@dataclass
class Project:
    name: str
    path: str
    icon: str = ""