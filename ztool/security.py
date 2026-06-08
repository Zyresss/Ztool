import ctypes
import subprocess
import sys

def isAdmin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except OSError:
        return False

def relunch_as_admin() -> None:
    args = subprocess.list2cmdline(sys.argv) # list2cmdline : converts a list of arguments into a command line string
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)