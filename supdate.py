FILE = __file__
APPDIR = FILE.split("\\")[0:-1]
import ctypes
import sys
import logging
from io import StringIO
logging.basicConfig(level=logging.INFO,stream=)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def radmin(arg):
    #Arg is list of stuff
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(arg), None, 1)

logevs = []

def setup():
