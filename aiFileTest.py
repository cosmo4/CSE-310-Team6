# This program will upload a chosen file to chatGPT and get a response, then parse and display the response to the user.
### THIS WILL NOT WORK WITHOUT AN OPENAI API KEY ###
### TO APPLY A KEY TYPE "setx OPENAI_API_KEY 'your_api_key'" REPLACING 'your_api_key' WITH YOUR KEY ###
### BE SURE TO ALSO CHANGE file_name TO AN EXISTING FILE ###

# Import OpenAI library
from openai import OpenAI
from openai import OpenAIError
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from tkinter import Listbox, Toplevel
import pyrebase
from threading import Thread

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

def summarize():
   # Initialize an OpenAI client
   client = OpenAI()
   # Set a file path
   file_name = select_file()

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
   citations = []
   for index, annotation in enumerate(annotations):
      # Replace the original text with annotatted references
      message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
      # Retrieve file citations if any
      if file_citation := getattr(annotation, "file_citation", None):
         cited_file = client.files.retrieve(file_citation.file_id)
         citations.append(f"[{index}] {cited_file.filename}")

   messagebox.showinfo(file_name + " Summarized", message_content.value)
   thread = Thread(target = clear_storage, args=(10,))
   thread.start()

def clear_storage(args):
   client = OpenAI()
   # Remove the file and vector store from API storage
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