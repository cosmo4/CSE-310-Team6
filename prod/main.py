# pip install pyrebase4
# pip install setuptools

import tkinter as tk
from tkinter import messagebox
from upload import upload
from aiFileTest import summarize
from drawwindow import DrawWindow
from login import LoginWindow

class MainWindow:
    """
    Class to handle the main window functionality.
    """
    def __init__(self, root):
        """
        Initialize the main window.
        """
        self.root = root
        self.root.title("Note Manager")
        self.root.geometry("600x400")

        # Create the frame for the main window
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame to hold the buttons on the left side
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # New Note button
        self.new_note_button = tk.Button(self.button_frame, text="New Note", width=20, height=2)
        self.new_note_button.pack(pady=10)

        # Summarize button
        self.summarize_button = tk.Button(self.button_frame, text="Summarize", width=20, height=2, command=summarize)
        self.summarize_button.pack(pady=10)

        # Draw button
        self.draw_button = tk.Button(self.button_frame, text="Draw", command=self.open_draw_window, width=20, height=2)
        self.draw_button.pack(pady=10)

        # Set Reminder button
        self.set_reminder_button = tk.Button(self.button_frame, text="Set Reminder", width=20, height=2)
        self.set_reminder_button.pack(pady=10)

        # Upload Notes button
        self.upload_notes_button = tk.Button(self.button_frame, text="Upload Notes", width=20, height=2, command=upload)
        self.upload_notes_button.pack(pady=10)

        # Text entry box on the right side
        self.text_entry = tk.Text(self.frame, wrap=tk.WORD)
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Function to launch the drawing window
    def open_draw_window(self):
            draw_window = DrawWindow(self.root)

class NoteManagerApp:
    """
    Main application class to manage the flow between login and main windows.
    """
    def __init__(self, root):
        """
        Initialize the application with the login window.
        """
        self.root = root
        self.login_window = LoginWindow(self.root, self)

    def open_main_window(self):
        """
        Transition from login window to main window.
        """
        self.login_window.frame.destroy()
        self.main_window = MainWindow(self.root)

if __name__ == "__main__":
    # Create the main Tkinter root window
    root = tk.Tk()
    # Initialize and run the application
    app = NoteManagerApp(root)
    root.mainloop()

