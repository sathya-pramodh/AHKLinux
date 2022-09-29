import time
import tkinter as tk
from tkinter import Button, Label, Canvas
from window.msgbox_combinations import ALL_COMBINATIONS


def parse_option(option):
    return ALL_COMBINATIONS.get(option, None)


def make_msgbox(title, text, option, timeout):
    root = tk.Tk()
    root.title(title)
    root.after(1000 * timeout, root.destroy)
    root.resizable(False, False)
    if isinstance(option, str):
        option = int(option, base=16)
    groups = parse_option(option)
    if groups is None:
        return 1
    groups = groups.split(",")
    btn_name = groups[0]
    if btn_name == "OK":
        root.geometry("500x175")
        Label(root, text=text, height=5, width=50, font=":11").pack(side=tk.TOP)
        Button(root, text="OK", command=root.destroy, width=15).pack(side=tk.BOTTOM)
    elif btn_name == "OK/Cancel":
        txt_canvas = Canvas(root)
        txt_canvas.grid(row=1, column=1, columnspan=4, rowspan=2)
        btn_canvas = Canvas(root)
        btn_canvas.grid(row=3, column=1, columnspan=5)
        lbl = Label(txt_canvas, text=text, height=5, width=50, font=":11")
        lbl.grid(row=1, column=1, rowspan=2)
        btn1 = Button(btn_canvas, text="OK", command=root.destroy, width=15)
        btn1.grid(row=1, column=1, columnspan=2)
        btn2 = Button(btn_canvas, text="Cancel", command=root.destroy, width=15)
        btn2.grid(row=1, column=3, columnspan=2)
    elif btn_name == "Abort/Retry/Ignore":
        txt_canvas = Canvas(root)
        txt_canvas.grid(row=1, column=1, columnspan=4, rowspan=2)
        btn_canvas = Canvas(root)
        btn_canvas.grid(row=3, column=1, columnspan=4)
        lbl = Label(txt_canvas, text=text, height=5, width=50, font=":11")
        lbl.grid(row=0, column=2, rowspan=2)
        btn1 = Button(btn_canvas, text="Abort", command=root.destroy, width=10)
        btn1.grid(row=2, column=0, columnspan=2)
        btn2 = Button(btn_canvas, text="Retry", command=root.destroy, width=10)
        btn2.grid(row=2, column=2, columnspan=2)
        btn3 = Button(btn_canvas, text="Ignore", command=root.destroy, width=10)
        btn3.grid(row=2, column=4, columnspan=2)
    elif btn_name == "Yes/No/Cancel":
        txt_canvas = Canvas(root)
        txt_canvas.grid(row=1, column=1, columnspan=4, rowspan=2)
        btn_canvas = Canvas(root)
        btn_canvas.grid(row=3, column=1, columnspan=5)
        lbl = Label(txt_canvas, text=text, height=5, width=50, font=":11")
        lbl.grid(row=0, column=2, rowspan=2)
        btn1 = Button(btn_canvas, text="Yes", command=root.destroy, width=10)
        btn1.grid(row=2, column=0, columnspan=2)
        btn2 = Button(btn_canvas, text="No", command=root.destroy, width=10)
        btn2.grid(row=2, column=2, columnspan=2)
        btn3 = Button(btn_canvas, text="Cancel", command=root.destroy, width=10)
        btn3.grid(row=2, column=4, columnspan=2)
    root.mainloop()
    return 0
