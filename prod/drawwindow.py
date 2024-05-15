import tkinter as tk

class DrawWindow:
    """
    Class to handle the draw window functionality.
    """
    def __init__(self, root):
        """
        Initialize the draw window.
        """
        self.root = root
        self.root.title("Draw")
        self.root.geometry("400x400")

        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def save_drawing(self, filename):
        """
        Save the drawing to a file.
        """
        self.canvas.postscript(file=filename, colormode='color')