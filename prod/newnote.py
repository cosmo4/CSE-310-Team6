import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pyrebase
import os

firebaseConfig = {
                'apiKey': "AIzaSyC-NJByPVn8XpksSCkSctCja08tr5creYU",
                'authDomain': "notes-manager-81e62.firebaseapp.com",
                'databaseURL': "https://notes-manager-81e62-default-rtdb.firebaseio.com",
                'projectId': "notes-manager-81e62",
                'storageBucket': "notes-manager-81e62.appspot.com",
                'messagingSenderId': "88497487267",
                'appId': "1:88497487267:web:e27eb195f07116bdedee16",
                'measurementId': "G-JB077QZ9QM"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class NewNoteWindow:
    def __init__(self, root, user, main_window, text=""):
        self.root = root
        self.user = user
        self.main_window = main_window
        
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
        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        tk.Label(self.note_window, text="Date:").pack(anchor="w", pady=(10, 5))
        self.date_entry = tk.Entry(self.note_window, width=30)
        self.date_entry.pack(pady=(0, 5), anchor="w")
        self.date_entry.insert(0, current_time)  # Automatically fill with today's date

        # Notes text area
        tk.Label(self.note_window, text="Notes:").pack(anchor="w", pady=(10, 5))
        self.notes_text = tk.Text(self.note_window, width=50, height=10)
        self.notes_text.pack(pady=(0, 20), anchor="w")
        self.notes_text.insert("end", text)

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

        data = {"title": title, "date": date, "note": note}

        if title and date and note:
            try:
                db.child("notes").child(self.user['localId']).push(data, self.user['idToken'])
                messagebox.showinfo("Success", "Note saved successfully!")
                self.main_window.load_notes()  # Reload notes
                self.note_window.destroy()
            
            except Exception as e:
                messagebox.showwarning("Error", f"Failed to save note: {e}")
                print("Error:", e)
                print("Data:", data)
                save_local(title, note)
                messagebox.showinfo("Saved Locally", "Error saving to cloud. Note saved locally.")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")

    def cancel_note(self):
        self.note_window.destroy()

def save_local(title, note):
    # Ensure the title is a valid filename (simple sanitization)
    filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).rstrip()

    # Find the correct folder to save the notes. This may need adjustment on final release.
    curr_dir = os.getcwd()
    folder_path = os.path.join(curr_dir,'notes')
    if not os.path.exists(folder_path):
        print(f"No such folder. Making new folder...")
        os.makedirs(folder_path)

    # Construct the full path where the note will be saved
    file_path = os.path.join(folder_path, f"{filename}.txt")

    # Write the content to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(note)
        messagebox.showinfo("Success", f"Note saved successfully as {file_path}")
    except IOError as e:
        messagebox.showerror("Error", f"Failed to save the note: {e}")

class ViewNoteWindow:
    def __init__(self, root, note):
        self.root = root
        self.note = note

        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Note")
        self.view_window.geometry("400x400")

        self.title_label = tk.Label(self.view_window, text="Title:")
        self.title_label.pack(anchor="w")
        self.title_entry = tk.Entry(self.view_window, width=30)
        self.title_entry.insert(0, note['title'])
        self.title_entry.config(state="readonly")
        self.title_entry.pack(anchor="w")

        self.date_label = tk.Label(self.view_window, text="Date:")
        self.date_label.pack(anchor="w")
        self.date_entry = tk.Entry(self.view_window, width=30)
        self.date_entry.insert(0, note['date'])
        self.date_entry.config(state="readonly")
        self.date_entry.pack(anchor="w")

        self.note_label = tk.Label(self.view_window, text="Note:")
        self.note_label.pack(anchor="w")
        self.note_text = tk.Text(self.view_window, width=50, height=10)
        self.note_text.insert(tk.END, note['note'])
        self.note_text.config(state="disabled")
        self.note_text.pack(anchor="w")