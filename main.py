import tkinter as tk
from tkinter import ttk
import subprocess

# Function to launch the selected application
def launch_selected_app():
    selected_app = app_combobox.get()
    if selected_app == "Sulfur Calculator":
        subprocess.Popen(["python", "calc.py"])  # Replace with the actual script name
    elif selected_app == "Raid Cost Calculator":
        subprocess.Popen(["python", "raidcost.py"])  # Replace with the actual script name

# Create the main window
root = tk.Tk()
root.title("Choose an Application")

# Create a label
ttk.Label(root, text="Choose an Application:").pack(padx=10, pady=10)

# Create a combobox to select the application
app_combobox = ttk.Combobox(root, values=["Sulfur Calculator", "Raid Cost Calculator"])
app_combobox.pack(padx=10, pady=10)
app_combobox.set("Sulfur Calculator")  # Default selection

# Create a button to launch the selected application
ttk.Button(root, text="Launch", command=launch_selected_app).pack(padx=10, pady=10)

# Run the GUI
root.mainloop()
