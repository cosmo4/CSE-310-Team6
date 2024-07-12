### CSE 310 Team 6

Luke Warner, Avery Anderson, Gabe Hayes, Jehyeon Kweon, Corbin Andrus

## Overview

**Project Title**: Note Manager

**Project Description**: User can take, save, summarize, notes, and set review date of the note for the test.

**Project Goals**: Create software that help to manage college students' notes.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Login window

    1. Sign in

        * Add email and password to authentication database in firebase

    2. Log in

        * If the email and password are in the firebase authentication open main window

2. Main window

    * open tkinter window with listbox of notes and buttons

    1. See existing notes

        * Get list of note that inside of user's directory and display on the listbox

        * When user duoble clicked show the specific note with new window

    2. Make new note

        * Open new window with title, date, and notes text entry box

        * Save: Save the title, date, note as dictionary into firebase database, if error occured save the note in local as txt file

        * Cancel: Close the new note window

    3. Get summary of note

        * Get the location of file to sumarize from user

        * Use openAI API to sumarize the note

        * User choose to save the summarized note to firebase or local storage

        * Save the file to the chosen place

    4. Make new note with handwriting

        * Open canvas window to draw or hand writing

        * Draw: draw black color on the canvas

        * Erase: draw white color on the canvas

        * Clear: delete everything on the canvas

        * Save as jpeg: save the canvas as jpeg file in the path that user chose

    5. Set remind date for tests

        * Open new window that has entries of next test month, date, and user's email 

        * Submit: send email that user put in to the entry 2 days before the test date that user gave.

    6. Upload existing note in PC

        * Open file exploreer to get the path of the file that want to be updated from user txt, docx, or jpeg

        * txt or docx file convert into a string or jpg or jpeg file run google vision API to conver to string

        * Open new note window on the note entry with the text insulted



Instructions for using the software:

1. Run main.py

2. Login window

    1. Sign in if you don't have account

    2. Log in with your email and password

3. Main window

    1. See existing notes

        display title of the note that exist in firebase database
        duble click to see the contents of the note

    2. Make new note

        put title and the note in the test boxes and click save button to choose directory to save as jpg file

    3. Get summary of note

        choose note to summarize in the listbox and clock the summrize button and choose the summary into cloud or local storage and where into the storage

    4. Make new note with handwriting

        take note with the drawing canvas 

    5. Set remind date for tests

        Put next test date, month and email address to recieve the reminder and submit 

    6. Upload existing note in PC

        choose txt or doxc file from your computer and check the new window that include the file text
        add title of the note and click save button

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* VScode

* Python
    * tkinter
    * pyrebase
    * pillow
    * openai
    * google

* firebase

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Website Title](Link)
*
*

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] First thing here
* [ ]
* [ ]
