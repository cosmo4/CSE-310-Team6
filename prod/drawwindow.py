# pip install Ghostscript
# https://ghostscript.com/releases/gsdnld.html
# reload vs code, test with 'gs --verion' if error, 'gswin64 --version'
# run main.py, try to save drawing as img. if error, add 'gswin64' to PATH in System Environment Variables
# windows>System>About>Advanced system settings>Environment Variables>Select 'Path' in System Variables section>Edit>New>'C:\Program Files\gs\gs10.03.1\bin\gswin64'>Ok

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import io

class DrawWindow:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Drawing Canvas")

        self.canvas = tk.Canvas(self.top, bg="white", width=1200, height=800)
        self.canvas.pack()

        self.draw_mode = True
        self.old_x = None
        self.old_y = None
        self.pen_color = "black"
        self.eraser_color = "white"
        self.pen_width = 3
        self.setup_ui()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def setup_ui(self):
        # Create a frame for buttons
        button_frame = tk.Frame(self.top)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=25, pady=20)

        # Define button dimensions
        button_width = 12
        button_height = 2
        button_padx = 10  # Spacing between buttons

        # Create buttons with specified dimensions and spacing
        draw_button = tk.Button(button_frame, text="Draw Mode", command=self.set_draw_mode, width=button_width, height=button_height)
        draw_button.pack(side=tk.LEFT, padx=button_padx)

        erase_button = tk.Button(button_frame, text="Erase Mode", command=self.set_erase_mode, width=button_width, height=button_height)
        erase_button.pack(side=tk.LEFT, padx=button_padx)

        clear_button = tk.Button(button_frame, text="Clear Canvas", command=self.clear_canvas, width=button_width, height=button_height)
        clear_button.pack(side=tk.LEFT, padx=button_padx)

        save_button = tk.Button(button_frame, text="Save as JPEG", command=self.save_as_jpeg, width=button_width, height=button_height)
        save_button.pack(side=tk.LEFT, padx=button_padx)


    def set_draw_mode(self):
        self.draw_mode = True

    def set_erase_mode(self):
        self.draw_mode = False

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_as_jpeg(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.canvas.update()
            ps = self.canvas.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            
            # Create a new white image with the same size as the canvas
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)  # Use alpha channel if available

            bg.save(file_path, "JPEG")

            messagebox.showinfo("Image Saved", "Image saved successfully!")

        # Close the drawing window
            self.top.destroy()


    def paint(self, event):
        paint_color = self.pen_color if self.draw_mode else self.eraser_color
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.pen_width, fill=paint_color, capstyle=tk.ROUND, smooth=tk.TRUE)

        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None
