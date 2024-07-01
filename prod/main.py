import tkinter as tk
from tkinter import messagebox
from upload import upload
from summarizeNote import summarize
from drawwindow import DrawWindow
from login import LoginWindow
from newnote import NewNoteWindow, ViewNoteWindow
from Date_Reminder import DateReminderApp
import pyrebase

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

# Initialize pyrebase and assign variables
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class MainWindow:
    """
    Class to handle the main window functionality.
    """
    def __init__(self, root, user):

        # Initialize the main window.
        self.user = user
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
        self.new_note_button = tk.Button(self.button_frame, text="New Note", width=20, height=2, command=self.open_new_note_window)
        self.new_note_button.pack(pady=10)

        # Summarize button
        self.summarize_button = tk.Button(self.button_frame, text="Summarize", width=20, height=2, command=lambda: summarize(user))
        self.summarize_button.pack(pady=10)

        # Draw button
        self.draw_button = tk.Button(self.button_frame, text="Draw", command=self.open_draw_window, width=20, height=2)
        self.draw_button.pack(pady=10)

        # Set Reminder button
        self.set_reminder_button = tk.Button(self.button_frame, text="Set Reminder", command=self.open_date_reminder, width=20, height=2)
        self.set_reminder_button.pack(pady=10)

        # Upload Notes button
        self.upload_notes_button = tk.Button(self.button_frame, text="Upload Notes", width=20, height=2, command=self.open_upload_file)
        self.upload_notes_button.pack(pady=10)

        # Listbox to display notes
        self.notes_listbox = tk.Listbox(self.frame)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notes_listbox.bind("<Double-1>", self.open_note)

        # Load notes from the database
        self.load_notes()

    # Function to convert uploaded document into text when the button is pressed
    def open_upload_file(self):
        text = upload()
        if text is not None:
            self.open_new_note_window(text)

    # Function to launch the drawing window when the button is pressed       
    def open_draw_window(self):
        draw_window = DrawWindow(self.root, self.user)
            
    def open_date_reminder(self):
        reminder = DateReminderApp(self.root)

    def open_new_note_window(self, text=""):
        new_note = NewNoteWindow(self.root, self.user, self, text)

    # Function to retrieve user notes from the db and display in listbox
    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)  # Clear the listbox
        try:
            notes = db.child("notes").child(self.user['localId']).get(self.user['idToken']).val()
            if notes:
                for note_id, note in notes.items():
                    note['id'] = note_id  # Assign the Firebase note ID to 'id' field
                    note_display_text = f"{note['title']} ({note['date']})"
                    self.notes_listbox.insert(tk.END, note_display_text)
            else:
                self.notes_listbox.insert(tk.END, "No notes available.")
        except Exception as e:
            messagebox.showwarning("Error", f"Failed to load notes: {e}")

    # Function to open user note when double clicked in the listbox
    def open_note(self, event):
        selected_index = self.notes_listbox.curselection() 
        if selected_index:
            selected_note_display_text = self.notes_listbox.get(selected_index) # Retrieve text from db
            selected_note_title = selected_note_display_text.split(" (")[0]  # Extract the title part
            notes = db.child("notes").child(self.user['localId']).get(self.user['idToken']).val()
            for note_id, note in notes.items(): 
                if note['title'] == selected_note_title:
                    note['id'] = note_id  # Ensure 'id' is assigned here
                    ViewNoteWindow(self.root, note, self)  # Pass self as main_window
                    break

class NoteManagerApp:
    """
    Main application class to manage the flow between login and main windows.
    """
    def __init__(self, root):
            
        # Initialize the application with the login window.
        self.root = root
        self.login_window = LoginWindow(self.root, self)
        self.user = None

    def open_main_window(self, user):
        
        # Transition from login window to main window.
        self.user = user
        # Close login window if authentication is successful 
        self.login_window.frame.destroy()
        self.main_window = MainWindow(self.root, self.user)

if __name__ == "__main__":
    # Create the main Tkinter root window
    root = tk.Tk()
    # Initialize and run the application
    app = NoteManagerApp(root)
    root.mainloop()