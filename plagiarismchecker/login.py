import tkinter as tk
from tkinter import messagebox

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        messagebox.showinfo("Login", "Inicio de sesión exitoso")
    else:
        messagebox.showerror("Login", "Nombre de usuario o contraseña incorrectos")


root = tk.Tk()
root.title("Login")


username_label = tk.Label(root, text="Nombre de usuario:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Contraseña:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Iniciar sesión", command=login)
login_button.pack()

root.mainloop()
