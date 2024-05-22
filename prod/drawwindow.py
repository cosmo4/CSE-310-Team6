import tkinter as tk
from tkinter import messagebox

class DrawWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Draw Window")

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        self.convert_button = tk.Button(self, text="Convert to ASCII", command=self.convert_to_ascii)
        self.convert_button.pack()

        self.canvas.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        x, y = event.x, event.y
        r = 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")

    def convert_to_ascii(self):
        # Implement your ASCII conversion logic here
        messagebox.showinfo("Conversion Result", "ASCII art will be displayed here.")

