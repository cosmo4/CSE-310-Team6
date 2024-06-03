import tkinter as tk
from tkinter import messagebox
import pyrebase

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyC-NJByPVn8XpksSCkSctCja08tr5creYU",
    'authDomain': "notes-manager-81e62.firebaseapp.com",
    'databaseURL': "https://notes-manager-81e62.firebaseio.com",
    'projectId': "notes-manager-81e62",
    'storageBucket': "notes-manager-81e62.appspot.com",
    'messagingSenderId': "88497487267",
    'appId': "1:88497487267:web:e27eb195f07116bdedee16",
    'measurementId': "G-JB077QZ9QM"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class NewNoteWindow:
    def __init__(self, parent):
        self.parent = parent
        self.new_note_window = tk.Toplevel(parent)
        self.new_note_window.title("New Note")
        self.new_note_window.geometry("400x300")

        # Title field
        self.title_label = tk.Label(self.new_note_window, text="Title")
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(self.new_note_window, width=50)
        self.title_entry.pack(pady=5)

        # Date field
        self.date_label = tk.Label(self.new_note_window, text="Date")
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(self.new_note_window, width=50)
        self.date_entry.pack(pady=5)

        # Text box
        self.text_label = tk.Label(self.new_note_window, text="Note")
        self.text_label.pack(pady=5)
        self.text_box = tk.Text(self.new_note_window, wrap=tk.WORD, height=10)
        self.text_box.pack(pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.new_note_window)
        self.button_frame.pack(pady=10)

        self.save_button = tk.Button(self.button_frame, text="Save Note", command=self.save_note)
        self.save_button.grid(row=0, column=0, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.new_note_window.destroy)
        self.cancel_button.grid(row=0, column=1, padx=5)

    def save_note(self):
        title = self.title_entry.get()
        date = self.date_entry.get()
        note = self.text_box.get("1.0", tk.END).strip()

        if title and date and note:
            note_data = {
                "title": title,
                "date": date,
                "note": note
            }
            db.child("notes").push(note_data)
            messagebox.showinfo("Success", "Note saved successfully!")
            self.new_note_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")

