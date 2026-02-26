from pathlib import Path

APP_NAME = "ztool" # The name of the application, used for various purposes such as logging, configuration, etc.
PARENT_MENU_NAME = "ZTool" # The name of the parent menu under which the tool's options will be organized in the user interface. This helps in categorizing and grouping related functionalities together for better user experience.

BASE_DIR = Path(__file__).resolve().parent.parent # The base directory of the project, which is determined by resolving the path of the current file (__file__) and navigating up two levels (parent.parent). This is useful for constructing paths to other files and directories within the project in a consistent manner.
DATA_FILE = BASE_DIR / "data.json" 