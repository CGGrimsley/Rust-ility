import tkinter as tk
from tkinter import ttk
import subprocess
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# Choose the application wanted
def launch_selected_app():
    selected_app = app_combobox.get()
    if selected_app == "Sulfur Calculator":
        subprocess.Popen(["python", "calc.py"])  # Replace with the actual script name
    elif selected_app == "Raid Cost Calculator":
        subprocess.Popen(["python", "raidcost.py"])  # Replace with the actual script name

# Create window
root = ThemedTk(theme="arc")
root.title("Choose an Application")
root.configure(bg="#000")

# Label
ttk.Label(root, text="Choose an Application:").pack(padx=10, pady=10)

style = ttk.Style()
style.configure("TSpinbox", background="black", foreground="grey")
style.configure("TText", background="black", foreground="grey")
style.configure("Dark.TLabel", foreground="grey", background="black")
style.configure("Dark.TButton", foreground="grey", background="black", padding=5)
style.configure("TFrame", background="black")
style.configure("TNotebook", background="grey")

logo_image = Image.open("Rustilitylogo.png")
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttk.Label(root, image=logo_photo, style="Dark.TLabel")

root.iconphoto(True, logo_photo)

# Create a combobox to select the application
app_combobox = ttk.Combobox(root, values=["Sulfur Calculator", "Raid Cost Calculator"])
app_combobox.pack(padx=10, pady=10)
app_combobox.set("Sulfur Calculator")  # Default selection

# Create a button to launch application
ttk.Button(root, text="Launch", command=launch_selected_app).pack(padx=10, pady=10)

root.mainloop()
