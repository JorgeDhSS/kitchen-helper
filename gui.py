from tkinter import *
from tkinter import ttk


def setText(text):
    label1.config(text=text)

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
label1 = ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
btn1 = ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()