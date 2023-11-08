import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

item_costs = {
    "Rocket": 1400,
    "C4": 2200,
    "Satchel": 480,
    "Explosive Round": 25,
    "High Velocity Rocket": 200,
    "Incendiary Rocket": 610,
}

item_ingredients = {
    "Rocket": {"Explosives": 10, "Gunpowder": 150, "Pipes": 2},
    "C4": {"Explosives": 20, "Tech Trash": 2, "Cloth": 5},
    "Satchel": {"Gunpowder": 240, "Metal Fragments": 80, "Rope": 1, "Cloth": 10},
    "Explosive Round": {"Metal Fragments": 10, "Gunpowder": 20, "Sulfur": 10},
    "High Velocity Rocket": {"Pipes": 1, "Gunpowder": 100},
    "Incendiary Rocket": {"Pipes": 2, "Gunpowder": 250, "Low Grade": 250, "Explosives": 1},
}

def calculate_max_items(raw_sulfur):
    max_items = {}
    remaining_sulfur = raw_sulfur
    
    for item, cost in item_costs.items():
        max_item_quantity = int(remaining_sulfur // cost)
        max_items[item] = max_item_quantity
        remaining_sulfur -= max_item_quantity * cost
    
    return max_items

def update_sulfur_allocation_labels(item, spinbox_var):
    update_remaining_sulfur()

def update_remaining_sulfur():
    raw_sulfur = float(raw_sulfur_entry.get())
    remaining_sulfur = raw_sulfur
    
    for item, cost, spinbox_var in zip(item_costs.keys(), item_costs.values(), spinbox_vars):
        quantity = int(spinbox_var.get())
        remaining_sulfur -= quantity * cost
    
    sulfur_allocation_label.config(text=f"Remaining Sulfur: {max(remaining_sulfur, 0):.2f} sulfur")
    
    # Calculate ingredients
    calculate_and_display_ingredients()

def allocate_max(item):
    raw_sulfur = float(raw_sulfur_entry.get())
    max_quantity = min(calculate_max_items(raw_sulfur)[item], raw_sulfur / item_costs[item])

    for spinbox, spinbox_var, spinbox_item in zip(spinboxes, spinbox_vars, item_costs.keys()):
        if spinbox.cget("state") != "disabled" and spinbox.cget("to") != "":
            if spinbox_item == item and spinbox_var.get() != max_quantity:
                spinbox_var.set(max_quantity)

    update_remaining_sulfur()

def submit_sulfur():
    raw_sulfur_input = raw_sulfur_entry.get()
    
    if raw_sulfur_input.isdigit():
        raw_sulfur = float(raw_sulfur_input)
        update_remaining_sulfur()
    else:
        messagebox.showerror("Error", "Please enter a valid whole number for raw sulfur.")

def calculate_and_display_ingredients():
    allocated_items = {}
    for item, spinbox_var in zip(item_costs.keys(), spinbox_vars):
        quantity = int(spinbox_var.get())
        allocated_items[item] = quantity
    
    ingredients_text.config(state=tk.NORMAL)
    ingredients_text.delete("1.0", tk.END)
    
    all_ingredients = {}
    for item, ingredients in item_ingredients.items():
        for ingredient, amount in ingredients.items():
            if ingredient in all_ingredients:
                all_ingredients[ingredient] += amount * allocated_items[item]
            else:
                all_ingredients[ingredient] = amount * allocated_items[item]
    
    ingredients_text.insert(tk.END, "All Ingredients:\n")
    for ingredient, amount in all_ingredients.items():
        ingredients_text.insert(tk.END, f"{amount} {ingredient}\n")
    ingredients_text.insert(tk.END, "\n")
    
    ingredients_text.config(state=tk.DISABLED)

# Create window
root = ThemedTk(theme="arc")
root.title("Rust Sulfur Calculator")
root.configure(bg="#000")

style = ttk.Style()
style.configure("TSpinbox", background="black", foreground="grey")
style.configure("TText", background="black", foreground="grey")
style.configure("Dark.TLabel", foreground="grey", background="black")
style.configure("Dark.TButton", foreground="grey", background="black", padding=5)
style.configure("TFrame", background="black")
style.configure("TNotebook", background="grey")

# Logo
logo_image = Image.open("Rustilitylogo.png")
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttk.Label(root, image=logo_photo, style="Dark.TLabel")

root.iconphoto(True, logo_photo)

# Create notebook w/ tabs
notebook = ttk.Notebook(root, style="TNotebook")
notebook.grid(row=2, column=0, padx=10, pady=10)

# Sulfur allocation tab
allocation_tab = ttk.Frame(notebook, style="TFrame")
notebook.add(allocation_tab, text="Sulfur Allocation")

# Ingredients tab
ingredients_tab = ttk.Frame(notebook, style="TFrame")
notebook.add(ingredients_tab, text="Raid Cost")

# Raw sulfur text box
raw_sulfur_label = ttk.Label(allocation_tab, text="Enter Raw Sulfur:")
raw_sulfur_label.grid(row=0, column=0, padx=5, pady=5)
raw_sulfur_entry = ttk.Entry(allocation_tab)
raw_sulfur_entry.grid(row=0, column=1, padx=5, pady=5)

# Submit button
submit_button = ttk.Button(allocation_tab, text="Submit", command=submit_sulfur)
submit_button.grid(row=0, column=2, padx=5, pady=5)

sulfur_allocation_label = ttk.Label(allocation_tab, text="")
sulfur_allocation_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Spinboxes and buttons
spinboxes = []
spinbox_vars = []
max_buttons = []

for i, item in enumerate(item_costs.keys()):
    label = ttk.Label(allocation_tab, text=f"{item}:", style="TLabel")
    label.grid(row=i + 2, column=0, padx=5, pady=5)
    
    spinbox_var = tk.StringVar()
    spinbox_var.set("0")
    spinbox = ttk.Spinbox(allocation_tab, from_=0, to=1000, textvariable=spinbox_var, command=lambda item=item, spinbox_var=spinbox_var: update_sulfur_allocation_labels(item, spinbox_var), style="TSpinbox")  # Use the configured style for spinboxes
    spinbox.grid(row=i + 2, column=1, padx=5, pady=5)
    
    max_button = ttk.Button(allocation_tab, text="Max", command=lambda item=item: allocate_max(item), style="TButton")
    max_button.grid(row=i + 2, column=2, padx=5, pady=5)
    
    spinboxes.append(spinbox)
    spinbox_vars.append(spinbox_var)
    max_buttons.append(max_button)

# Ingredients text
ingredients_text = tk.Text(ingredients_tab, wrap=tk.WORD, state=tk.DISABLED)
ingredients_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
ingredients_text.configure(bg="#333", fg="white", insertbackground="white")

root.mainloop()