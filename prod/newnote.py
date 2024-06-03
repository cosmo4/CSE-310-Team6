import tkinter as tk
from tkinter import messagebox
from datetime import date
import pyrebase

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

import tkinter as tk
from tkinter import messagebox
from datetime import date

class NewNoteWindow:
    def __init__(self, root):
        self.root = root
        self.note_window = tk.Toplevel(self.root)
        self.note_window.title("New Note")
        self.note_window.geometry("400x400")
        self.note_window["padx"] = 20
        self.note_window["pady"] = 20

        # Title entry
        tk.Label(self.note_window, text="Title:").pack(anchor="w")
        self.title_entry = tk.Entry(self.note_window, width=30)
        self.title_entry.pack(pady=(5, 2), anchor="w")

        # Date entry
        tk.Label(self.note_window, text="Date:").pack(anchor="w", pady=(10, 5))
        self.date_entry = tk.Entry(self.note_window, width=30)
        self.date_entry.pack(pady=(0, 5), anchor="w")
        self.date_entry.insert(0, str(date.today()))  # Automatically fill with today's date

        # Notes text area
        tk.Label(self.note_window, text="Notes:").pack(anchor="w", pady=(10, 5))
        self.notes_text = tk.Text(self.note_window, width=50, height=10)
        self.notes_text.pack(pady=(0, 20), anchor="w")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.note_window)
        self.buttons_frame.pack(anchor="w")

        # Save button
        self.save_button = tk.Button(self.buttons_frame, text="Save", command=self.save_note)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Cancel button
        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.cancel_note)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def save_note(self):
        title = self.title_entry.get()
        date = self.date_entry.get()
        note = self.notes_text.get("1.0", tk.END).strip()

        if title and date and note:
            save_to_firestore(title, date, note)
            messagebox.showinfo("Note Saved", "Note saved successfully!")
            self.note_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")

    def cancel_note(self):
        self.note_window.destroy()

def save_to_firestore(title, date, note):
    # Get a reference to the database
    notes_ref = db.child("notes")

    # Push the new note data to the database
    new_note_ref = notes_ref.push({
        'title': title,
        'date': date,
        'note': note
    })
