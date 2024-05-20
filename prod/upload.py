from tkinter import *
from tkinter import filedialog
import docx2txt

def upload():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("word files", "*.docx*")))

    if filename[-5:] == '.docx':
        with open(filename, 'rb') as r_file:
            with open('docx2txt.txt', 'w', encoding='utf-8') as w_file:
                text = docx2txt.process(r_file)
                w_file.write(text)

    if filename[-4:] == '.txt':
        with open(filename, 'rb') as r_file:
            with open('txt2txt.txt', 'wb') as w_file:
                done = False
                while not done:
                    block = r_file.read(1024*4)
                    if block:
                        w_file.write(block)
                    else:
                        done = True
            