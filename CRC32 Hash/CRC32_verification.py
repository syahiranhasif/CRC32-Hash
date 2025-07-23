import os
import binascii
import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar
from tkinterdnd2 import TkinterDnD, DND_FILES

# CRC32 presets
known_crc32s = {
    "OMNIA/LV/PHOENIX": "BA1DED31",
    "ENTRY/LV": "6477BBA7",
    "BASIC/LV": "932EA465"
}

# Set theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Main windows
base = TkinterDnD.Tk()
base.withdraw()  # Hide base root
app = ctk.CTkToplevel(base)
selected_crc = StringVar(master=app, value="")

# ✅ Get CRC32 from file
def get_crc32(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            crc = binascii.crc32(data) & 0xFFFFFFFF
            return f"{crc:08X}"
    except Exception as e:
        return f"Error: {e}"

# File check logic
def check_file(file_path):
    if not os.path.isfile(file_path):
        return
    file_crc = get_crc32(file_path)
    expected_crc = known_crc32s[selected_crc.get()]
    status = "✅ MATCH" if file_crc == expected_crc else "❌ MISMATCH"
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    textbox.insert("0.0", f"📁 File: {file_path}\n\n🔑 CRC32: {file_crc}\n🎯 Expected: {expected_crc}\n\n📊 Result: {status}")
    textbox.configure(state="disabled")

# Browse file
def browse_and_check():
    file_path = filedialog.askopenfilename()
    if file_path:
        check_file(file_path)

# Drag-and-drop file
def on_drop(event):
    file_path = event.data.strip().strip("{}")
    check_file(file_path)

# Theme toggle
def toggle_theme():
    ctk.set_appearance_mode("light" if theme_switch.get() else "dark")

# Proper app close (fix zombie process)
def close_all():
    app.destroy()
    base.destroy()

# GUI Layout
app.title("CRC32 Hash")
app.geometry("640x560")
app.resizable(False, False)
app.drop_target_register(DND_FILES)
app.dnd_bind("<<Drop>>", on_drop)
app.protocol("WM_DELETE_WINDOW", close_all)  # 👈 Proper shutdown

ctk.CTkLabel(app, text="📁 Drag or Browse File to Check CRC32", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

radio_frame = ctk.CTkFrame(app)
radio_frame.pack(pady=5)
ctk.CTkLabel(radio_frame, text="Select CRC32 to Match:").pack(anchor="w", padx=10)

for key in known_crc32s:
    ctk.CTkRadioButton(
        radio_frame,
        text=key,
        variable=selected_crc,
        value=key,
        font=ctk.CTkFont(size=12),       # Smaller font
        text_color="#0EA0F5",            # Subtle dark text
        radiobutton_height=12            # Optional: you can tweak height
    ).pack(anchor="w", padx=10, pady=2)

ctk.CTkButton(app, text="Browse File", command=browse_and_check).pack(pady=10)

textbox = ctk.CTkTextbox(app, width=560, height=220, font=("Consolas", 11))
textbox.pack(pady=10)
textbox.insert("0.0", "Output will appear here...")
textbox.configure(state="disabled")

theme_switch = ctk.CTkSwitch(app, text="☀️ Light / 🌙 Dark", command=toggle_theme)
theme_switch.pack(pady=5)
theme_switch.select()

ctk.CTkLabel(app, text="v1.4.2", font=ctk.CTkFont(size=8), text_color="#888888").pack(anchor="se", padx=6, pady=(0, 1))
ctk.CTkLabel(app, text="syhiranhasf", font=ctk.CTkFont(size=8, slant="italic"), text_color="#aaaaaa").pack(anchor="se", padx=6, pady=(0, 6))

# Start app
app.mainloop()
