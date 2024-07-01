import tkinter as tk
from tkinter import messagebox

class DrawWindow(tk.Toplevel):
    """
    Class to handle the login window functionality.
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Draw Window")

        # Open draw window
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(padx=20, pady=20)

        # Create convert button and assign command
        self.convert_button = tk.Button(self, text="Convert to ASCII", command=self.convert_to_ascii)
        self.convert_button.pack(pady=10)

        # Allow user to draw when clicking on canvas
        self.canvas.bind("<B1-Motion>", self.draw)

    # Define the function for drawing
    def draw(self, event):
        x, y = event.x, event.y
        r = 3 # Attach radius of drawing point
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")

    def convert_to_ascii(self):
        # ASCII conversion here
        messagebox.showinfo("Conversion Result", "ASCII art will be displayed here.")
        
        # Close draw window when ASCII conversion is successful
