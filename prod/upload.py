from tkinter import filedialog
import docx2txt

def upload():

    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("word files", "*.docx*")))

    if filename[-5:] == '.docx':
        with open(filename, 'rb') as r_file:
            text = docx2txt.process(r_file)


    if filename[-4:] == '.txt':
        with open(filename, 'r') as r_file:
            text = r_file.read()

    return text