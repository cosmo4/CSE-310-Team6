from tkinter import *
import requests
import json

# initialize tkinter window
root = Tk()
# title of window
root.title('Weather App Tkinter')

# window size in pixels
root.geometry("800x300")

# api_key = "9DF650B5-C018-43DF-A9B0-1EDF15BFD5D2"
green = "#00e400"
yellow = "#ffff00"
orange = "#ff7e00"
red = "#ff0000"
purple = "#8f3f97"
maroon = "#7e0023"

# function to call to the weather api and decide what to do with that info
def zipLookup():

    try:
        api_request = requests.get(f"https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode={zip.get()}&date=2024-05-01&distance=25&API_KEY=9DF650B5-C018-43DF-A9B0-1EDF15BFD5D2")

        # format the json data
        api = json.loads(api_request.content)

        # access the information
        city = api[0]['ReportingArea']
        quality = api[0]['AQI']
        category = api[0]['Category']['Name']

        # decision on background color
        if category == 'Good':
            weather_color = green
        elif category == 'Moderate':
            weather_color = yellow
        elif category == 'Unhealthy for Sensitive Groups':
            weather_color = orange
        elif category == 'Unhealthy':
            weather_color = red
        elif category == 'Very Unhealthy':
            weather_color = purple
        elif category == 'Hazardous':
            weather_color = maroon
        
        # set the background color to variable 'weather_color'
        root.configure(background=weather_color)

        # Creates a label so the information can be displayed in the window
        myLabel = Label(root, text=f"{city} Air Quality {quality} {category}", font=('Helvetica', 20), background=weather_color)

        # sets the location of the label
        myLabel.grid(row=1, column=0, columnspan=2)

    except Exception as e:
        api = "Error"

# creates an input object on the window and sets its location
zip = Entry(root)
zip.grid(row=0, column=0)

# creates the button and links the command to run zipLookup function
zipButton = Button(root, text="Lookup Zipcode", command=zipLookup)
zipButton.grid(row=0, column=1)

# IMPORTANT - Runs the code until you close out of the window
root.mainloop()