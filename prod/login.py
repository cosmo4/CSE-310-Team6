import tkinter as tk
from tkinter import messagebox
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
auth = firebase.auth()

class LoginWindow:
    """
    Class to handle the login window functionality.
    """
    def __init__(self, root, app):
        
        # Initialize the login window.
        self.root = root
        self.app = app
        self.root.title("Note Manager")
        self.root.geometry("400x300")

        # Create the frame for the login window
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Add a label with instructions
        title_label = tk.Label(self.frame, text=('Please log in with your email and password.\n'
                                                 '\nIf you have never logged in, enter email and password '
                                                 'and click "Create Account".'), wraplength=350, justify="left")
        title_label.pack(pady=10)

        # email field
        self.email_label = tk.Label(self.frame, text="Email")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5)

        # Password field
        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        # Frame to hold the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        # Create account button
        self.create_account_button = tk.Button(
            self.button_frame, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=0, column=0, padx=5)

        # Sign in button
        self.sign_in_button = tk.Button(
            self.button_frame, text="Sign In", command=self.sign_in)
        self.sign_in_button.grid(row=0, column=1, padx=5)

    # Function to create an account if the button is pressed
    def create_account(self):

        # Assign variables for email and password
        email = self.email_entry.get()
        password = self.password_entry.get()

        # If email and password are valid, create user
        try:
            user = auth.create_user_with_email_and_password(email, password)
            messagebox.showinfo("Account Created", "Account created successfully. Confirm signup in your email inbox.")
        # If email and password are not valid, display error window
        except:
            messagebox.showwarning("Input Error", "Please enter both valid email and password.")

    # Function to sign in the user if the button is pressed
    def sign_in(self):

        # Assign variables for email and password    
        email = self.email_entry.get()
        password = self.password_entry.get()

        # If email and password are valid, sign in user
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            # Open main menu with login info
            self.app.open_main_window(login)
            # Retrieve and store user token
            token = auth.get_account_info(login['idToken'])
        # If email and password are not valid, display error window
        except:
            messagebox.showwarning("Input Error", "Login failed. Please enter both a valid email and password.")