import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

items_data = {
    "Wood Door": {"Destructive Items": {"Rocket": 0, "Explosive Ammo": 0, "Molotov": 2}},
    "Wood Door (Eoka)": {"Destructive Items": {"Rocket": 0, "Explosive Ammo": 0, "Molotov": 0, "Handmade shells": 45}},
    "Ladder Hatch": {"Destructive Items": {"Rocket": 1, "Explosive Ammo": 8, "Molotov": 0}},
    "Sheet Metal Door": {"Destructive Items": {"Rocket": 1, "Explosive Ammo": 8, "Molotov": 0}},
    "Garage Door": {"Destructive Items": {"Rocket": 1, "Explosive Ammo": 0, "C4": 1}},
    "Armored Door": {"Destructive Items": {"Rocket": 1, "Explosive Ammo": 0, "C4": 2}},
    "Wood Wall": {"Destructive Items": {"Rocket": 0, "Explosive Ammo": 0, "Molotov": 4}},
    "Stone Wall": {"Destructive Items": {"Rocket": 4, "Explosive Ammo": 0, "Molotov": 0}},
    "Sheet Metal Wall": {"Destructive Items": {"Rocket": 8, "Explosive Ammo": 0, "Molotov": 0}},
    "Armored Wall": {"Destructive Items": {"Rocket": 15, "Explosive Ammo": 0, "Molotov": 0}},
    "Wood High External": {"Destructive Items": {"Rocket": 0, "Explosive Ammo": 0, "Incendiary Rocket": 1}},
    "Stone High External": {"Destructive Items": {"Rocket": 4, "Explosive Ammo": 0, "Incendiary Rocket": 0}},
    "Auto-Turret": {"Destructive Items": {"Rocket": 0, "Explosive Ammo": 0, "High Velocity Rocket": 3}},
}

# update raid cost
def update_raid_cost():
    raid_cost.delete(0, tk.END)  # Clear the Raid Cost

    stacked_items = {}  # Dictionary to stack D_Items for all C_Items
    for item, spinbox in spinboxes.items():
        quantity = int(spinbox.get())
        if quantity > 0:
            destructive_items = items_data[item]["Destructive Items"]
            for destructive_item, amount_needed in destructive_items.items():
                if destructive_item in stacked_items:
                    stacked_items[destructive_item] += quantity * amount_needed
                else:
                    stacked_items[destructive_item] = quantity * amount_needed

    # Display the stacked D_Items in the raid cost
    for destructive_item, total_quantity in stacked_items.items():
        raid_cost.insert(tk.END, f"{total_quantity} {destructive_item}")

root = ThemedTk(theme="arc")
root.title("Rust Raid Calculator")
root.configure(bg="#000")

items_frame = ttk.Frame(root)
items_frame.grid(row=0, column=0, padx=10, pady=10)

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

spinboxes = {}
row_counter = 0
for item in items_data.keys():
    ttk.Label(items_frame, text=item).grid(row=row_counter, column=0, padx=10, pady=5)
    spinbox = tk.StringVar()
    spinbox.set("0")
    ttk.Entry(items_frame, textvariable=spinbox, width=5).grid(row=row_counter, column=1, padx=10, pady=5)
    ttk.Button(items_frame, text="+", command=lambda s=spinbox: s.set(int(s.get()) + 1)).grid(row=row_counter, column=2, padx=5, pady=5)
    ttk.Button(items_frame, text="-", command=lambda s=spinbox: s.set(max(int(s.get()) - 1, 0))).grid(row=row_counter, column=3, padx=5, pady=5)
    spinboxes[item] = spinbox
    row_counter += 1

raidcost_frame = ttk.Frame(root)
raidcost_frame.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(raidcost_frame, text="Raid Cost:").pack(padx=10, pady=10)

raid_cost = tk.Listbox(raidcost_frame, selectmode=tk.SINGLE)
raid_cost.pack(padx=10, pady=10)

ttk.Button(raidcost_frame, text="Update Raid Cost", command=update_raid_cost).pack(padx=10, pady=10)

root.mainloop()
