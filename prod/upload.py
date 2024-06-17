import os
from tkinter import filedialog
import docx2txt

def upload():
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select a File",
        filetypes=(("Text files", "*.txt*"), ("Word files", "*.docx*"))
    )

    if not filename:
        return None  # No file selected

    text = ""
    if filename.lower().endswith('.docx'):
        text = docx2txt.process(filename)
    elif filename.lower().endswith('.txt'):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

    return text
