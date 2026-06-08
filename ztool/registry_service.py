import os
import winreg 
from dataclasses import dataclass # dataclass is a decorator that automatically generates special methods for classes, such as __init__, __repr__, and __eq__, based on the class attributes. In this code, it is used to define the RegistryTarget class, which represents a target location in the Windows registry for adding context menu entries

from ztool.config import PARENT_MENU_NAME


@dataclass(frozen=True)
class RegistryTarget:
    hkey: int
    base_path: str
    argument_token: str # the argument token is a placeholder that will be replaced with the actual file or directory path when the context menu entry is invoked. For example, "%1" represents the selected file or directory, while "%V" represents the current directory when right-clicking on the background of a folder


class RegistryService:
    TARGETS = [
        RegistryTarget(winreg.HKEY_CLASSES_ROOT, r"*\shell", "%1"),
        RegistryTarget(winreg.HKEY_CLASSES_ROOT, r"Directory\shell", "%1"),
        RegistryTarget(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell", "%V"),
    ]

    @staticmethod
    def _normalize(path: str) -> str:
        return os.path.normpath(path)

    @staticmethod
    def _choose_icon_value(exe_path: str, icon_path: str) -> str:
        normalized_exe = RegistryService._normalize(exe_path)
        candidate = RegistryService._normalize(icon_path) if icon_path else ""

        if candidate and os.path.exists(candidate):
            ext = os.path.splitext(candidate)[1].lower()
            if ext == ".ico":
                return candidate
            if ext in {".exe", ".dll"}:
                return f"{candidate},0"

        return f"{normalized_exe},0"

    def add_project(self, name: str, exe_path: str, icon_path: str) -> None:
        normalized_exe = self._normalize(exe_path)
        icon_value = self._choose_icon_value(normalized_exe, icon_path)

        if not os.path.exists(normalized_exe):
            raise FileNotFoundError(f"Executable not found: {normalized_exe}")

        for target in self.TARGETS:
            parent_key = f"{target.base_path}\\{PARENT_MENU_NAME}"
            shell_key = f"{parent_key}\\shell"
            app_key = f"{shell_key}\\{name}"
            command_key = f"{app_key}\\command"

            try:
                with winreg.CreateKey(target.hkey, parent_key) as key:
                    winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, PARENT_MENU_NAME)
                    winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ, "")

                winreg.CreateKey(target.hkey, shell_key)

                with winreg.CreateKey(target.hkey, app_key) as key:
                    winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, name)
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_value)

                command = f'"{normalized_exe}" "{target.argument_token}"'
                with winreg.CreateKey(target.hkey, command_key) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, command)
            except OSError as exc:
                raise OSError(f"Registry write failed at {target.base_path}: {exc}") from exc

    def remove_project(self, name: str) -> None:
        for target in self.TARGETS:
            app_key = f"{target.base_path}\\{PARENT_MENU_NAME}\\shell\\{name}"
            command_key = f"{app_key}\\command"
            try:
                winreg.DeleteKey(target.hkey, command_key)
            except FileNotFoundError:
                pass
            try:
                winreg.DeleteKey(target.hkey, app_key)
            except FileNotFoundError:
                pass

