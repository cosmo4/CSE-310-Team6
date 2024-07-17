# This program will upload a chosen file to chatGPT and get a response, then parse and display the response to the user.
### THIS WILL NOT WORK WITHOUT AN OPENAI API KEY ###
### TO APPLY A KEY TYPE "setx OPENAI_API_KEY 'your_api_key'" REPLACING 'your_api_key' WITH YOUR KEY ###

# Import OpenAI library
import openai
from openai import OpenAI
from openai import OpenAIError
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from tkinter import Listbox, Toplevel
import pyrebase
from threading import Thread
import ntpath
from datetime import datetime

# Firebase info - Could we put this in one place and pass it into various files?
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

def file_location(user):
   def select_location(args):
      if args == 0:
         dialog.file = select_firebase(user)
      else:
         dialog.file = select_file()
      dialog.destroy()

   dialog = Toplevel()
   dialog.title("Select file location")
   l = Label(dialog, text="Where is your note stored?")
   l.pack(side="top")
   
   firebase_button = tk.Button(dialog, text="Cloud", command=lambda: select_location(0))
   firebase_button.pack(pady=10, padx=5, side="left")

   local_button = tk.Button(dialog, text="Local", command=lambda: select_location(1))
   local_button.pack(pady=10, padx=5, side="right")

   dialog.wait_window()
   return dialog.file

def select_firebase(user):
   def open_note():
      selected_index = listbox.curselection()
      if selected_index:
         selected_note_text = listbox.get(selected_index)
         selected_note_title = selected_note_text.split(" (")[0]
         notes = db.child("notes").child(user['localId']).get(user['idToken']).val()
         for note_id, note in notes.items():
            if note['title'] == selected_note_title:
               note['id'] = note_id
               new_file(note)
               dialog.destroy()

   def new_file(file_info):
      notes_path = os.path.join(os.getcwd(), 'note_to_summarize')
      if not os.path.exists(notes_path):
         os.makedirs(notes_path)
      file_location = os.path.join(notes_path, f"{file_info['title'].replace(' ','_')}.txt" )
      file = open(file_location, "w")
      file.write(file_info['note'])
      file.close()
      dialog.user_selected_file = file_location

   # Get all file names from Firebase Storage
   def fetch_files(user):
      notes = db.child("notes").child(user['localId']).get(user['idToken']).val()
      if notes:
         for note_id, note in notes.items():
            note['id'] = note_id
      return [note for note in notes.items()]

   # Create a new window for file selection
   dialog = Toplevel()
   dialog.title("Select a file from Firebase")
   dialog.grab_set()
   listbox = Listbox(dialog, width=50, height=10)
   listbox.pack(padx=20, pady=20)

   # Fetch and list files from Firebase
   try:
      files = fetch_files(user)
      for file in files:
         listbox.insert(tk.END, file[1]['title'])
   except Exception as e:
      messagebox.showerror("Error", f"Failed to list files from Firebase: {e}")
      return

   # Button to confirm selection
   select_button = tk.Button(dialog, text="Select", command=open_note)
   select_button.pack(pady=10)

   dialog.user_selected_video_file = None
   dialog.wait_window()

   return dialog.user_selected_file

def select_file():
   # Function to handle selection
   def on_select():
      selection = listbox.curselection()
      if selection:
         selected_file = listbox.get(selection[0])
         dialog.user_selected_file = os.path.join(folder_path, selected_file)
         print("Selected:", dialog.user_selected_file)
         dialog.destroy()  # Close the dialog

   curr_dir = os.getcwd()
   folder_path = os.path.join(curr_dir,'notes')
   if not os.path.exists(folder_path):
        print(f"Not such folder. Making new folder...")
        os.makedirs(folder_path)
   try:
      files = os.listdir(folder_path)
   except Exception as e:
      print("Failed to list files:", e)
      return

   # Create a new window for file selection
   dialog = Toplevel()
   dialog.title("Select a file")
   dialog.grab_set()
   listbox = Listbox(dialog, width=50, height=10)
   listbox.pack(padx=20, pady=20)

   # Populate the listbox with files
   for file in files:
      listbox.insert(tk.END, file)

   # Button to confirm selection
   select_button = tk.Button(dialog, text="Select", command=on_select)
   select_button.pack(pady=10)

   dialog.user_selected_file = None
   dialog.wait_window()

   return dialog.user_selected_file

def summarize(user, self):
   # Initialize an OpenAI client
   client = OpenAI()
   # Open AI API key - Should hide this is pushed live
   client.api_key = 'sk-proj-H1gRZpqPmXLgfY1T5PPGT3BlbkFJw1QFp8QZw3AdRmhB8DfO'
   # Set a file path
   file_name = file_location(user)

   # Create a new assistant named "Note Summarizer" using the gpt-3.5-turbo model with the given instructions
   assistant = client.beta.assistants.create(
   name="Note Summarizer",
   model="gpt-3.5-turbo",
   instructions="You are a note summarizer. You read a text document and summarize the key points of college student's notes.",
   # Make sure the file_search tool is used in order to upload and read files
   tools=[{"type":"file_search"}],
   )

   # Create a vector store to store the notes documents
   vector_store = client.beta.vector_stores.create(name="Notes")

   # Update the assistant to use the vector store for file access
   assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search":{"vector_store_ids":[vector_store.id]}},
   )

   # Create a message file containing the notes
   message_file = client.files.create(
      file=open(file_name, "rb"), purpose="assistants"
   )

   # Create a thread to interact with the assistant
   thread = client.beta.threads.create(
      messages=[
         {
            "role": "user",
            "content": "Summarize these notes in a more compressed manner. They should still be useable as notes for the various topics, just shortened and summarized.",
            "attachments": [
               { "file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ]
         }
      ]
   )

   # Run the assistant
   run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id, assistant_id=assistant.id
   )

   # Retrieve the message from the assistant
   messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

   # Extract the content of the message
   message_content = messages[0].content[0].text
   # Extract any annotations and citations from the content
   annotations = message_content.annotations
   for index, annotation in enumerate(annotations):
      # Replace the original text with annotatted references
      message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
      # Retrieve file citations if any
      if file_citation := getattr(annotation, "file_citation", None):
         cited_file = client.files.retrieve(file_citation.file_id)

   os.remove(file_name)

   messagebox.showinfo(ntpath.basename(file_name) + " Summarized", message_content.value)
   thread = Thread(target = clear_storage, args=(10,))
   thread.start()
   save_summary(file_name, message_content.value, self)

3# Remove the file and vector store from API storage
def clear_storage(args):
   client = OpenAI()
   try:
      file_list = client.files.list()
      for file in file_list:
         try:
            client.files.delete(file.id)
            print(f"Deleted file with ID: {file.id}")
         except OpenAIError as e:
            print(f"Failed to delete file with ID: {file.id}. Error: {e}")
      
      vector_store_list = client.beta.vector_stores.list()
      for vector in vector_store_list:
         try:
            client.beta.vector_stores.delete(vector.id)
            print(f"Deleted vector store with ID: {vector.id}")
         except OpenAIError as e:
            print(f"Failed to delete vector store with ID: {vector.id}. Error: {e}")

   except OpenAIError as e:
      print(f"An error occurred while deleting: {e}")

# The function to allow saving a summary
def save_summary(file_path, summarized_note, self):

   # Saving locally
   def save_locally(final_path):
      file = open(final_path, "w")
      file.write(summarized_note)
      messagebox.showinfo("File saved.")

   #Saving to the cloud
   def save_to_cloud(file_name):
      data = {"title": file_name, "date": datetime.now().strftime("%m/%d/%Y %H:%M:%S"), "note": summarized_note}
      try:
         # Check to make sure it's not creating duplicates
         notes = db.child("notes").child(self.user['localId']).get(self.user['idToken']).val()
         for note_id, note in notes.items():
            if note['title'] == file_name:
               db.child("notes").child(self.user['localId']).child(note_id).remove(self.user['idToken'])
         # Push the summary to the cloud
         db.child("notes").child(self.user['localId']).push(data, self.user['idToken'])
         messagebox.showinfo("Success", "Note saved successfully!") # Display success message
      except Exception as e:
         messagebox.showwarning("Error", f"Failed to save note: {e}")
   
   # Ask user if they want to save the summary
   if messagebox.askyesno("Save Summary", "Do you want to save the summary?"):
      summary_window = Toplevel()
      summary_window.title("Save Summary")
      Label(summary_window, text="Choose where to save the summary:").pack(pady=10)

      # Make buttons to save locally or on the cloud
      local_save_button = tk.Button(summary_window, text="Save Locally", command=lambda: save_locally(final_path))
      local_save_button.pack(pady=10, padx=5, side="left")

      cloud_save_button = tk.Button(summary_window, text="Save to Cloud", command=lambda: save_to_cloud(file_name))
      cloud_save_button.pack(pady=10, padx=5, side="right")

      summarized_folder_path = os.path.join(os.getcwd(), 'notes')
      file_name = ntpath.basename(file_path[:-4]) + "_summary.txt"
      final_path = os.path.join(summarized_folder_path, file_name)

      summary_window.wait_window()

      summary_window.mainloop()
