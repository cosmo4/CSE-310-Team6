import tkinter as tk
from datetime import datetime
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, firestore

# reference the firebase private key JSON that authorizes the program to write to the database
cred = credentials.Certificate(r"C:\Users\cjand\OneDrive - BYU-Idaho\CSE 310\Team Project\notes-manager-81e62-firebase-adminsdk-ueu3m-b003348f0b.json")
firebase_admin.initialize_app(cred)

API_KEY = 'AIzaSyC-NJByPVn8XpksSCkSctCja08tr5creYU'

# store the firestore call as the variable db
db = firestore.client()

class NewNoteWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("New Note")

        self.title_label = tk.Label(self, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.date_label = tk.Label(self, text="Date:")
        self.date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to current date
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.text_label = tk.Label(self, text="Text:")
        self.text_label.grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        self.text_entry = tk.Text(self, width=30, height=10)
        self.text_entry.grid(row=2, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self, text="Save", command=self.save_note)
        self.save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def save_note(self):
        title = self.title_entry.get()
        date = self.date_entry.get()
        text = self.text_entry.get("1.0", tk.END)

        # Connect to your Firestore database and save the note
        firebase = firebase.FirebaseApplication('https://console.firebase.google.com/project/notes-manager-81e62/firestore/databases/-default-/data/~2F', None)
        firebase.post('/notes', {'title': title, 'date': date, 'text': text})

        # For demonstration purposes, just print the note details
        print("Title:", title)
        print("Date:", date)
        print("Text:", text)
