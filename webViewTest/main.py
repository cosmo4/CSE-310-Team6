# First install 'pip install requests==2.11.1'
# pip uninstall pyrebase
# pip install pyrebase4
# pip install setuptools
# 

import pyrebase
import tkinter
import customtkinter

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
auth = firebase.auth()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")

def login():
    email = email_entry.get()
    password = password_entry.get()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        result.configure(text="Successfully logged in!")
    except:
        result.configure(text="Invalid credentials :(")

def signup():
    email = email_entry.get()
    password = password_entry.get()
    try:
        user = auth.create_user_with_email_and_password(email, password)
        result.configure(text="Account created! Confirm signup in your email inbox")
    except:
        result.configure(text="Failed to sign up :(")

email = customtkinter.CTkLabel(master=app,
                                  text = "Email",
                                  width=80,
                                  height=25,
                                  text_color="black",
                                  fg_color=("black", "white"),
                                  corner_radius=8)
email.place(relx=0.3, rely=0.3, anchor=tkinter.CENTER)

password = customtkinter.CTkLabel(master=app,
                                  text = "Password",
                                  width=80,
                                  height=25,
                                  text_color="black",
                                  fg_color=("black", "white"),
                                  corner_radius=8)
password.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

email_entry = customtkinter.CTkEntry(master=app,
                                     placeholder_text="example@email.com",
                                     width=180,
                                     height=25,
                                     text_color="black",
                                     fg_color=("black", "white"),
                                     corner_radius=8)
email_entry.place(relx=0.65, rely=0.3, anchor=tkinter.CENTER)

password_entry = customtkinter.CTkEntry(master=app,
                                     placeholder_text="**********",
                                     width=180,
                                     height=25,
                                     text_color="black",
                                     fg_color=("black", "white"),
                                     corner_radius=8)
password_entry.place(relx=0.65, rely=0.5, anchor=tkinter.CENTER)

login_button = customtkinter.CTkButton(master=app,
                                       width=80,
                                       height=32,
                                       border_width=0,
                                       corner_radius=8,
                                       text="Login",
                                       command=login)
login_button.place(relx=0.71, rely=0.7, anchor=tkinter.CENTER)

signup_button = customtkinter.CTkButton(master=app,
                                       width=80,
                                       height=32,
                                       border_width=0,
                                       corner_radius=8,
                                       text="SignUp",
                                       command=signup)
signup_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

result = customtkinter.CTkLabel(master=app,
                                text = "",
                                width=120,
                                height=25,
                                text_color="black",
                                fg_color=("black", "white"),
                                corner_radius=8)
result.place(relx=0.62, rely=0.85, anchor=tkinter.CENTER)



app.mainloop()

