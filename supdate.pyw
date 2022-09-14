INSTALLDIR = "\\".join(__file__.split("\\")[0:-1])
import ctypes
import sys
import json
import os
import requests
from packaging import version
VERSION = 2
def handleexc(type,value,traceback):
    r = Tk()
    r.withdraw()
    r.attributes("-topmost",True)
    messagebox.showerror("Supdate Fatal Error",f"A fatal error has occured.\nType: {str(type)}\nError: {str(value)}")
    sys.exit(-1)
sys.excepthook = handleexc
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def radmin(arg):
    #Arg is list of stuff
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(arg), None, 1)
from tkinter import ttk,messagebox,Tk

args = sys.argv[1:]
loadedargs = True
if "--about" in args:
    loadedargs = False
print(args)
if not os.path.isfile(INSTALLDIR + "\\supdate.manifest"):
    messagebox.showerror("Supdate",f"Supdate Version {VERSION}\n\nNo Manifest File Found. This istallation may be broken.")
    sys.exit(-1)

try:
    with open(INSTALLDIR + "\\supdate.manifest") as f:
        LDATA = json.load(f)
except json.decoder.JSONDecodeError:
    messagebox.showerror("Supdate Error","Manifest file is corrupt. This installation may be broken")
    sys.exit(-1)

if not loadedargs:
    messagebox.showinfo("Supdate",f"Supdate Version {VERSION}. (c) 2022 Enderbyte Programs\n\nLicensed To: {LDATA['licensedto']}")

SILENT = False
if "--silent" in args or "-s" in args:
    SILENT = True

def exinl(data,look):
    inc = 0
    for v in data:
        if look in v:
            return (True,inc)
        inc += 1
    return (False,-1)
if exinl(args,"--reference")[0]:
    e = exinl(args,"--reference")[1]
    NEWDREF = e.split("=")[1]
else:
    NEWDREF = LDATA["vreflink"]

try:
    UDATA = requests.get(NEWDREF).json()
    V = UDATA["version"]
    DLINK = UDATA["link"]
    CHG = UDATA["changelog"]
except:
    messagebox.showerror("Supdate","An Internet connection is required")
    sys.exit(-1)
_ly = '\n'.join(CHG)
if version.parse(V) > version.parse(LDATA["currentversion"]):
    if not SILENT:
        if messagebox.askyesno("Supdate",f"A new update is available for {LDATA['appname']}.\n\nYour Version: {LDATA['currentversion']}.\nNewest Version: {V}\nChangeset:\n{_ly}"):
            pass
        else:
            sys.exit()
else:
    if not SILENT:
        messagebox.showinfo("Supdate","No new updates are available")
        sys.exit()