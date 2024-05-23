import csv
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

FILENAME = 'phonebook.csv'


def initialize_csv():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Address", "Email", "Phone Numbers"])


def add_contact(name, address, email, phone_numbers):
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, address, email, phone_numbers])
    messagebox.showinfo("Success", f"Contact '{name}' added.")


def edit_contact(name, new_address=None, new_email=None, new_phone_numbers=None):
    contacts = []
    updated = False
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                if new_address: row[1] = new_address
                if new_email: row[2] = new_email
                if new_phone_numbers: row[3] = new_phone_numbers
                updated = True
            contacts.append(row)

    if not updated:
        messagebox.showerror("Error", f"Contact '{name}' not found.")
        return

    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(contacts)
    messagebox.showinfo("Success", f"Contact '{name}' updated.")


def view_contacts():
    contacts = []
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            contacts.append(row)
    contacts_sorted = sorted(contacts[1:], key=lambda x: x[0])  # Exclude header row and sort by name
    view_window = tk.Toplevel()
    view_window.title("View Contacts")
    view_window.configure(bg="#ffebcd")

    for contact in contacts_sorted:
        contact_label = tk.Label(view_window,
                                 text=f"Name: {contact[0]}, Address: {contact[1]}, Email: {contact[2]}, Phone Numbers: {contact[3]}",
                                 bg="#ffebcd", font=("Arial", 12))
        contact_label.pack(pady=5)


def delete_contact(name):
    contacts = []
    deleted = False
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != name:
                contacts.append(row)
            else:
                deleted = True

    if not deleted:
        messagebox.showerror("Error", f"Contact '{name}' not found.")
        return

    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(contacts)
    messagebox.showinfo("Success", f"Contact '{name}' deleted.")


def search_contact(param, value):
    found = False
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if (param == 'name' and row[0] == value) or (param == 'phone' and value in row[3]):
                messagebox.showinfo("Contact Found",
                                    f"Name: {row[0]}, Address: {row[1]}, Email: {row[2]}, Phone Numbers: {row[3]}")
                found = True

    if not found:
        messagebox.showinfo("Not Found", f"No contact found with {param} '{value}'.")


def add_contact_gui():
    name = simpledialog.askstring("Input", "Enter name:")
    if not name: return
    address = simpledialog.askstring("Input", "Enter address:")
    email = simpledialog.askstring("Input", "Enter email:")
    phone_numbers = simpledialog.askstring("Input", "Enter phone numbers (comma separated):")
    add_contact(name, address, email, phone_numbers)


def edit_contact_gui():
    name = simpledialog.askstring("Input", "Enter name of the contact to edit:")
    if not name: return
    new_address = simpledialog.askstring("Input", "Enter new address (leave blank to skip):")
    new_email = simpledialog.askstring("Input", "Enter new email (leave blank to skip):")
    new_phone_numbers = simpledialog.askstring("Input",
                                               "Enter new phone numbers (comma separated, leave blank to skip):")
    edit_contact(name, new_address or None, new_email or None, new_phone_numbers or None)


def delete_contact_gui():
    name = simpledialog.askstring("Input", "Enter name of the contact to delete:")
    if name:
        delete_contact(name)


def search_contact_gui():
    param = simpledialog.askstring("Input", "Search by 'name' or 'phone':").strip().lower()
    value = simpledialog.askstring("Input", f"Enter {param} to search:").strip()
    search_contact(param, value)


def main():
    initialize_csv()

    root = tk.Tk()
    root.title("Phonebook Application")
    root.configure(bg="#add8e6")
    root.geometry("500x500")

    title_frame = tk.Frame(root, bg="#1E90FF", bd=5)
    title_frame.pack(pady=20)

    title_label = tk.Label(title_frame, text="Phonebook Application", font=("Helvetica", 18, "bold"), bg="#1E90FF",
                           fg="white")
    title_label.pack()

    button_frame = tk.Frame(root, bg="#87CEEB", bd=5)
    button_frame.pack(pady=10)

    button_style = {
        "font": ("Helvetica", 12),
        "bg": "#FFD700",
        "fg": "black",
        "activebackground": "#FFA500",
        "activeforeground": "white",
        "bd": 2,
        "relief": tk.RAISED,
        "width": 20,
    }

    add_button = tk.Button(button_frame, text="Add Contact ☎️", command=add_contact_gui, **button_style)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    edit_button = tk.Button(button_frame, text="Edit Contact ✏️", command=edit_contact_gui, **button_style)
    edit_button.grid(row=0, column=1, padx=10, pady=10)

    view_button = tk.Button(button_frame, text="View Contacts 👁️", command=view_contacts, **button_style)
    view_button.grid(row=1, column=0, padx=10, pady=10)

    delete_button = tk.Button(button_frame, text="Delete Contact ❌", command=delete_contact_gui, **button_style)
    delete_button.grid(row=1, column=1, padx=10, pady=10)

    search_button = tk.Button(button_frame, text="Search Contact 🔍", command=search_contact_gui, **button_style)
    search_button.grid(row=2, column=0, columnspan=2, pady=10)

    exit_button = tk.Button(root, text="Exit 🚪", command=root.quit, **button_style)
    exit_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
