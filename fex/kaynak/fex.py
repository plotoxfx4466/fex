import tkinter as tk
import subprocess
import sys
import time

def restart_program():
    subprocess.Popen([sys.executable, sys.argv[0]])
    
def exit_app(event=None):
    restart_program()
    root.destroy()


def on_closing():
    exit_app()
    
def on_altf4(event=None):
    return "break" 

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

label = tk.Label(root, text="!!! SIKINTI KARDEŞİM YA !!!\nGithub: plotoxfx4466", 
                  fg="white", bg="black", font=("Helvetica", 48), justify="center")
label.pack(expand=True)


root.protocol("WM_DELETE_WINDOW", on_closing)


root.bind_all("<Alt-F4>", on_altf4)


root.mainloop()