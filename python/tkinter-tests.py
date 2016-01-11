from Tkinter import *

master = Tk()

canvas = Canvas(master, width=800, height=600)
canvas.pack()

canvas.create_rectangle(250, 10, 790, 590, fill="white")

b = Button(master, text="Hello world")
b.pack(side="left", fill='both', expand=False, padx=4, pady=4)


mainloop()