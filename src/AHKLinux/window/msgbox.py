import tkinter as tk
from tkinter import Button, Label, Canvas
from window.msgbox_combinations import ALL_COMBINATIONS
from PIL import ImageTk, Image

BTNS = [
    "OK",
    "OK/Cancel",
    "Abort/Retry/Ignore",
    "Yes/No/Cancel",
    "Yes/No",
    "Retry/Cancel",
    "Cancel/Try Again/Continue",
]
ICONS = [
    "Icon Hand (stop/error)",
    "Icon Question",
    "Icon Exclamation",
    "Icon Asterisk (info)",
]
DEFAULT_BTNS = ["2nd btn default", "3rd btn default", "4th btn default"]
MODALITIES = ["System modal", "Task modal", "Always-on-top"]
OTHER_OPTIONS = ["Add help btn", "Right-justified", "Right-to-left"]


def make_contents(
    root,
    text,
    width,
    row,
    text1,
    column1,
    text2=None,
    column2=None,
    text3=None,
    column3=None,
):
    txt_canvas = Canvas(root)
    txt_canvas.grid(row=1, column=1, columnspan=4, rowspan=2)
    btn_canvas = Canvas(root)
    btn_canvas.grid(row=3, column=1, columnspan=5)
    lbl = Label(txt_canvas, text=text, height=5, width=50, font=":11")
    lbl.grid(row=0, column=2, rowspan=2)
    btn1 = Button(btn_canvas, text=text1, command=root.destroy, width=width)
    btn1.grid(row=row, column=column1, columnspan=2)
    if text2 and column2:
        btn2 = Button(btn_canvas, text=text2, command=root.destroy, width=width)
        btn2.grid(row=row, column=column2, columnspan=2)
        if text3 and column3:
            btn3 = Button(btn_canvas, text=text3, command=root.destroy, width=width)
            btn3.grid(row=row, column=column3, columnspan=2)
            return [btn1, btn2, btn3]
        return [btn1, btn2]

    return [btn1]


def get_sequence(groups):
    seq = {
        "btn": "OK",
        "icon": None,
        "default_btn": None,
        "modality": None,
        "other_options": [],
    }
    for group in groups:
        if group in BTNS:
            seq["btn"] = group
        elif group in ICONS:
            seq["icon"] = group
        elif group in DEFAULT_BTNS:
            seq["default_btn"] = group
        elif group in MODALITIES:
            seq["modality"] = group
        elif group in OTHER_OPTIONS:
            seq["other_options"].append(group)
    return seq


def make_icon(img_path):
    # Need to set image to global because python's GC deletes the local variable.
    global img
    img = ImageTk.PhotoImage(Image.open(img_path))
    lbl = Label(image=img)
    lbl.grid(row=1, column=1)


def make_msgbox(title, text, option, timeout):
    root = tk.Tk()
    root.title(title)
    root.after(1000 * timeout, root.destroy)
    root.resizable(False, False)
    if isinstance(option, str):
        option = int(option, base=16)
    groups = ALL_COMBINATIONS.get(option, None)
    if groups is None:
        return 1
    groups = groups.split(",")
    seq = get_sequence(groups)

    # Parse Button option
    btn_name = seq["btn"]
    buttons = []
    if btn_name == "OK/Cancel":
        buttons = make_contents(root, text, 15, 1, "OK", 1, "Cancel", 3)
    elif btn_name == "Abort/Retry/Ignore":
        buttons = make_contents(root, text, 10, 2, "Abort", 0, "Retry", 2, "Ignore", 4)
    elif btn_name == "Yes/No/Cancel":
        buttons = make_contents(root, text, 10, 2, "Yes", 0, "No", 2, "Cancel", 4)
    elif btn_name == "Yes/No":
        buttons = make_contents(root, text, 15, 1, "Yes", 1, "No", 3)
    elif btn_name == "Retry/Cancel":
        buttons = make_contents(root, text, 15, 1, "Retry", 1, "Cancel", 3)
    elif btn_name == "Cancel/Try Again/Continue":
        buttons = make_contents(
            root, text, 10, 2, "Cancel", 0, "Try Again", 2, "Continue", 4
        )

    else:
        buttons = make_contents(root, text, 50, 1, "OK", 1)

    # Parse icon option
    icon = seq["icon"]
    if icon == "Icon Hand (stop/error)":
        make_icon("media/icon_hand.png")
    elif icon == "Icon Question":
        make_icon("media/icon_question.png")
    elif icon == "Icon Exclamation":
        make_icon("media/icon_exclamation.png")
    elif icon == "Icon Asterisk (info)":
        make_icon("media/icon_asterisk.png")

    # Parse modality
    modality = seq["modality"]
    if modality == "System modal":
        root.attributes("-topmost", True)
    elif modality == "Task modal":
        root.grab_set()  # untested
    elif modality == "Always-on-top":
        root.attributes("-topmost", True)

    # Parse default button option
    default_btn = seq["default_btn"]
    if len(buttons) == 2 and default_btn == "2nd btn default":
        btn = buttons[1]
        root.bind("<Return>", lambda e, btn=btn: btn.invoke())
    elif len(buttons) == 3 and default_btn == "3rd btn default":
        btn = buttons[2]
        root.bind("<Return>", lambda e, btn=btn: btn.invoke())
    else:
        btn = buttons[0]
        root.bind("<Return>", lambda e, btn=btn: btn.invoke())
    # Need to implement 4th btn default option

    # Parse other options
    # Not implemented yet
    other_options = seq["other_options"]
    for option in other_options:
        if option == "Add help btn":
            pass
        elif option == "Right-justified":
            pass
        elif option == "Right-to-left":
            pass

    root.bind("<Control-c>", root.clipboard_append(text))
    root.mainloop()
    return 0
