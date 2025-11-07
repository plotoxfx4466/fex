import os
import sys
import tempfile
import subprocess

def get_startup_folder():
    appdata = os.getenv('APPDATA')
    if not appdata:
        raise EnvironmentError("APPDATA ortam değişkeni bulunamadı. Bu script Windows üzerinde çalıştırılmalıdır.")
    return os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")

def create_shortcut_with_pywin(target_exe, shortcut_path):
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_exe
    shortcut.WorkingDirectory = os.path.dirname(target_exe)
    shortcut.IconLocation = target_exe
    shortcut.Save()

def create_shortcut_with_vbs(target_exe, shortcut_path):
    vbs = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_exe}"
oLink.WorkingDirectory = "{os.path.dirname(target_exe)}"
oLink.IconLocation = "{target_exe}"
oLink.Save
'''
    fd, vbs_path = tempfile.mkstemp(suffix=".vbs", text=True)
    os.close(fd)
    try:
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs)

        subprocess.check_call(["cscript", "//nologo", vbs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        try:
            os.remove(vbs_path)
        except Exception:
            pass

def install_shortcut(exe_name="main.exe", force_overwrite=False):
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    target_exe = os.path.join(script_dir, exe_name)

    if not os.path.isfile(target_exe):

        return False

    startup = get_startup_folder()
    shortcut_name = os.path.splitext(exe_name)[0] + ".lnk"
    shortcut_path = os.path.join(startup, shortcut_name)

    if os.path.exists(shortcut_path) and not force_overwrite:

        return True


    try:
        try:
            import win32com.client  
            create_shortcut_with_pywin(target_exe, shortcut_path)

        except ImportError:

            create_shortcut_with_vbs(target_exe, shortcut_path)



        return True
    except subprocess.CalledProcessError as e:

        return False
    except Exception as e:

        return False

def remove_shortcut(exe_name="main.exe"):
    startup = get_startup_folder()
    shortcut_name = os.path.splitext(exe_name)[0] + ".lnk"
    shortcut_path = os.path.join(startup, shortcut_name)
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)

            return True
        except Exception as e:

            return False
    else:

        return False

if __name__ == "__main__":

    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if arg == "remove":
        remove_shortcut()
    else:
        force = (arg == "force")
        install_shortcut(force_overwrite=force)
