# import os
# from tkinter import filedialog
# import docx2txt

# def upload():
#     filename = filedialog.askopenfilename(
#         initialdir=os.getcwd(),
#         title="Select a File",
#         filetypes=(("Text files", "*.txt*"), ("Word files", "*.docx*"))
#     )

#     if not filename:
#         return None  # No file selected

#     text = ""
#     if filename.lower().endswith('.docx'):
#         text = docx2txt.process(filename)
#     elif filename.lower().endswith('.txt'):
#         with open(filename, 'r', encoding='utf-8') as file:
#             text = file.read()

#     return text
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import docx2txt
import io
from google.cloud import vision
from google.cloud.vision_v1 import types

# Initialize Google Cloud Vision API client
def initialize_vision_client():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_directory, 'admin-key.json')

    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_path)
    return client

# Function to upload file and extract text
def upload():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"),
                                                      ("Text files", "*.txt"),
                                                      ("Word files", "*.docx"),
                                                      ("JPEG files", "*.jpg *.jpeg")])
    if file_path:
        if file_path.endswith(('.txt', '.docx')):
            return extract_text_from_file(file_path)
        elif file_path.endswith(('.jpg', '.jpeg')):
            return extract_text_from_image(file_path)
        else:
            return "Unsupported file format."

# Function to extract text from text file
def extract_text_from_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()
    elif file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
    return text

# Function to extract text from image using Vision API
def extract_text_from_image(file_path):
    client = initialize_vision_client()

    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return 'No text found'
