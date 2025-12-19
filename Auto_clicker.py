import threading
import time
import keyboard
import json
import os
import ttkbootstrap as tb
from tkinter import messagebox

CONFIG_FILE = "config.json"

running = False
KEY_TO_PRESS = None
DELAY = 0.1


# ---------------- CONFIG ----------------

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"key": "f", "delay": 0.1}


def save_config(key, delay):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"key": key, "delay": delay}, f)


config = load_config()


# ---------------- WORKER ----------------

def key_spammer():
    while True:
        if running:
            keyboard.press_and_release(KEY_TO_PRESS)
            time.sleep(DELAY)
        else:
            time.sleep(0.1)


def toggle():
    global running
    running = not running
    status_lbl.config(
        text="RUNNING" if running else "STOPPED",
        bootstyle="success" if running else "danger"
    )


def exit_program():
    print("Exiting...")
    keyboard.unhook_all_hotkeys()
    app.destroy()


# ---------------- START ----------------

def start_app():
    global KEY_TO_PRESS, DELAY

    key = key_var.get().strip().lower()
    custom = custom_entry.get().strip().lower()
    KEY_TO_PRESS = custom if custom else key

    if not KEY_TO_PRESS:
        messagebox.showerror("Error", "Please select or enter a key")
        return

    try:
        DELAY = float(delay_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid delay value")
        return

    save_config(KEY_TO_PRESS, DELAY)

    status_lbl.config(text="READY", bootstyle="info")


# ---------------- UI ----------------

app = tb.Window(themename="darkly")
app.title("Keyboard Auto Clicker")
app.geometry("420x380")
app.resizable(False, False)

tb.Label(app, text="Keyboard Auto Clicker", font=("Segoe UI", 18, "bold")).pack(pady=15)

frame = tb.Frame(app)
frame.pack(pady=10)

tb.Label(frame, text="Select common key").grid(row=0, column=0, sticky="w")
key_var = tb.StringVar(value=config["key"])

tb.Combobox(
    frame,
    textvariable=key_var,
    values=[
        "a","b","c","d","e","f","w","s",
        "space","enter","tab","shift","ctrl","alt","esc"
    ],
    width=25
).grid(row=1, column=0, pady=5)

tb.Label(frame, text="Or enter custom key").grid(row=2, column=0, sticky="w")
custom_entry = tb.Entry(frame, width=27)
custom_entry.grid(row=3, column=0, pady=5)

tb.Label(frame, text="Delay (seconds)").grid(row=4, column=0, sticky="w")
delay_entry = tb.Entry(frame, width=27)
delay_entry.insert(0, str(config["delay"]))
delay_entry.grid(row=5, column=0, pady=5)

status_lbl = tb.Label(app, text="STOPPED", bootstyle="danger", font=("Segoe UI", 11, "bold"))
status_lbl.pack(pady=10)

tb.Button(app, text="APPLY SETTINGS", bootstyle="primary", width=20, command=start_app).pack(pady=5)
tb.Button(app, text="EXIT", bootstyle="danger", width=20, command=exit_program).pack(pady=5)

tb.Label(app, text="F11 → Start / Stop\nEsc → Exit", font=("Segoe UI", 9)).pack(pady=10)

# ---------------- HOTKEYS ----------------

keyboard.add_hotkey("F11", toggle)
keyboard.add_hotkey("esc", exit_program)

# Start worker thread
threading.Thread(target=key_spammer, daemon=True).start()

app.mainloop()
