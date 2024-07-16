'''
Author: Jesse Gore
Date: 7/15/2024
Assignment Project status report
Purpose: to create a ordering program that takes multiple selections, gives total pricem delivery time, and driver ot in-store pick up associate.
'''


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Constants
PIZZA_SIZES = {"Small": 5, "Medium": 8, "Large": 10}
TOPPINGS = {"Cheese": 1, "Pepperoni": 1, "Mushrooms": 1, "Onions": 1, "Bacon": 1}
MALE_NAMES = ["John", "Michael", "David", "James", "Robert"]
FEMALE_NAMES = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]

# Main Application Class
class PizzaPalaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Palace")
        self.root.geometry("500x500")
        self.create_main_window()

    def create_main_window(self):
        self.clear_window()
        self.main_label = tk.Label(self.root, text="Welcome to Pizza Palace!")
        self.main_label.pack(pady=10)

        self.create_pizza_button = tk.Button(self.root, text="Create Your Own Pizza", command=self.create_pizza_window)
        self.create_pizza_button.pack(pady=5)

    def create_pizza_window(self):
        self.clear_window()
        self.pizza_label = tk.Label(self.root, text="Create Your Own Pizza")
        self.pizza_label.pack(pady=10)

        self.size_label = tk.Label(self.root, text="Choose Size:")
        self.size_label.pack()

        self.size_var = tk.StringVar(value=list(PIZZA_SIZES.keys())[0])
        self.size_images = {}
        for size, price in PIZZA_SIZES.items():
            frame = tk.Frame(self.root)
            frame.pack()

            canvas = tk.Canvas(frame, width=60, height=60)
            canvas.pack(side=tk.LEFT)

            if size == "Small":
                canvas.create_oval(15, 15, 45, 45, outline="black", fill="black")
            elif size == "Medium":
                canvas.create_oval(10, 10, 50, 50, outline="black", fill="black")
            elif size == "Large":
                canvas.create_oval(5, 5, 55, 55, outline="black", fill="black")

            rb = tk.Radiobutton(frame, text=f"{size} (${price})", variable=self.size_var, value=size)
            rb.pack(side=tk.LEFT)

        self.topping_label = tk.Label(self.root, text="Choose Toppings:")
        self.topping_label.pack()

        self.topping_vars = []
        for topping, price in TOPPINGS.items():
            var = tk.BooleanVar()
            frame = tk.Frame(self.root)
            frame.pack()
            cb = tk.Checkbutton(frame, text=f"{topping} (${price})", variable=var)
            cb.pack(side=tk.LEFT)
            self.topping_vars.append((var, topping))

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.pack()

        self.quantity_var = tk.StringVar(value="1")
        self.quantity_menu = tk.OptionMenu(self.root, self.quantity_var, *[str(i) for i in range(1, 21)])
        self.quantity_menu.pack()

        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_window)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.review_order)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def review_order(self):
        pizza_size = self.size_var.get()
        toppings = [topping for var, topping in self.topping_vars if var.get()]
        quantity = self.quantity_var.get()

        size_price = PIZZA_SIZES[pizza_size]
        toppings_price = sum([TOPPINGS[topping] for topping in toppings])
        total_price = int(quantity) * (size_price + toppings_price)

        self.clear_window()

        order_summary = f"Order Summary:\n\nSize: {pizza_size} (${size_price})\n"
        order_summary += f"Toppings: {', '.join(toppings)} (${toppings_price})\n"
        order_summary += f"Quantity: {quantity}\nTotal Price: ${total_price}\n"

        self.order_summary_label = tk.Label(self.root, text=order_summary, justify=tk.LEFT)
        self.order_summary_label.pack(pady=10)

        self.payment_button = tk.Button(self.root, text="Proceed to Payment", command=self.payment_window)
        self.payment_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Back", command=self.create_pizza_window)
        self.back_button.pack(pady=5)

    def payment_window(self):
        self.clear_window()
        self.payment_label = tk.Label(self.root, text="Payment/Delivery Options")
        self.payment_label.pack(pady=10)

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.root)
        self.address_entry.pack()

        self.delivery_label = tk.Label(self.root, text="Delivery or Pickup:")
        self.delivery_label.pack()

        self.delivery_var = tk.StringVar(value="Delivery")
        self.delivery_menu = tk.OptionMenu(self.root, self.delivery_var, "Delivery", "Pickup")
        self.delivery_menu.pack()

        self.card_label = tk.Label(self.root, text="Credit Card Number:")
        self.card_label.pack()

        self.card_frame = tk.Frame(self.root)
        self.card_frame.pack()

        self.card_entries = []
        for _ in range(4):
            entry = tk.Entry(self.card_frame, width=4, justify='center')
            entry.pack(side=tk.LEFT, padx=5)
            entry.bind("<KeyRelease>", self.card_entry_validation)
            self.card_entries.append(entry)

        self.expiration_label = tk.Label(self.root, text="Expiration Date (MM/YYYY):")
        self.expiration_label.pack()

        self.expiration_frame = tk.Frame(self.root)
        self.expiration_frame.pack()

        self.expiration_month = tk.Entry(self.expiration_frame, width=2, justify='center')
        self.expiration_month.pack(side=tk.LEFT)
        tk.Label(self.expiration_frame, text="/").pack(side=tk.LEFT)
        self.expiration_year = tk.Entry(self.expiration_frame, width=4, justify='center')
        self.expiration_year.pack(side=tk.LEFT)

        self.cvv_label = tk.Label(self.root, text="CVV:")
        self.cvv_label.pack()

        self.cvv_entry = tk.Entry(self.root, width=3, justify='center')
        self.cvv_entry.pack()

        self.back_button = tk.Button(self.root, text="Back", command=self.review_order)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_order)
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def card_entry_validation(self, event):
        widget = event.widget
        text = widget.get()
        if not text.isdigit() or len(text) > 4:
            widget.delete(4, tk.END)

        if len(text) == 4:
            current_index = self.card_entries.index(widget)
            if current_index < 3:
                self.card_entries[current_index + 1].focus()

    def submit_order(self):
        # Input validation
        if not self.name_entry.get() or not self.address_entry.get() or any(not entry.get() for entry in self.card_entries):
            messagebox.showerror("Error", "All fields are required!")
            return

        card_number = "".join(entry.get() for entry in self.card_entries)
        if not card_number.isdigit() or len(card_number) != 16:
            messagebox.showerror("Error", "Credit Card Number must be 16 digits long!")
            return

        expiration_month = self.expiration_month.get()
        expiration_year = self.expiration_year.get()
        if not expiration_month.isdigit() or not expiration_year.isdigit() or len(expiration_month) != 2 or len(expiration_year) != 4:
            messagebox.showerror("Error", "Expiration date must be in MM/YYYY format!")
            return

        cvv = self.cvv_entry.get()
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showerror("Error", "CVV must be a 3-digit number!")
            return

        # Generate random order number and estimated time
        order_number = random.randint(1000, 9999)
        estimated_time = random.randint(20, 45)  # estimated time in minutes

        # Random driver or pickup name
        if self.delivery_var.get() == "Delivery":
            driver_name = random.choice(MALE_NAMES)
            delivery_message = f"Your order will be delivered by {driver_name}."
        else:
            pickup_name = random.choice(FEMALE_NAMES)
            delivery_message = f"Your order will be ready for pickup by {pickup_name}."

        # Display the order confirmation screen
        self.clear_window()
        confirmation_message = f"Order Confirmed!\n\nOrder Number: {order_number}\nEstimated Time: {estimated_time} minutes\n{delivery_message}"
        self.confirmation_label = tk.Label(self.root, text=confirmation_message, justify=tk.LEFT)
        self.confirmation_label.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaPalaceApp(root)
    root.mainloop()
