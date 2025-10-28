#!/usr/bin/env python3
"""gui.py - A tiny Tkinter GUI to generate a single password"""
import tkinter as tk
from tkinter import ttk, messagebox
from password_generator import generate_password

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("420x220")
        self.resizable(False, False)

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Length:").grid(column=0, row=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        ttk.Spinbox(frm, from_=4, to=64, textvariable=self.length_var, width=6).grid(column=1, row=0, sticky="w")

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(frm, text="Uppercase", variable=self.upper_var).grid(column=0, row=1, sticky="w")
        ttk.Checkbutton(frm, text="Lowercase", variable=self.lower_var).grid(column=1, row=1, sticky="w")
        ttk.Checkbutton(frm, text="Digits", variable=self.digits_var).grid(column=0, row=2, sticky="w")
        ttk.Checkbutton(frm, text="Symbols", variable=self.symbols_var).grid(column=1, row=2, sticky="w")

        ttk.Button(frm, text="Generate", command=self.on_generate).grid(column=0, row=3, columnspan=2, pady=8, sticky="ew")

        self.output = tk.Text(frm, height=3, width=48, wrap="word")
        self.output.grid(column=0, row=4, columnspan=2, pady=6)

    def on_generate(self):
        try:
            pw = generate_password(self.length_var.get(), self.upper_var.get(), self.lower_var.get(), self.digits_var.get(), self.symbols_var.get())
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, pw)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()