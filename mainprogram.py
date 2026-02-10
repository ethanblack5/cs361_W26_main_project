import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kitchen Inventory Organizer")
        self.geometry("1000x1000")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=1)
        self.inventory = {}
        self.frames = {}
        self.recipes = {}
        self.lists = {}
        self.kitchen = []
        self.selected_recipe = tk.StringVar(value="")
        self.selected_list = tk.StringVar(value="")
        self.locations = []              
        self.selected_location = tk.StringVar(value="")

        for F in (HomePage, 
                  Inventory, AddItem, RemoveItem, ImportList, DesignKitchen, SearchInventory,     ## inventory classes
                  Recipes, AddRecipe, ViewRecipe, RemoveRecipe,                                     ## recipe classes
                  GroceryLists, AddList, ViewList, RemoveList,                                      ## list classes
                  UsableRecipes, 
                  Calendar, AddEvent, RemoveEvent, ViewEvent,                                       ## calendar classes
                  HelpPage):                  
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

    def add_inventory_item(self, item_name, qty, location, last_bought):
        self.inventory[item_name] = {
            "Quantity": qty,
            "Location": location,
            "Last Bought": last_bought
        }

        if location not in self.kitchen:
            self.kitchen.append(location)

        return
    
    def add_location(self, location_name):
        location_name = location_name.strip()
        if not location_name:
            return False
        if location_name not in self.locations:
            self.locations.append(location_name)
            self.locations.sort()
        return True

    def get_locations(self):
        for location in self.kitchen:
            print(location)
        return
    
    def add_recipe(self, name, prep_time, cook_time, ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, qty1, qty2, qty3, qty4, qty5, qty6, qty7, qty8, qty9, qty10, instructions):
        self.recipes[name] = {
            "Ingredient 1": ing1,    "Ingredient 1 Quantity": qty1,
            "Ingredient 2": ing2,    "Ingredient 2 Quantity": qty2,
            "Ingredient 3": ing3,    "Ingredient 3 Quantity": qty3,
            "Ingredient 4": ing4,    "Ingredient 4 Quantity": qty4,
            "Ingredient 5": ing5,    "Ingredient 5 Quantity": qty5,
            "Ingredient 6": ing6,    "Ingredient 6 Quantity": qty6,
            "Ingredient 7": ing7,    "Ingredient 7 Quantity": qty7,
            "Ingredient 8": ing8,    "Ingredient 8 Quantity": qty8,
            "Ingredient 9": ing9,    "Ingredient 9 Quantity": qty9,
            "Ingredient 10": ing10,  "Ingredient 10 Quantity": qty10,
            "Prep Time": prep_time,  "Cook Time": cook_time,
            "Instructions": instructions
        }
        return
    
    def get_recipe(self, recipe_name):
        return
    
    def remove_inventory_item(self, item_name):
        item_name = item_name.strip()
        if item_name in self.inventory:
            del self.inventory[item_name]
            return True
        return False
    
    def remove_recipe(self, recipe_name):
        recipe_name = recipe_name.strip()
        if recipe_name in self.recipes:
            del self.recipes[recipe_name]
            return True
        return False
    
    def add_list(self, list_name, items, notes):
        self.lists[list_name] = {
            "items": items,      
            "notes": notes
        }

    def remove_list(self, list_name):
        list_name = list_name.strip()
        if list_name in self.lists:
            del self.lists[list_name]
            return True
        return False
    
    def import_inventory_items(self, lines, default_location="", default_last_bought=""):
        for item in lines:
            name = (item.get("name") or "").strip()
            if not name:
                continue
            qty = item.get("qty", 0)
            self.add_inventory_item(name, qty, default_location, default_last_bought)
    

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Keep track of your kitchen and minimize food waste!", font=('Arial', 20)).pack(side=tk.BOTTOM, pady=20)

        tk.Label(self, text="Welcome! Please choose an option.", font=("Arial", 20)).pack(pady=20)
        tk.Button(self, text="Inventory", command=lambda: controller.show_frame(Inventory)).pack(side=tk.LEFT)
        tk.Button(self, text="Recipes", command=lambda: controller.show_frame(Recipes)).pack(side=tk.LEFT)
        tk.Button(self, text="Grocery Lists", command=lambda: controller.show_frame(GroceryLists)).pack(side=tk.LEFT)
        tk.Button(self, text="Calendar", command=lambda: controller.show_frame(Calendar)).pack(side=tk.LEFT)
        tk.Button(self, text="Usable Recipes", command=lambda: controller.show_frame(UsableRecipes)).pack(side=tk.LEFT)
        tk.Button(self, text="Help", command=lambda: controller.show_frame(HelpPage)).pack(side=tk.LEFT)

class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Help", font=("Arial", 20)).pack(pady=20)
        htext = "While navigating through this program, first confirm which option you want\n" \
                "to do at the bottom of the screen. Then, depending on that button's function, the \n" \
                "program will change to your specifications.\n" \
                "\n" \
                "This program will always prompt you to confirm removing or deleting any data, just in case.\n" \
                "\n" \
                "Plan grocery trips to calendars, recipes to your cookbook, prepare grocery lists,\n" \
                "items to your kitchen or figure out what recipes you can make based on the food already in your\n" \
                "kitchen.\n" \
                "\n" \
                "Enjoy!"
        help_txt = tk.Label(self, text=htext, font=('Arial', 14))
        help_txt.pack()
        tk.Button(self, text="Back", command=lambda: controller.show_frame(HomePage)).pack(side=tk.LEFT)

class Inventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Your Inventory", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        b1 = tk.Button(button_frame, text="Add Item", command=lambda: controller.show_frame(AddItem))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(button_frame, text="Remove Item", command=lambda: controller.show_frame(RemoveItem))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

        b3 = tk.Button(button_frame, text="Home", command=lambda: controller.show_frame(HomePage))
        b3.pack(side=tk.LEFT, padx=5, pady=5)

        b4 = tk.Button(button_frame, text="Design", command=lambda: controller.show_frame(DesignKitchen))
        b4.pack(side=tk.LEFT, padx=5, pady=5)

        b5 = tk.Button(button_frame, text="Search", command=lambda: controller.show_frame(SearchInventory))
        b5.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh(self):
        for i in self.list_frame.winfo_children():
            i.destroy()

        inventory = self.controller.inventory

        if not inventory:
            tk.Label(self.list_frame, text="No items yet. Click 'Add Item' to start.", font=("Arial", 14)).pack(anchor="w")
            return

        header = tk.Frame(self.list_frame)
        header.pack(fill="x", pady=(0, 6))

        tk.Label(header, text="Item", width=20, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Qty", width=10, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Location", width=20, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
        tk.Label(header, text="Last Bought", width=15, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=3, sticky="w")

        for row, (name, data) in enumerate(inventory.items(), start=1):
            row = tk.Frame(self.list_frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=name, width=20, anchor="w").grid(row=0, column=0, sticky="w")
            tk.Label(row, text=str(data.get("Quantity", "")), width=10, anchor="w").grid(row=0, column=1, sticky="w")
            tk.Label(row, text=data.get("Location", ""), width=20, anchor="w").grid(row=0, column=2, sticky="w")
            tk.Label(row, text=data.get("Last Bought", ""), width=15, anchor="w").grid(row=0, column=3, sticky="w")


class SearchInventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Search Item", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        search_row = tk.Frame(self)
        search_row.pack(fill="x", padx=20, pady=(0, 10))

        
        tk.Label(search_row, text="Search:").pack(side=tk.LEFT)

        self.search_var = tk.StringVar(value="")
        search_entry = tk.Entry(search_row, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=8)

        tk.Button(search_row, text="Clear", command=lambda: self.search_var.set("")).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Back", command=lambda: controller.show_frame(Inventory)).pack(side=tk.LEFT)

        self.search_var.trace_add("write", lambda *_: self.refresh())

    def refresh(self):
        for i in self.list_frame.winfo_children():
            i.destroy()

        inv = self.controller.inventory
        search_query = self.search_var.get().strip().lower()

        items = list(inv.items())
        if search_query:
            items = [(name, data)
                    for (name, data) in items
                    if search_query in name.lower()
                    or search_query in str(data.get("Location", "")).lower()
                    or search_query in str(data.get("Last Bought", "")).lower()]

        if not inv:
            tk.Label(self.list_frame, text="No items yet. Click 'Add Item' to start.").pack(anchor="w")
            return

        if search_query and not items:
            tk.Label(self.list_frame, text="No matching items found.").pack(anchor="w")
            return

        header = tk.Frame(self.list_frame)
        header.pack(fill="x", pady=(0, 6))

        tk.Label(header, text="Item", width=20, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Qty", width=10, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Location", width=20, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w")
        tk.Label(header, text="Last Bought", width=15, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=3, sticky="w")

        for name, data in items:
            row = tk.Frame(self.list_frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=name, width=20, anchor="w").grid(row=0, column=0, sticky="w")
            tk.Label(row, text=str(data.get("Quantity", "")), width=10, anchor="w").grid(row=0, column=1, sticky="w")
            tk.Label(row, text=data.get("Location", ""), width=20, anchor="w").grid(row=0, column=2, sticky="w")
            tk.Label(row, text=data.get("Last Bought", ""), width=15, anchor="w").grid(row=0, column=3, sticky="w")




class AddItem(tk.Frame):                        ## inventory page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Add Item", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Item Name").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.item = tk.Entry(form_frame, width=20)
        self.item.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Quantity").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.quantity = tk.Entry(form_frame, width=20)
        self.quantity.grid(row=1, column=1, padx=10, pady=5)

        self.location_var = tk.StringVar(value="")
        tk.Label(form_frame, text="Location").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.location_box = ttk.Combobox(form_frame, textvariable=self.location_var, values=self.controller.locations, state="readonly")
        self.location_box.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(form_frame, text="Last Bought (MM/DD/YYYY)").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.lb = tk.Entry(form_frame, width=20)
        self.lb.grid(row=3, column=1, padx=10, pady=5)

        b1 = tk.Button(button_frame, text="Confirm", command=self.when_confirm_pressed)
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(button_frame, text="Cancel", command=lambda: controller.show_frame(Inventory))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

        b3 = tk.Button(button_frame, text="Import", command=lambda: controller.show_frame(ImportList))
        b3.pack(side=tk.LEFT, padx=5, pady=5)

    def when_confirm_pressed(self):
        item_name = self.item.get().strip()
        qty_text = self.quantity.get().strip()
        location = self.location_var.get().strip()
        last_bought = self.lb.get().strip()

        if not item_name:
            print("Item name required.")
            return
        
        qty = float(qty_text) if qty_text else 0

        self.controller.add_inventory_item(item_name=item_name, qty=qty, location=location, last_bought=last_bought)
        self.item.delete(0, tk.END)
        self.quantity.delete(0, tk.END)

        if self.controller.locations:
            self.location_var.set(self.controller.locations[0])
        else:
            self.location_var.set("")

        self.lb.delete(0, tk.END)
        self.controller.show_frame(Inventory)

    def refresh(self):
        self.location_box["values"] = self.controller.locations

        if self.controller.locations and not self.location_var.get():
            self.location_var.set(self.controller.locations[0])
            


class RemoveItem(tk.Frame):                     ## inventory page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Remove Item", font=("Arial", 20)).pack(pady=20)

        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="Select item:").pack(side=tk.LEFT, padx=5)

        self.selected_item = tk.StringVar(value="")
        self.item_box = ttk.Combobox(row, textvariable=self.selected_item, values=[], state="readonly", width=30)
        self.item_box.pack(side=tk.LEFT, padx=5)

        self.message = tk.Label(self, text="", fg="red")
        self.message.pack(pady=(5, 0))

        buttons = tk.Frame(self)
        buttons.pack(side=tk.BOTTOM, pady=15)

        tk.Button(buttons, text="Remove", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Back", command=lambda: controller.show_frame(Inventory)).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        names = sorted(self.controller.inventory.keys())
        self.item_box["values"] = names

        if names:
            self.selected_item.set(names[0])
            self.message.config(text="")
        else:
            self.selected_item.set("")
            self.message.config(text="No items to remove.", fg="red")

    def remove_selected(self):
        name = self.selected_item.get()
        if not name:
            self.message.config(text="Select an item first.", fg="red")
            return

        if not messagebox.askyesno("Confirm", f"Remove '{name}'?"):
            return

        removed = self.controller.remove_inventory_item(name)
        if removed:
            self.message.config(text=f"Removed: {name}", fg="green")
            self.refresh()
            self.controller.show_frame(Inventory)
        else:
            self.message.config(text="Item not found.", fg="red")


class ImportList(tk.Frame):                    ## inventory page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Import Items", font=("Arial", 20)).pack(pady=20)

        help_text = ("Copy and paste any lists you have within this program below!")
        tk.Label(self, text=help_text, justify="left").pack(anchor="w", padx=15)

        defaults = tk.Frame(self)
        defaults.pack(fill="x", padx=15, pady=(10, 0))

        tk.Label(defaults, text="Default Location:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.location_var = tk.StringVar(value="")
        self.location_box = ttk.Combobox(defaults, textvariable=self.location_var, values=self.controller.locations, state="readonly", width=25)
        self.location_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(defaults, text="Default Last Bought:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.last_bought_entry = tk.Entry(defaults, width=20)
        self.last_bought_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        self.text = ScrolledText(self, height=18, wrap=tk.WORD)
        self.text.pack(fill="both", expand=True, padx=15, pady=10)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="Go Back", command=lambda: controller.show_frame(AddItem)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Confirm Import", command=self.confirm_import).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        self.location_box["values"] = self.controller.locations
        if self.controller.locations and not self.location_var.get():
            self.location_var.set(self.controller.locations[0])
        elif not self.controller.locations:
            self.location_var.set("")

    def parse_lines(self, raw: str):

        items = []
        for line in raw.splitlines():
            s = line.strip()
            if not s:
                continue

            name = s
            qty = 0.0

            if " - " in s:
                left, right = s.split(" - ", 1)
                name = left.strip()
                try:
                    qty = float(right.strip())
                except:
                    qty = 0.0

            items.append({"name": name, "qty": qty})
        return items

    def confirm_import(self):
        raw = self.text.get("1.0", tk.END).strip()
        if not raw:
            self.msg.config(text="Paste at least one item line to import.", fg="red")
            return

        default_location = self.location_var.get().strip()
        default_last_bought = self.last_bought_entry.get().strip()

        parsed = self.parse_lines(raw)
        if not parsed:
            self.msg.config(text="No valid lines found.", fg="red")
            return

        for item in parsed:
            name = item["name"].strip()
            if not name:
                continue
            self.controller.add_inventory_item(item_name=name, qty = item.get("qty", 0.0), location=default_location, last_bought=default_last_bought)

        self.text.delete("1.0", tk.END)
        self.last_bought_entry.delete(0, tk.END)
        self.msg.config(text=f"Imported {len(parsed)} item(s).", fg="green")
        self.controller.show_frame(Inventory)

class DesignKitchen(tk.Frame):                   ## inventory page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Design Kitchen", font=("Arial", 20)).pack(pady=20)

        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="New Location:").pack(side=tk.LEFT, padx=5)
        self.location_entry = tk.Entry(row, width=25)
        self.location_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(row, text="Add", command=self.on_add_location).pack(side=tk.LEFT, padx=5)
        tk.Button(row, text="Back", command=lambda: controller.show_frame(Inventory)).pack(side=tk.LEFT, padx=5)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack()

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def on_add_location(self):
        loc = self.location_entry.get()
        if self.controller.add_location(loc):
            self.location_entry.delete(0, tk.END)
            self.msg.config(text="Added!", fg="green")
            self.refresh()
        else:
            self.msg.config(text="Enter a location name.", fg="red")

    def refresh(self):
        for i in self.list_frame.winfo_children():
            i.destroy()

        if not self.controller.locations:
            tk.Label(self.list_frame, text="No locations yet. Add one above.").pack(anchor="w")
            return

        for loc in self.controller.locations:
            tk.Label(self.list_frame, text=f"• {loc}").pack(anchor="w")


class Recipes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Your Recipes", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)


        b1 = tk.Button(button_frame, text="Add Recipe", command=lambda: controller.show_frame(AddRecipe))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(button_frame, text="Remove Recipe", command=lambda: controller.show_frame(RemoveRecipe))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

        b3 = tk.Button(button_frame, text="Go Home", command=lambda: controller.show_frame(HomePage))
        b3.pack(side=tk.LEFT, padx=5, pady=5)

        b4 = tk.Button(button_frame, text="View", command=lambda: controller.show_frame(ViewRecipe))
        b4.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh(self):
        for i in self.list_frame.winfo_children():
            i.destroy()

        sel = self.controller.selected_recipe.get()
        if sel not in self.controller.recipes:
            self.controller.selected_recipe.set("")

        for name in self.controller.recipes.keys():
            tk.Radiobutton(self.list_frame, text=name, variable=self.controller.selected_recipe, value=name, anchor="w", justify="left").pack(fill="x", anchor="w")

    def view_selected(self):
        name = self.controller.selected_recipe.get()
        if not name:
            self.msg.config(text="Select a recipe first.")
            return
        self.msg.config(text="")
        self.controller.show_frame(ViewRecipe)

class AddRecipe(tk.Frame):                            ## recipe page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Add Recipe", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        form = tk.Frame(self)
        form.pack(anchor="nw", padx=10, pady=10)

        ## Ingredients/Recipe Name/Prep/Cook Time
        tk.Label(form, text="Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name = tk.Entry(form, width=30)
        self.name.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Prep Time").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.prep_time = tk.Entry(form, width=30)
        self.prep_time.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Cook Time").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cook_time = tk.Entry(form, width=30)
        self.cook_time.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 1").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.i1 = tk.Entry(form, width=30)
        self.i1.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 2").grid(row=3, column=2, sticky="e", padx=5, pady=5)
        self.i2 = tk.Entry(form, width=30)
        self.i2.grid(row=3, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 3").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.i3 = tk.Entry(form, width=30)
        self.i3.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 4").grid(row=4, column=2, sticky="e", padx=5, pady=5)
        self.i4 = tk.Entry(form, width=30)
        self.i4.grid(row=4, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 5").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.i5 = tk.Entry(form, width=30)
        self.i5.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 6").grid(row=5, column=2, sticky="e", padx=5, pady=5)
        self.i6 = tk.Entry(form, width=30)
        self.i6.grid(row=5, column=3, sticky="w", padx=5, pady=5)
        
        tk.Label(form, text="Ingredient 7").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.i7 = tk.Entry(form, width=30)
        self.i7.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 8").grid(row=6, column=2, sticky="e", padx=5, pady=5)
        self.i8 = tk.Entry(form, width=30)
        self.i8.grid(row=6, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 9").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.i9 = tk.Entry(form, width=30)
        self.i9.grid(row=7, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 10").grid(row=7, column=2, sticky="e", padx=5, pady=5)
        self.i10 = tk.Entry(form, width=30)
        self.i10.grid(row=7, column=3, sticky="w", padx=5, pady=5)

        ## Quantites
        tk.Label(form, text="Ingredient 1 Quantity").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.q1 = tk.Entry(form, width=30)
        self.q1.grid(row=8, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 2 Quantity").grid(row=8, column=2, sticky="e", padx=5, pady=5)
        self.q2 = tk.Entry(form, width=30)
        self.q2.grid(row=8, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 3 Quantity").grid(row=9, column=0, sticky="e", padx=5, pady=5)
        self.q3 = tk.Entry(form, width=30)
        self.q3.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 4 Quantity").grid(row=9, column=2, sticky="e", padx=5, pady=5)
        self.q4 = tk.Entry(form, width=30)
        self.q4.grid(row=9, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 5 Quantity").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.q5 = tk.Entry(form, width=30)
        self.q5.grid(row=10, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 6 Quantity").grid(row=10, column=2, sticky="e", padx=5, pady=5)
        self.q6 = tk.Entry(form, width=30)
        self.q6.grid(row=10, column=3, sticky="w", padx=5, pady=5)
        
        tk.Label(form, text="Ingredient 7 Quantity").grid(row=11, column=0, sticky="e", padx=5, pady=5)
        self.q7 = tk.Entry(form, width=30)
        self.q7.grid(row=11, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 8 Quantity").grid(row=11, column=2, sticky="e", padx=5, pady=5)
        self.q8 = tk.Entry(form, width=30)
        self.q8.grid(row=11, column=3, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 9 Quantity").grid(row=12, column=0, sticky="e", padx=5, pady=5)
        self.q9 = tk.Entry(form, width=30)
        self.q9.grid(row=12, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form, text="Ingredient 10 Quantity").grid(row=12, column=2, sticky="e", padx=5, pady=5)
        self.q10 = tk.Entry(form, width=30)
        self.q10.grid(row=12, column=3, sticky="w", padx=5, pady=5)

        ## Instructions
        tk.Label(form, text="Instructions").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.instructions = ScrolledText(form, height=10, width=50, wrap=tk.WORD)
        self.instructions.grid(row=15, column=1, sticky="e", padx=5, pady=5)

        b1 = tk.Button(self, text="Confirm", command=self.when_confirm_pressed)
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(self, text="Cancel", command=lambda: controller.show_frame(Recipes))
        b2.pack(side=tk.LEFT, padx=5, pady=5)
    
    def when_confirm_pressed(self):
        recipe_name = self.name.get().strip()
        prep_time = self.prep_time.get().strip()
        cook_time = self.cook_time.get().strip()
        ingredient_1 = self.i1.get().strip()
        ingredient_2 = self.i2.get().strip()
        ingredient_3 = self.i3.get().strip()
        ingredient_4 = self.i4.get().strip()
        ingredient_5 = self.i5.get().strip()
        ingredient_6 = self.i6.get().strip()
        ingredient_7 = self.i7.get().strip()
        ingredient_8 = self.i8.get().strip()
        ingredient_9 = self.i9.get().strip()
        ingredient_10 = self.i10.get().strip()
        quantity_1 = self.q1.get().strip()
        quantity_2 = self.q2.get().strip()
        quantity_3 = self.q3.get().strip()
        quantity_4 = self.q4.get().strip()
        quantity_5 = self.q5.get().strip()
        quantity_6 = self.q6.get().strip()
        quantity_7 = self.q7.get().strip()
        quantity_8 = self.q8.get().strip()
        quantity_9 = self.q9.get().strip()
        quantity_10 = self.q10.get().strip()
        instructions = self.instructions.get("1.0", tk.END).strip()

        self.controller.add_recipe(name=recipe_name, prep_time=prep_time, cook_time=cook_time,
                                   ing1=ingredient_1, ing2=ingredient_2, ing3=ingredient_3, ing4=ingredient_4,
                                   ing5=ingredient_5, ing6=ingredient_6, ing7=ingredient_7, ing8=ingredient_8,
                                   ing9=ingredient_9, ing10=ingredient_10, qty1=quantity_1, qty2=quantity_2,
                                   qty3=quantity_3, qty4=quantity_4, qty5=quantity_5, qty6=quantity_6, qty7=quantity_7,
                                   qty8=quantity_8, qty9=quantity_9, qty10=quantity_10, instructions=instructions)
        self.name.delete(0, tk.END)
        self.prep_time.delete(0, tk.END)
        self.cook_time.delete(0, tk.END)
        self.i1.delete(0, tk.END)
        self.i2.delete(0, tk.END)
        self.i3.delete(0, tk.END)
        self.i4.delete(0, tk.END)
        self.i5.delete(0, tk.END)
        self.i6.delete(0, tk.END)
        self.i7.delete(0, tk.END)
        self.i8.delete(0, tk.END)
        self.i9.delete(0, tk.END)
        self.i10.delete(0, tk.END)
        self.q1.delete(0, tk.END)
        self.q2.delete(0, tk.END)
        self.q3.delete(0, tk.END)
        self.q4.delete(0, tk.END)
        self.q5.delete(0, tk.END)
        self.q6.delete(0, tk.END)
        self.q7.delete(0, tk.END)
        self.q8.delete(0, tk.END)
        self.q9.delete(0, tk.END)
        self.q10.delete(0, tk.END)
        self.instructions.delete("1.0", tk.END)
        self.controller.show_frame(Recipes)
        return

class ViewRecipe(tk.Frame):                             ## recipe page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title = tk.Label(self, text="", font=("Arial", 20, "bold"))
        self.title.pack(side=tk.TOP, pady=20)

        self.body = tk.Label(self, text="", justify="left", anchor="w")
        self.body.pack(fill="both", expand=True, padx=10, pady=10)

        b1 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(Recipes))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh(self):
        name = self.controller.selected_recipe.get()
        data = self.controller.recipes.get(name)

        if not data:
            self.title.config(text="No recipe selected")
            self.body.config(text="")
            return

        self.title.config(text=name)

        lines = []
        for i in range(1, 11):
            ingredient = data.get(f"Ingredient {i}", "").strip()
            qty = data.get(f"Ingredient {i} Quantity", "").strip()
            if ingredient or qty:
                lines.append(f"- {ingredient} {qty}".strip())

        instructions = data.get("Instructions", "").strip()

        text = "Ingredients:\n" + ("\n".join(lines) if lines else "(none)") + "\n\n"
        text += "Instructions:\n" + (instructions if instructions else "(none)")

        self.body.config(text=text)


class RemoveRecipe(tk.Frame):                             ## recipe page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Remove Recipe", font=("Arial", 20)).pack(pady=20)

        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="Select recipe:").pack(side=tk.LEFT, padx=5)

        self.selected_recipe = tk.StringVar(value="")
        self.recipe_box = ttk.Combobox(row, textvariable=self.selected_recipe, values=[], state="readonly", width=35)
        self.recipe_box.pack(side=tk.LEFT, padx=5)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack(pady=(5, 0))

        btns = tk.Frame(self)
        btns.pack(side=tk.BOTTOM, pady=15)

        tk.Button(btns, text="Remove", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Back", command=lambda: controller.show_frame(Recipes)).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        names = sorted(self.controller.recipes.keys())
        self.recipe_box["values"] = names

        if names:
            self.selected_recipe.set(names[0])
            self.msg.config(text="")
        else:
            self.selected_recipe.set("")
            self.msg.config(text="No recipes to remove.", fg="red")

    

    def remove_selected(self):
        name = self.selected_recipe.get()
        if not name:
            self.msg.config(text="Select a recipe first.", fg="red")
            return

        if not messagebox.askyesno("Confirm", f"Remove '{name}'?"):
            return

        if self.controller.remove_recipe(name):
            self.msg.config(text=f"Removed: {name}", fg="green")
            self.refresh()
            self.controller.show_frame(Recipes)
        else:
            self.msg.config(text="Recipe not found.", fg="red")


class GroceryLists(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Grocery Lists", font=("Arial", 20)).pack(pady=20)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="Add List", command=lambda: controller.show_frame(AddList)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View List",command=self.view_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove List", command=lambda: controller.show_frame(RemoveList)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Go Home", command=lambda: controller.show_frame(HomePage)).pack(side=tk.LEFT, padx=5)

    def refresh(self):

        for rb in self.list_frame.winfo_children():
            rb.destroy()

        names = sorted(self.controller.lists.keys())

        current = self.controller.selected_list.get()
        if current not in names:
            self.controller.selected_list.set(names[0] if names else "")

        if not names:
            tk.Label(self.list_frame, text="No lists yet. Click 'Add List' to create one.", font=("Arial", 14)).pack(anchor="w")
            return

        for name in names:
            tk.Radiobutton(self.list_frame, text=name, variable=self.controller.selected_list, value=name, anchor="w", justify="left").pack(fill="x", anchor="w")

    def view_selected(self):
        name = self.controller.selected_list.get()
        if not name:
            self.msg.config(text="Select a list first.")
            return
        self.msg.config(text="")
        self.controller.show_frame(ViewList)

class AddList(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Add Grocery List", font=("Arial", 20)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(fill="both", expand=True, padx=15, pady=10)

        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="List Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.list_name_entry = tk.Entry(form)
        self.list_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Items", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=(15, 5))
        tk.Label(form, text="Quantity", font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w", pady=(15, 5))

        self.item_entries = []
        self.qty_entries = []

        start_row = 2
        num_rows = 12  

        for i in range(num_rows):
            item_e = tk.Entry(form)
            qty_e = tk.Entry(form, width=12)

            item_e.grid(row=start_row + i, column=0, sticky="ew", padx=5, pady=3)
            qty_e.grid(row=start_row + i, column=1, sticky="w", padx=5, pady=3)

            self.item_entries.append(item_e)
            self.qty_entries.append(qty_e)

        form.grid_columnconfigure(0, weight=1)

        notes_row = start_row + num_rows
        tk.Label(form, text="Notes").grid(row=notes_row, column=0, sticky="w", padx=5, pady=(15, 5))
        self.notes = ScrolledText(form, height=6, wrap=tk.WORD)
        self.notes.grid(row=notes_row + 1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        form.grid_rowconfigure(notes_row + 1, weight=1)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="Confirm", command=self.when_confirm_pressed).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=lambda: controller.show_frame(GroceryLists)).pack(side=tk.LEFT, padx=5)

    def when_confirm_pressed(self):
        list_name = self.list_name_entry.get().strip()
        if not list_name:
            print("List name required")
            return

        items = []
        for item_entry, qty_entry in zip(self.item_entries, self.qty_entries):
            item = item_entry.get().strip()
            qty = qty_entry.get().strip()
            if item or qty:
                items.append({"name": item, "qty": qty})

        notes = self.notes.get("1.0", tk.END).strip()

        # save
        self.controller.add_list(list_name=list_name, items=items, notes=notes)

        self.list_name_entry.delete(0, tk.END)
        for e in self.item_entries + self.qty_entries:
            e.delete(0, tk.END)
        self.notes.delete("1.0", tk.END)

        self.controller.show_frame(GroceryLists)

class ViewList(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title = tk.Label(self, text="", font=("Arial", 18, "bold"))
        self.title.pack(pady=10)

        self.text = ScrolledText(self, height=15, wrap=tk.WORD)
        self.text.pack(fill="both", expand=True, padx=15, pady=10)
        self.text.config(state="disabled")

        buttons = tk.Frame(self)
        buttons.pack(side=tk.BOTTOM, pady=10)

        tk.Button(buttons, text="Back", command=lambda: controller.show_frame(GroceryLists)).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        list_name = self.controller.selected_list.get()
        data = self.controller.lists.get(list_name)

        self.title.config(text=list_name if list_name else "No list selected")

        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)

        if not data:
            self.text.insert(tk.END, "No list selected (or it no longer exists).")
            self.text.config(state="disabled")
            return

        items = data.get("items", [])
        notes = data.get("notes", "").strip()

        self.text.insert(tk.END, "Items:\n")
        if not items:
            self.text.insert(tk.END, "  (none)\n")
        else:
            for it in items:
                name = (it.get("name") or "").strip()
                qty = (it.get("qty") or "").strip()
                if name or qty:
                    line = f"{name}"
                    if qty:
                        line += f" - {qty}"
                    self.text.insert(tk.END, line + "\n")

        if notes:
            self.text.insert(tk.END, "\nNotes:\n")
            self.text.insert(tk.END, notes + "\n")

        self.text.config(state="disabled")

class RemoveList(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Remove Grocery List", font=("Arial", 20)).pack(pady=20)

        row = tk.Frame(self)
        row.pack(pady=10)

        tk.Label(row, text="Select list:").pack(side=tk.LEFT, padx=5)

        self.selected = tk.StringVar(value="")
        self.box = ttk.Combobox(row, textvariable=self.selected, values=[],
                                state="readonly", width=35)
        self.box.pack(side=tk.LEFT, padx=5)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.pack(pady=(5, 0))

        buttons = tk.Frame(self)
        buttons.pack(side=tk.BOTTOM, pady=15)

        tk.Button(buttons, text="Remove", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Back",
                  command=lambda: controller.show_frame(GroceryLists)).pack(side=tk.LEFT, padx=5)

    def refresh(self):
        names = sorted(self.controller.lists.keys())
        self.box["values"] = names

        if names:
            cur = self.selected.get()
            self.selected.set(cur if cur in names else names[0])
            self.msg.config(text="")
        else:
            self.selected.set("")
            self.msg.config(text="No lists to remove.", fg="red")

    def remove_selected(self):
        name = self.selected.get()
        if not name:
            self.msg.config(text="Select a list first.", fg="red")
            return

        if not messagebox.askyesno("Confirm", f"Remove '{name}'?"):
            return

        if self.controller.remove_list(name):
            if getattr(self.controller, "selected_list", None) and self.controller.selected_list.get() == name:
                self.controller.selected_list.set("")

            self.msg.config(text=f"Removed: {name}", fg="green")
            self.controller.show_frame(GroceryLists)  
        else:
            self.msg.config(text="List not found.", fg="red")

class UsableRecipes(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Recipes you can make now:", font=("Arial", 20)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage)).pack()

class Calendar(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)

        title = tk.Label(self, text="Calendar", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        b1 = tk.Button(self, text="Add Event", command=lambda: controller.show_frame(AddEvent))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

        b3 = tk.Button(self, text="Remove Event", command=lambda: controller.show_frame(AddList))
        b3.pack(side=tk.LEFT, padx=5, pady=5)

        b4 = tk.Button(self, text="View Event", command=lambda: controller.show_frame(ViewEvent))
        b4.pack(side=tk.LEFT, padx=5, pady=5)

class AddEvent(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)

        title = tk.Label(self, text="Add Event", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        b1 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(Calendar))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(self, text="Confirm", command=lambda: controller.show_frame(Calendar))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

class ViewEvent(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)

        title = tk.Label(self, text="View Event", font=("Arial", 20))
        title.pack(side=tk.TOP, pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)

        b1 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(Calendar))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

class RemoveEvent(tk.Frame):                             
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Select an event to remove:", font=("Arial", 20)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage)).pack()

if __name__ == '__main__':
    app = App()
    app.mainloop()