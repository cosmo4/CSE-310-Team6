# i created this file to experiment and familiarize myself with tkinter, as well as get it working with a firestore db.

import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

# reference the firebase private key JSON that authorizes the program to write to the database
cred = credentials.Certificate(r"C:\Users\cjand\OneDrive - BYU-Idaho\CSE 310\Team Project\notes-manager-81e62-firebase-adminsdk-ueu3m-b003348f0b.json")
firebase_admin.initialize_app(cred)

# store the firestore call as the variable db
db = firestore.client()

def create_new_note():
    def save_note():
        # Get title, date, and notes from entry fields and text area
        title = title_entry.get()
        date = date_entry.get()
        note = notes_text.get("1.0", tk.END)
        
        # Save the note to Firestore
        save_to_firestore(title, date, note)
        
        # Show message box indicating successful save
        messagebox.showinfo("Note Saved", "Note saved successfully!")
        
        # Close the note window
        note_window.destroy()

    def cancel_note():
        # Close the note window without saving
        note_window.destroy()

    # Create a new window for creating a note
    note_window = tk.Toplevel(root)
    note_window.title("New Note")

    # Set padding for the window
    note_window["padx"] = 20
    note_window["pady"] = 20

    # Title entry
    tk.Label(note_window, text="Title:").pack(anchor="w")
    title_entry = tk.Entry(note_window, width=30)
    title_entry.pack(pady=(5, 2), anchor="w")

    # Date entry
    tk.Label(note_window, text="Date:").pack(anchor="w")
    date_entry = tk.Entry(note_window, width=30)
    date_entry.pack(pady=(2, 2), anchor="w")

    # Notes text area
    tk.Label(note_window, text="Notes:").pack(anchor="w")
    notes_text = tk.Text(note_window, width=50, height=10)
    notes_text.pack(pady=(2, 5), anchor="w")

    # Buttons frame
    buttons_frame = tk.Frame(note_window)
    buttons_frame.pack(anchor="w")
    
    # Save and Cancel buttons
    save_button = tk.Button(buttons_frame, text="Save", command=save_note)
    save_button.pack(side=tk.LEFT, padx=5)
    cancel_button = tk.Button(buttons_frame, text="Cancel", command=cancel_note)
    cancel_button.pack(side=tk.LEFT, padx=5)

def save_to_firestore(title, date, note):
    # Add a new document with auto-generated ID to Firestore collection 'notes'
    db.collection('notes').add({
        'title': title,
        'date': date,
        'note': note
    })

def view_previous_notes():
    # Fetch notes from Firestore
    notes = db.collection('notes').get()

    # Display notes in a new window
    notes_window = tk.Toplevel(root)
    notes_window.title("Previous Notes")

    # Display notes in a text area
    notes_text = tk.Text(notes_window, width=80, height=20)
    notes_text.pack(pady=10, padx=10)

    # Iterate over each note document, format and display in the text area
    for note in notes:
        note_data = note.to_dict()
        notes_text.insert(tk.END, f"Title: {note_data['title']}\nDate: {note_data['date']}\nNote: {note_data['note']}\n\n")

def close_window():
    # Close the main window
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Note Manager")

# Set main window size and padding
root.geometry("400x200")
root["padx"] = 20
root["pady"] = 20

# Create 'Create New Note' button (where button is, what text displays, what it does, alignment)
create_note_button = tk.Button(root, text="Create New Note", command=create_new_note, anchor="w")
create_note_button.pack(pady=10, anchor="w")

# Create 'View Previous Notes' button
view_notes_button = tk.Button(root, text="View Previous Notes", command=view_previous_notes, anchor="w")
view_notes_button.pack(pady=10, anchor="w")

# Run the Tkinter event loop
root.mainloop()