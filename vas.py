import spacy
import random
import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import subprocess
import pyautogui
import wikipedia
import os
import sys
import cv2
import wmi
import psutil
import pywhatkit
import pyjokes
import requests
import webbrowser
from geopy.geocoders import Nominatim
from urllib.parse import quote
from googletrans import Translator
from translate import Translator
from PyDictionary import PyDictionary
import datetime
import pygame
from art import *
from termcolor import colored
from email.mime.text import MIMEText
from email .mime.multipart import MIMEMultipart
import time
import smtplib

name = "IRIS"

# Create ASCII art of the name in large size
ascii_art = text2art(name, font='block')

# Print the colored ASCII art
colored_art = colored(ascii_art, 'red')
print(colored_art)



r = sr.Recognizer()
engine = pyttsx3.init()
#cur_time = int(datetime.datetime.now().hour)
cur_time = datetime.datetime.now().strftime("%H:%M:%S")

#smtp server creds
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_mail = "ajaysajuloo@gmail.com"
sender_pass = "Ajaysajuloo7#"


def speak(phrase):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(phrase)
    engine.runAndWait()


def user_listen():
    with sr.Microphone() as source:
        print("Listening active...")
        r.pause_threshold = 0.6
        r.adjust_for_ambient_noise(source)
        aud_in = r.listen(source)
        try:
            print("Recognizing User Input...")
            usr_aud = r.recognize_google(aud_in, language='en-in')
            print(f"User: {usr_aud}")



        except sr.UnknownValueError as e:
            print("[!]Exception occured!", e)
            speak("Sorry")
            speak("I didn't quite understand what you just said.")
    return usr_aud



# Load the pre-trained model
nlp = spacy.load("en_core_web_lg")

intents = {
    "send mail": ["Send a mail for me", "Prepare a mail for me"],
    "dictionary":["open dictionary","dictionary"],
    "translate":["translate language","translate"],
    "find location":["find location","location please"],
    "current news":["current news","get the news"],
    "todo list":["todo","create a todo","todo list","create a todo list"],
    "screenshort":["screenshort please","windows capture"],
     "reminder": ["make a reminder for me", "set a reminder"],
    "greeting": ["hello", "hi", "hey"],
    "parting": ["bye", "goodbye", "see you"],
    "weather": [
        "what's the weather like today?", "will it rain today?",
        "is it sunny outside?"
    ],
    "who are you": ["Who are you", "Tell me about yourself","what can you do","what are your abilities"],
    "Spawn dir": [
        "Create a folder", "Make a folder", "Create a directory",
        "Make a directory"
    ],
    "Spawn file":
    ["Create a file", "Make a file", "Create a file", "Make a file"],
    "Make note": ["Make a note for me", "Create a note", "Write a note"],
    "search": [
        "search", "find", "check", "what is", "who is", "explain",
        "Tell me about", "what do you know about", "wikipedia", "why is",
        "who was", "what was", "why was", "where was", "where is"
    ],
    "open file": ["open a file for me", "open a file"],
    "delete file":["delete a file for me","remove a file","delete a file"],
    "rename file":["rename a file foe me","rename a file"],
    "update file":["update a file","edit file","update file"],
    "create file":["create a file for me","create a file"],
    "move file":["move a file for me","move a file"],
    "shutdown": ["shutdown system", "poweroff"],
    "restart": ["restart system"],
    "brightness":["brightness of your system","set brightness"],
    "battery charge":["battery charge","battery charge please"],
    "run app": ["open app", "run app","run application","open application"],
    "takepicture":["take a picture","photo please"],
    "play song":["play","play a song","play music"],
    "jokes":["tell a joke","joke"]
   
    
    # Add more intents as per your requirements
}

def introduce():
    intros = [
        "I am iris, your AI assistant developed using Python. I am programmed to provide assistance to you on your PC.Let's get started. How may I help you?",
        "I'm iris. Your very own virtual assistant. I'm programmed to to aid you in getting things done on your PC. I can help you out with a variety of chores. How may be of assistance to you?"
    ]
    speak(random.choice(intros))

def make_note():
    today = datetime.date.today().strftime('%Y-%m-%d')
    speak("What do you want me to write in the note?")
    note_text = user_listen()
    with open("note.txt", "a") as f:
        f.write(f"{today} - {note_text}\n")
    speak("Note saved successfully.")




class Task:
    def __init__(self, name):
        self.name = name
        self.due_date = datetime.datetime.now()


    def __str__(self):
        return f"{self.name} (due {self.due_date.strftime('%A, %B %d, %Y at %I:%M %p')})"

class ToDoList:
    def __init__(self, filename):
        self.tasks = []
        self.filename = filename

    def add_task(self, task):
        self.tasks.append(task)
        speak(f"Added task: {task}")
        self.save_to_file()

    def remove_task(self, task):
        try:
            self.tasks.remove(task)
            speak(f"Removed task: {task}")
            self.save_to_file()
        except ValueError:
            speak(f"'{task}' not found in the to-do list.")

    def view_tasks(self):
        if not self.tasks:
            speak("To-do list is empty.")
        else:
            speak("To-do list:")
            for i, task in enumerate(self.tasks, start=1):
                speak(f"{i}. {task}")

    def save_to_file(self):
        with open(self.filename, "w") as f:
            for task in self.tasks:
                f.write(f"{task.name},{task.due_date}\n")

    def load_from_file(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    name, due_date = line.strip().split(",")
                    self.tasks.append(Task(name))
                    self.tasks[-1].due_date = datetime.fromisoformat(due_date)
                speak(f"Loaded {len(self.tasks)} tasks from {self.filename}.")
        except FileNotFoundError:
            speak(f"{self.filename} not found. Starting with an empty to-do list.")

def todo_list(filename):
    # create an instance of the ToDoList class with the specified filename, and load tasks from file (if it exists)
    todo = ToDoList(filename)
    todo.load_from_file()

    while True:
        print("\nMenu:")
        print("1. Add task")
        print("11. Remove task")
        print("111. View tasks")
        print("5. Quit")

        speak("Enter your choice: ")
        choice = user_listen()

        if choice == "1":
            speak("Enter task name: ")
            name =user_listen()
            todo.add_task(Task(name))
        elif choice == "11":
            speak("Enter task name: ")
            name =user_listen()
            todo.remove_task(Task(name))
        elif choice == "111":
            todo.view_tasks()
        elif choice == "4":
            speak("Goodbye!")
            break
        else:
            speak("Invalid choice. Please try again.")

    # save the to-do list to file before exiting
    todo.save_to_file()





def set_reminder():
    # Get the reminder text from the user
    speak("Enter the reminder text: ")
    reminder_text=user_listen()
    # Get the date and time for the reminder from the user
    speak("Enter the year: ")
    year = user_listen() 
    speak("Enter the month: ")
    month = user_listen()
    speak("Enter the day: ")
    day =user_listen()
    speak("Enter the hour: ")
    hour = user_listen()
    speak("Enter the minute: ")
    minute =user_listen()
    # create a datetime object for the reminder
    reminder_time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    # calculate the number of seconds between now and the reminder time
    seconds_until_reminder = (reminder_time - datetime.datetime.now()).total_seconds()

    # convert the reminder time to a string for display
    reminder_time_string = reminder_time.strftime('%Y-%m-%d %H:%M:%S')

    # print a message indicating when the reminder will go off
    speak(f"Reminder set for {reminder_text} on {reminder_time_string}...")

    # wait for the reminder time
    time.sleep(seconds_until_reminder)

    # Initialize pygame
    pygame.init()

# Load the sound file
    sound = pygame.mixer.Sound('tone.wav')

# Play the sound
    sound.play()

# Wait for the sound to finish playing
    pygame.time.wait(int(sound.get_length() * 1000))

# Clean up
    pygame.quit()

    # print the reminder message
    speak(f"Reminder: {reminder_text}")
    





def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def play_song(song_name):
    doc = nlp(song_name)
    song = ''
    for i in doc:
        if i.text == 'play':
            continue
        song = song + i.text
    try:
        speak("Alright")
        speak(f"Playing f{song}")
        pywhatkit.playonyt(song)

    except sr.UnknownValueError as e:
        speak("Pardon me")
        speak("I couldn't quite understand what you said")

    except pywhatkit.exceptions.VideoUnavailable as e:
        speak("Sorry")
        speak("I couldn't find the requested song on youtube")




def greet():
    greet_phrase = ""
    response = [
        "How may I help you?", "How may I be of service",
        "What can I do for you?"
    ]
    if (cur_time < 12):
        greet_phrase = "Good morning"
    elif (12 <= cur_time < 18):
        greet_phrase = "Good afternoon"
    else:
        greet_phrase = "Good evening"
    out = random.choice(["Hi there", "Hello there", "Hey there"
                         ]) + greet_phrase + random.choice(response)
    speak(out)


def say_goodbye(input_text):
    responses = ["Goodbye!", "Bye!", "See you!","Catch ya later"]
    return random.choice(responses)


# Add more actions as per your requirements


#Function to process user voice input
def process_input(input_text):
    # Tokenize the input
    doc = nlp(input_text)

    # Extract the named entities
    named_entities = [(entity.text, entity.label_) for entity in doc.ents]

    # Perform part-of-speech tagging
    pos_tags = [(token.text, token.pos_) for token in doc]

    # Code to identify the intent of the input and return the action to perform
    intent = None
    max_similarity = 0
    for key, samples in intents.items():
        for sample in samples:
            sample_doc = nlp(sample)
            similarity = doc.similarity(sample_doc)
            if similarity > max_similarity:
                max_similarity = similarity
                intent = key
    return intent, max_similarity


#Function to fetch weather data
def get_weather(location):
    responses = [
        "fetching weather updates", "here are the weather updates",
        "the weather updates are as follows"
    ]
    response = random.choice(responses)
    speak(response)
    url = f"https://www.weather-forecast.com/locations/{location}/forecasts/latest"
    webbrowser.open_new_tab(url)
    phrase = random.choice(responses) + f"for {location}"
    speak(phrase)

#FUNCTION TO SEND MAIL
def send_mail():
    recipient_name = ''
    ext = '@gmail.com'
    speak("Tell me the name of the recipient")
    resp1 = user_listen()
    # recipient_mail_id = extract_email_addresses(resp1)
    tok = nlp(resp1)
    for ent in tok.ents:
        if ent.label_ == 'PERSON':
            recipient = ent.text

    speak("Specify the recipient email address")
    rec=input("enter me the name of the recipient")
    #rec = user_listen()
    rec = rec.strip()
    rec.replace(" ", "")
    rec = rec + ext
    speak("What is the subject of the mail")
    subject = user_listen()
    speak(
        random.choice([
            "What should the mail say",
            "What should be the content of the mail",
            "Please specify the mail content"
        ]))
    content = user_listen()

    message = MIMEMultipart()
    message["From"] = sender_mail
    message["To"] = rec
    message["Subject"] = subject

    message.attach(MIMEText(content, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_mail, sender_pass)
        server.send(message)
        server.quit()
        speak("Your email has been sent successfully")

    except Exception as e:
        speak("Sorry")
        speak(
            random.choice([
                "There seems to be trouble sending your mail",
                "Your mail couldn't be sent due to some unexpected error",
                "Something went wrong while sending your mail"
            ]))
        speak("Please try again later")

#Function to open/run an application program on the system
def run_app(user_input):
    doc = nlp(user_input)
    app_name = ""
    for token in doc:
        if token.pos_ == "PROPN":
            app_name += token.text + " "
    app_name = app_name.strip()
    try:
        speak(f'Opening {app_name}')
        pyautogui.press('win')
        pyautogui.typewrite(app_name)
        pyautogui.press('enter')

    except Exception as e:
        speak(f"Pardon. Couldn't open {app_name}")
        speak("Please try again")

#FUNCTION TO PERFORM RESTART SYSTEM

def restart_computer(user_input):
    speak("Got it")
    speak("Restarting your computer now")
    os.system("shutdown /r /t 1")
    

#FUNCTION TO PERFORM SYSTEM SUTDOWN

def shutdown(user_input):
    speak("Got it")
    speak("Shutting down your system now")
    os.system("shutdown /s /t 1") # shutdown the system after 1 second delay
    

#TAKING PICTURe

# Define the required functions
def take_picture(user_input):
    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened
    if not cap.isOpened():
        raise IOError("Couldn't open webcam")

    # Set the resolution of the camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Capture a frame from the camera
    ret, frame = cap.read()
    speak("Image captured")
    speak("Under what name should I save the image")
    im=user_listen()
    im1=im+".jpg"
    # Save the frame as a JPEG file
    cv2.imwrite(im1, frame)

    # Release the camera
    cap.release()

    speak(f"Your the image has been saved as '{im1}'..")

#TAKE A SCREENSHORT
def screenshort():

    # take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    speak("Under what name should I save the screenshot")
    im=user_listen()
    im1=im+".png"
    # save the screenshot to a file
    screenshot.save(im1)
    speak(f"Picture taken and saved as '{im1}'..")


#OPENING A FILE
def openfile(filename):
        path = os.path.join(os.path.expanduser('~'), filename)
        speak("this is path..")
        speak(path)
        if os.path.exists(path):
            speak("File has been found")
            speak("opening file now")
            os.startfile(path)
        
        else:
            speak(f"File '{filename}' not found.")
#DELETING A FILE
def deletefile(filename):
    path = os.path.join(os.path.expanduser('~'), filename)

    if os.path.exists(path):
        os.remove(path)
        speak(f"File '{filename}' deleted successfully!")
    else:
        speak(f"File '{filename}' not found.")

#RENAME A FILE
def renamefile(filename):
    speak("What would you like to rename the file to?: ")
    new_filename=user_listen()
    old_path = os.path.join(os.path.expanduser('~'),filename)
    new_path = os.path.join(os.path.expanduser('~'), new_filename)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        speak(f"File renamed from '{filename}' to '{new_filename}' successfully!")
    else:
        speak(f"File '{filename}' not found.")
#UPDATE A FILE
def updatefile(filename,u):
    path = os.path.join(os.path.expanduser('~'), filename)
    if os.path.exists(path):
        with open(path, 'a') as file:
            file.write("\n")
            file.write(u)
            speak(f"File '{filename}' updated successfully!")
    else:
             speak(f"File '{filename}' not found.")

#CREATE A FILE
def createfile(cr,cn):

    path = os.path.join(os.path.expanduser('~'),cr)

    with open(path, 'w') as file:
        file.write(cn)

    speak(f"File '{cr}' created successfully!")
#MOVE A FILE to folder
def movefile(filename,destination_folder):
    source_path = os.path.join(os.path.expanduser('~'), filename)

    if os.path.exists(source_path):
        destination_path = os.path.join(os.path.expanduser('~'), destination_folder, filename)

    if not os.path.exists(os.path.join(os.path.expanduser('~'), destination_folder)):
        os.mkdir(os.path.join(os.path.expanduser('~'), destination_folder))

        os.rename(source_path, destination_path)
        speak(f"File '{filename}' moved successfully to '{destination_folder}'.")
    else:
        speak(f"File '{filename}' not found.")

#BRIGHTNESS OF YOUR SYSTEM
def set_brightness(brightness):
    brightness = int(brightness) # convert to value between 0 and 255
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)
    speak("brightness is successfully adjusted as per your requirement ")
#BATTERY CHARGE
def get_battery_charge():
    battery = psutil.sensors_battery()
    if battery is None:
        speak("Battery information not available")
    else:
        percent = battery.percent
        plugged = battery.power_plugged
        status = "plugged in" if plugged else "not plugged in"
        speak(f"Battery is {status}, {percent}% charged.")

#NEWS READ
def news(place):
    # set up your News API key
    NEWS_API_KEY = 'b2fc4764a20c4de5b7d407f017fd80c3'


    # make a request to the News API to get the news articles for the given place
    url = f'https://newsapi.org/v2/everything?q={place}&pageSize=5&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    # display the headlines and sources
    for article in data['articles']:
        speak(f"{article['title']} - {article['source']['name']}")
        speak(article['description'])
        speak(article['url'])
        
#FUNCTION TO SHOW MAp

# Function to open Google Maps and fetch the exact location the user requested
def find_location(location):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(location)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        url = f"https://www.google.com/maps/@{latitude},{longitude},17z"
        query = quote(location.address)
        marker_url = f"https://www.google.com/maps/search/?api=1&query={query}&query_place_id={location.raw['place_id']}"
        webbrowser.open_new_tab(marker_url)
        webbrowser.open_new_tab(url)
    else:
        speak("Sorry, I could not find the location you requested.")


#TRANSLATOR
def translate(words,destination_lang ):    
    print(words)
    print(destination_lang)

    translator = Translator(to_lang=destination_lang)
    translation = translator.translate(words)

    print(translation)


    print(translation)
    speak(translation)

#DICTIONARY
def dictionary():

# create an instance of the PyDictionary class
    dictionary = PyDictionary()

# get the user-specified word
    speak("specify a word to find its meaning: ")
    word = user_listen()

# get the meaning of the word
    meaning = dictionary.meaning(word)

# if the word exists in the dictionary, print its meaning
    if meaning:
        speak(f"Meaning of '{word}':")
        for part_of_speech, definitions in meaning.items():
            speak(f"{part_of_speech}:")
            for definition in definitions:
                speak(f"  - {definition}")
    else:
        speak(f"'{word}' not found in the dictionary.")

    



#Function to perform wikipedia search
def wiki_search(key):
    doc = nlp(key)
    subject = ''
    verb = ''
    for token in doc:
        if token.pos_ == 'VERB':
            verb = token.text
        elif token.dep_ == 'nsubj':
            subject = token.text

    try:
        results = wikipedia.search(subject + ' ' + verb)
        page = wikipedia.page(results[0])
        speak(page.summary)

    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"I found multiple results for {key}")
        speak("Please be more specific")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry")
        speak(f"Wikipedia doesn't seem to have any results for {key}")


def no_context(key):
    speak("Couldn't recognize command")
    speak(f"Meanwhile here are some results for {key} that i found on the web")
    webbrowser.open_new_tab(key)
    
#show file items and helps to fetch a desired one
def lst():
    string_array=[]
    directory = r"C:\Users\c4hf9"  # Replace with your directory path
    files = os.listdir(directory)
    counter=0
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            counter=counter+1
            string_array.append(str(counter)+".        \n"+file)    
    for file1 in string_array:
        print(str(counter) + ".", file1.strip(), end="\n")
        counter += 1
    speak("please select the corresponding index number of the file you want")
    num=user_listen()
    num1=int(num)
    num2=num1-1
    str1=[]  
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            str1.append(file)
    return(str1[num2])

def ls():
    language_codes = [
    "es Spanish","fr French","de German","it Italian","pt Portuguese","ru Russian","ja Japanese","zh Chinese","ko Korean","ar Arabic","hi Hindi","bn Bengali","ur Urdu","pa Punjabi","ta Tamil","te Telugu","mr Marathi","gu Gujarati","kn Kannada"]
    for index, code in enumerate(language_codes):
        print(f"{index}: {code}")
    speak("please select the corresponding index number of the language you want")
    num=user_listen()
    num1=int(num)
    #num2=num1-1
    language_codes1 = [
    "es","fr","de","it","pt","ru","ja","zh","ko","ar","hi","bn","ur","pa","ta","te","mr","gu","kn"]
    return( language_codes1[num1])

speak("System online and ready to comply")
print("------------------------------------------[+] System active [+]--------------------------------------------------------------------")

while True:
    input_query = user_listen()
    intent, confidence = process_input(input_query)
    try:
        if confidence > 0.5:
            if intent == "greeting":
                response = greet()
                speak(response)
            elif intent == "parting":
                response = say_goodbye(input_query)
                speak(response)
            elif intent == "weather":
                speak("Please specify the location whose weather you need to know")
                loc = user_listen()
                get_weather(loc)
            elif intent=="restart":
                speak("your system is restarting now...")
                restart_computer(input_query)
            elif intent=="shutdown":
                speak("your system is shutdowning now..")
                shutdown(input_query)
            elif intent=="takepicture":
                speak("ok getready,,keep similing..")
                take_picture(input_query)
            elif intent=="open file":
                s=lst()
                openfile(s)
                
                
            elif intent=="delete file": 
                d=lst()
                deletefile(d)

            elif intent=="rename file":
                a=lst()
                renamefile(a)
            elif intent=="current news":
                speak("enter the name of the place you want to know")
                place=user_listen()
                news(place)

            elif intent=="update file":
                r=lst()
                speak("What would you like to add to the file?: ")
                u=user_listen()
                updatefile(r,u)

            elif intent=="create file":
                speak("What would you like to name your file?: ")
                cr=user_listen()
                speak("what is content")
                cn=user_listen()
                createfile(cr,cn)

            elif intent=="move file":
                x=lst()
                speak("Where do you want to move the file?: ")
                wh=user_listen()
                movefile(x,wh)

            
            elif intent=="brightness":
                speak("enter the value of brightness you want to adjust")
                q=user_listen()
                set_brightness(q)
            
            elif intent=="battery charge":
                get_battery_charge()

            elif intent=="make note":
                make_note()
            elif intent=="todo list":
                speak("please specify the todolist filename that you want")
                filename=user_listen()
                filename1=filename+"txt"
                todo_list(filename1)
            elif intent=="play song":
                play_song(input_query)
            elif intent=="jokes":
                response=tell_joke(input_query)
                speak(response)
            elif intent=="reminder":
                set_reminder()

            elif intent == "run app":
                run_app(input_query)

            elif intent == "search":
                wiki_search(input_query)
            elif intent=="screenshort":
                screenshort()
            elif intent=="find location":
                speak("specify the exact place you want to locate")
                l=user_listen()
                find_location(l)
            elif intent=="translate":
                # Get the words from the user
                x=ls()
                speak("Enter the words to be translated: ")
                h=user_listen()
                from googletrans import constants
                constants.DEFAULT_SERVICE_URL = 'https://translate.google.com'
                translate(h,x)
            elif intent=="dictionary":
                dictionary()
            elif intent=="who are you":
                introduce()
            elif intent=="send mail":
                send_mail()
            
            else:
                no_context(input_query)

    except Exception as e:
        speak("Sorry")
        speak("It seems an unexpexted error has occured")
        speak("Let's try that again")