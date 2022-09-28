import time
import tkinter as tk
from tkinter import messagebox

BTNS = {
    0: "OK",
    1: "OK/Cancel",
    2: "Abort/Retry/Ignore",
    3: "Yes/No/Cancel",
    4: "Yes/No",
    5: "Retry/Cancel",
    6: "Cancel/Try Again/Continue",
}
ICONS = {
    16: "Icon Hand (stop/error)",
    32: "Icon Question",
    48: "Icon Exclamation",
    64: "Icon Asterisk (info)",
}
DEFAULT_BTNS = {256: "2nd btn default", 512: "3rd btn default", 768: "4th btn default"}
MODALITIES = {4096: "System modal", 8192: "Task modal", 262144: "Always-on-top"}
OTHER_OPTIONS = {
    16384: "Add help btn",
    524288: "Right-justified",
    1048576: "Right-to-left",
}
ALL_COMBINATIONS = {}
for key, value in BTNS.items():
    ALL_COMBINATIONS[key] = value
for key, value in ICONS.items():
    ALL_COMBINATIONS[key] = value
for key, value in DEFAULT_BTNS.items():
    ALL_COMBINATIONS[key] = value
for key, value in MODALITIES.items():
    ALL_COMBINATIONS[key] = value
for key, value in OTHER_OPTIONS.items():
    ALL_COMBINATIONS[key] = value


def make_option_combinations(*args):
    base_value = args[0]
    args = args[1:]
    base_key = sum(args)
    first_option = OTHER_OPTIONS[16384]
    second_option = OTHER_OPTIONS[524288]
    third_option = OTHER_OPTIONS[1048576]
    ALL_COMBINATIONS[base_key + 16384] = "{},{}".format(base_value, first_option)
    ALL_COMBINATIONS[base_key + 524288] = "{},{}".format(base_value, second_option)
    ALL_COMBINATIONS[base_key + 1024576] = "{},{}".format(base_value, third_option)
    ALL_COMBINATIONS[base_key + 16384 + 524288] = "{},{},{}".format(
        base_value, first_option, second_option
    )
    ALL_COMBINATIONS[base_key + 524288 + 1042576] = "{},{},{}".format(
        base_value, second_option, third_option
    )

    ALL_COMBINATIONS[base_key + 16384 + 1042576] = "{},{},{}".format(
        base_value, first_option, third_option
    )
    ALL_COMBINATIONS[base_key + 16384 + 524288 + 1042576] = "{},{},{},{}".format(
        base_value, first_option, second_option, third_option
    )


def get_value_combinations(
    btn,
    btn_desc,
    icon,
    icon_desc,
    default_btn,
    default_btn_desc,
    modality,
    modality_desc,
):
    combinations = {}
    combinations[btn + icon] = "{},{}".format(btn_desc, icon_desc)
    combinations[btn + default_btn] = "{},{}".format(btn_desc, default_btn_desc)
    combinations[btn + modality] = "{},{}".format(btn_desc, modality_desc)
    combinations[btn + icon + default_btn] = "{},{},{}".format(
        btn_desc, icon_desc, default_btn_desc
    )
    combinations[btn + icon + modality] = "{},{},{}".format(
        btn_desc, icon_desc, modality_desc
    )
    combinations[btn + default_btn + modality] = "{},{},{}".format(
        btn_desc, default_btn_desc, modality_desc
    )
    combinations[icon + default_btn] = "{},{}".format(icon_desc, default_btn_desc)
    combinations[icon + modality] = "{},{}".format(icon_desc, modality_desc)
    combinations[icon + default_btn + modality] = "{},{},{}".format(
        icon_desc, default_btn_desc, modality_desc
    )
    combinations[default_btn + modality] = "{},{}".format(
        default_btn_desc, modality_desc
    )
    combinations[btn + icon + default_btn + modality] = "{},{},{},{}".format(
        btn_desc, icon_desc, default_btn_desc, modality_desc
    )
    return combinations


def parse_option(option):
    for btn in BTNS.keys():
        for icon in ICONS.keys():
            for default_btn in DEFAULT_BTNS.keys():
                for modality in MODALITIES.keys():
                    values = get_value_combinations(
                        btn,
                        BTNS[btn],
                        icon,
                        ICONS[icon],
                        default_btn,
                        DEFAULT_BTNS[default_btn],
                        modality,
                        MODALITIES[modality],
                    )
                    for key, value in values.items():
                        ALL_COMBINATIONS[key] = value
                    value = (
                        BTNS[btn]
                        + ICONS[icon]
                        + DEFAULT_BTNS[default_btn]
                        + MODALITIES[modality]
                    )
                    make_option_combinations(value, btn, icon, default_btn, modality)
    return ALL_COMBINATIONS.get(option, None)


def make_msgbox(title, text, option, timeout):
    root = tk.Tk()
    root.withdraw()
    if isinstance(option, str):
        option = int(option, base=16)
    groups = parse_option(option)
    if groups is None:
        return 1
    groups = groups.split(",")
    if groups[0] == "OK":
        messagebox.showinfo(title, text)
    elif groups[0] == "OK/Cancel":
        messagebox.askokcancel(title, text)
    elif groups[0] == "Abort/Retry/Ignore":
        messagebox.showinfo(title, text)
    elif groups[0] == "Yes/No/Cancel":
        messagebox.askyesnocancel(title, text)
    elif groups[0] == "Yes/No":
        messagebox.askyesno(title, text)
    elif groups[0] == "Retry/Cancel":
        messagebox.askretrycancel(title, text)
    elif groups[0] == "Cancel/Try Again/Continue":
        messagebox.showinfo(title, text)
