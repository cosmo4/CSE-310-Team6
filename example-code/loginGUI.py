import tkinter as tk
from tkinter import messagebox
from upload import upload
from aiFileTest import summarize
from drawwindow import DrawWindow
from Date_Reminder import DateReminderApp


class LoginWindow:
    """
    Class to handle the login window functionality.
    """
    def __init__(self, root, app):
        """
        Initialize the login window.
        """
        self.root = root
        self.app = app
        self.root.title("Note Manager")
        self.root.geometry("400x300")

        # Create the frame for the login window
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Add a label with instructions
        title_label = tk.Label(self.frame, text=('Please log in with your username and password.\n'
                                                 '\nIf you have never logged in, enter a username and password '
                                                 'and click "Create Account".'), wraplength=350, justify="left")
        title_label.pack(pady=10)

        # Username field
        self.username_label = tk.Label(self.frame, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        # Password field
        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        # Frame to hold the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        # Create account button
        self.create_account_button = tk.Button(self.button_frame, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=0, column=0, padx=5)

        # Sign in button
        self.sign_in_button = tk.Button(self.button_frame, text="Sign In", command=self.sign_in)
        self.sign_in_button.grid(row=0, column=1, padx=5)

    def create_account(self):
        """
        Handle user account creation.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            messagebox.showinfo("Account Created", "Account created successfully. You can now sign in.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password")

    def sign_in(self):
        """
        Handle user sign-in.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.app.open_main_window()
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password")

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
        self.set_reminder_button = tk.Button(self.button_frame, text="Set Reminder", command=self.date_reminder, width=20, height=2)
        self.set_reminder_button.pack(pady=10)

        # Upload Notes button
        self.upload_notes_button = tk.Button(self.button_frame, text="Upload Notes", width=20, height=2, command=self.open_file)
        self.upload_notes_button.pack(pady=10)

        # Text entry box on the right side
        self.text_entry = tk.Text(self.frame, wrap=tk.WORD)
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Function to get the testing days and set the reminder
    def date_reminder(self):
        reminder = DateReminderApp(self.root)

    # Function to launch the drawing window
    def open_draw_window(self):
        draw_window = DrawWindow(self.root)

    def open_file(self):
        file_name, text = upload()

        # file_name = os.path.basename(file_name)
        # self.title_entry.delete(0, tk.END)
        # self.title_entry.insert(0, file_name)

        self.text_entry.delete(1.0, tk.END)
        self.text_entry.insert(tk.END, text)

        # display save button and saving function

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

