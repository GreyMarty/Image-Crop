import tkinter as tk
from tkinter import filedialog
import os
import shutil

from panel import Panel
from editor import Editor


def load():
    global editor

    path = filedialog.askopenfilename()

    if path:
        if editor:
            for child in editor_area.winfo_children():
                child.destroy()

        editor = Editor(path, master=editor_area, bg="black")
        editor.pack()


def crop_image(event):
    global editor

    if editor:
        img = editor.crop_image()

        if not img:
            return

        try:
            os.mkdir("tmp")
        except WindowsError:
            pass
        img.save("tmp/img.jpg")

        for child in editor_area.winfo_children():
            child.destroy()

        editor = Editor("tmp/img.jpg", master=editor_area, bg="black")
        editor.pack()


def save():
    path = filedialog.asksaveasfilename()

    if path and editor:
        file_type = path.split(".")[-1].upper() if not path.endswith(".jpg") else "JPEG"
        editor.img.save(path, file_type)


def on_close():
    try:
        shutil.rmtree("tmp")
    except WindowsError:
        pass
    finally:
        root.destroy()


root = tk.Tk()

root.minsize(1280, 720)

editor = None

panel_buttons = {
    "Load": load,
    "Save": save
}
panel = Panel(panel_buttons, master=root, height=30, highlightbackground="#c7c7c7", highlightthickness=1)
panel.pack()

editor_area = tk.Frame(root)
editor_area.pack(side="bottom", fill="both", expand=1)

root.bind("<Return>", crop_image)
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
