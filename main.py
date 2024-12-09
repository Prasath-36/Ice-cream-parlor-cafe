import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# SQLite database 
def init_db():
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS allergens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flavor_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    FOREIGN KEY (flavor_id) REFERENCES seasonal_flavors(id)
                )''')

    conn.commit()
    conn.close()
def reset_ids(table_name):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    if table_name == "cart":
        columns = "flavor_id, quantity"
    elif table_name == "seasonal_flavors":
        columns = "name, description, price"
    elif table_name == "allergens":
        columns = "name"
    else:
        conn.close()
        raise ValueError("Invalid table name")
    c.execute(f"CREATE TEMPORARY TABLE temp_table AS SELECT {columns} FROM {table_name}")
    c.execute(f"DELETE FROM {table_name}")  
    c.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")  
    c.execute(f"INSERT INTO {table_name} ({columns}) SELECT {columns} FROM temp_table")
    c.execute("DROP TABLE temp_table") 
    conn.commit()
    conn.close()

def add_flavor(name, description, price):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    name=name.lower()
    c.execute('SELECT * FROM seasonal_flavors WHERE name = ?', (name,))
    existing_flavor = c.fetchone()
    if existing_flavor:
        messagebox.showerror("Error", "Flavor already exists!")
        conn.close()
        return
    c.execute('INSERT INTO seasonal_flavors (name, description, price) VALUES (?, ?, ?)', 
              (name, description, price))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Flavor added successfully!")

def add_allergen(name):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO allergens (name) VALUES (?)', (name,))
        conn.commit()
        messagebox.showinfo("Success", "Allergen added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Allergen already exists!")
    conn.close()

def add_to_cart(flavor_id):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()

    c.execute('SELECT * FROM cart WHERE flavor_id = ?', (flavor_id,))
    existing_item = c.fetchone()

    if existing_item:
        new_quantity = existing_item[2] + 1
        c.execute('UPDATE cart SET quantity = ? WHERE flavor_id = ?', (new_quantity, flavor_id))
    else:
        c.execute('INSERT INTO cart (flavor_id, quantity) VALUES (?, ?)', (flavor_id, 1))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Item added to cart!")

def remove_from_cart(cart_id):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
    conn.commit()
    conn.close()
    reset_ids("cart")
    messagebox.showinfo("Success", "Item removed from cart!")

def search_flavors(query):
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('SELECT * FROM seasonal_flavors WHERE name LIKE ?', (f"%{query}%",))
    results = c.fetchall()
    conn.close()
    return results

def get_all_flavors():
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('SELECT * FROM seasonal_flavors')
    results = c.fetchall()
    conn.close()
    return results

def get_cart_items():
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('''SELECT cart.id, seasonal_flavors.name, seasonal_flavors.description, seasonal_flavors.price, cart.quantity
                 FROM cart 
                 JOIN seasonal_flavors ON cart.flavor_id = seasonal_flavors.id''')
    results = c.fetchall()
    conn.close()
    return results

def get_all_allergens():
    conn = sqlite3.connect('ice_cream.db')
    c = conn.cursor()
    c.execute('SELECT * FROM allergens')
    results = c.fetchall()
    conn.close()
    return results

class IceCreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ice Cream Parlor Management")
        self.init_ui()

    def init_ui(self):
        self.tab_control = ttk.Notebook(self.root)

        self.flavors_tab = ttk.Frame(self.tab_control)
        self.cart_tab = ttk.Frame(self.tab_control)
        self.allergens_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.flavors_tab, text="Seasonal Flavors")
        self.tab_control.add(self.cart_tab, text="Cart")
        self.tab_control.add(self.allergens_tab, text="Allergens")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_flavors_tab()
        self.setup_cart_tab()
        self.setup_allergens_tab()

    def setup_flavors_tab(self):
        ttk.Label(self.flavors_tab, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.flavor_name_entry = ttk.Entry(self.flavors_tab)
        self.flavor_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.flavors_tab, text="Description").grid(row=1, column=0, padx=5, pady=5)
        self.flavor_description_entry = ttk.Entry(self.flavors_tab)
        self.flavor_description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.flavors_tab, text="Price").grid(row=2, column=0, padx=5, pady=5)
        self.flavor_price_entry = ttk.Entry(self.flavors_tab)
        self.flavor_price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.flavors_tab, text="Add Flavor", command=self.add_flavor).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(self.flavors_tab, text="Search Flavors").grid(row=4, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.flavors_tab)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.flavors_tab, text="Search", command=self.search_flavors).grid(row=4, column=2, padx=5, pady=5)
        ttk.Button(self.flavors_tab, text="Home", command=self.refresh_flavors).grid(row=4, column=3, padx=5, pady=5)
        self.flavors_tree = ttk.Treeview(self.flavors_tab, columns=("ID", "Name", "Description", "Price"), show="headings")
        self.flavors_tree.heading("ID", text="ID")
        self.flavors_tree.heading("Name", text="Name")
        self.flavors_tree.heading("Description", text="Description")
        self.flavors_tree.heading("Price", text="Price")
        self.flavors_tree.grid(row=5, column=0, columnspan=4, pady=10, padx=10)
        ttk.Button(self.flavors_tab, text="Add to Cart", command=self.add_selected_flavor_to_cart).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self.flavors_tab, text="Delete Flavor", command=self.delete_selected_flavor).grid(row=6, column=2, columnspan=2, pady=10)
        self.refresh_flavors()

    def setup_cart_tab(self):
        self.cart_tree = ttk.Treeview(self.cart_tab, columns=("ID", "Name", "Description", "Price", "Quantity"), show="headings")
        self.cart_tree.heading("ID", text="ID")
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Description", text="Description")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        ttk.Button(self.cart_tab, text="Remove from Cart", command=self.remove_selected_cart_item).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(self.cart_tab, text="Cart Total Value:").grid(row=2, column=0, padx=5, pady=5)
        self.cart_total_label = ttk.Label(self.cart_tab, text="₹0.00")
        self.cart_total_label.grid(row=2, column=1, padx=5, pady=5)
        self.refresh_cart()

    def setup_allergens_tab(self):
        ttk.Label(self.allergens_tab, text="Allergen Name").grid(row=0, column=0, padx=5, pady=5)
        self.allergen_name_entry = ttk.Entry(self.allergens_tab)
        self.allergen_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.allergens_tab, text="Add Allergen", command=self.add_allergen).grid(row=1, column=0, columnspan=2, pady=5)
        self.allergens_tree = ttk.Treeview(self.allergens_tab, columns=("ID", "Name"), show="headings")
        self.allergens_tree.heading("ID", text="ID")
        self.allergens_tree.heading("Name", text="Name")
        self.allergens_tree.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        ttk.Button(self.allergens_tab, text="Remove Allergen", command=self.remove_selected_allergen).grid(row=3, column=0, columnspan=2, pady=5)
        self.refresh_allergens()

    def remove_selected_allergen(self):
        selected = self.allergens_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No allergen selected!")
            return
        allergen_id = self.allergens_tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this allergen?")
        if confirm:
            conn = sqlite3.connect('ice_cream.db')
            c = conn.cursor()
            c.execute('DELETE FROM allergens WHERE id = ?', (allergen_id,))
            conn.commit()
            conn.close()
            reset_ids("allergens")
            messagebox.showinfo("Success", "Allergen removed successfully!")
            self.refresh_allergens()    

    def refresh_flavors(self):
        for item in self.flavors_tree.get_children():
            self.flavors_tree.delete(item)
        for flavor in get_all_flavors():
            self.flavors_tree.insert("", "end", values=flavor)

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        cart_items = get_cart_items()
        total_value = 0
        for cart_item in cart_items:
            self.cart_tree.insert("", "end", values=cart_item)
            total_value += cart_item[3] * cart_item[4] 
        self.cart_total_label.config(text=f"₹{total_value:.2f}")
        '''for cart_item in get_cart_items():
            self.cart_tree.insert("", "end", values=cart_item)'''

    def refresh_allergens(self):
        for item in self.allergens_tree.get_children():
            self.allergens_tree.delete(item)
        for allergen in get_all_allergens():
            self.allergens_tree.insert("", "end", values=allergen)

    def add_flavor(self):
        name = self.flavor_name_entry.get()
        description = self.flavor_description_entry.get()
        price = self.flavor_price_entry.get()
        add_flavor(name, description, price)
        self.refresh_flavors()

    def add_selected_flavor_to_cart(self):
        selected = self.flavors_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No flavor selected!")
            return
        flavor_id = self.flavors_tree.item(selected[0], "values")[0]
        add_to_cart(flavor_id)
        self.refresh_cart()

    def remove_selected_cart_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No cart item selected!")
            return
        cart_id = self.cart_tree.item(selected[0], "values")[0]
        remove_from_cart(cart_id)
        self.refresh_cart()

    def search_flavors(self):
        query = self.search_entry.get()
        results = search_flavors(query)
        for item in self.flavors_tree.get_children():
            self.flavors_tree.delete(item)
        for flavor in results:
            self.flavors_tree.insert("", "end", values=flavor)

    def delete_selected_flavor(self):
        selected = self.flavors_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No flavor selected!")
            return
        flavor_id = self.flavors_tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this flavor?")
        if confirm:
            conn = sqlite3.connect('ice_cream.db')
            c = conn.cursor()
            c.execute('DELETE FROM seasonal_flavors WHERE id = ?', (flavor_id,))
            conn.commit()
            conn.close()
            reset_ids("seasonal_flavors")
            messagebox.showinfo("Success", "Flavor deleted successfully!")
            self.refresh_flavors()

    def add_allergen(self):
        name = self.allergen_name_entry.get()
        add_allergen(name)
        self.refresh_allergens()
        
init_db() 
root = tk.Tk()
app = IceCreamApp(root)
root.mainloop()
