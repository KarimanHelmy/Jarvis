#Main gui is the main gui which will run them please run from there and maximize the window
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3  # 2.6 version  for no errors
import pytz
import comtypes.gen
import pyttsx3
import webbrowser
import smtplib
import random
import wikipedia
import datetime
import wolframalpha
import sys
import subprocess
import urllib.request
import urllib.parse
import re
import pyowm
import cv2
from googlesearch import search
from youtube_search import YoutubeSearch
import tkinter
from tkinter import *


# Create the client with app ID (request from Wolfram Alpha)
client = wolframalpha.Client('9VAJAA-5EPRPU89YE')
owm = pyowm.OWM('00f09d79c50ab45d9b40d3e44f5e6daa')

music = ["song", "music", "play song", "play music", "some music"]

forecast = ["weather forecaste", "forecast"]
jokes = ["What do you call a cow in an earthquake , . , . A milkshake",
         "What did the shark say when it ate a clown-fish . , . , this tastes funny",
         "what do you get when you put a vest on an alligator . , . , an investigator ",
         "How do you keep warm in a cold room  . , . , you go to a corner because its always 90 degrees",
         "I'm reading a book about anti-gravity. , . , I can't put it down.",
         "Time flies like an arrow. , . , Fruit flies like a banana.",
         "What do you call a nervous javelin thrower? , . , . Shakespeare."]
scope = ['https://www.googleapis.com/auth/calendar.readonly']
Months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
Days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
DayExtension = ["st", "nd", "rd", "th"]
CalenderWords = ["what do i have on....", "do i have plans", "am i busy", "plants", "events", "plans"]
Note_jarvis = ["make a note", "write this down", "remeber that"]


# make voice assisstant speak
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.say(text)
    engine.runAndWait()


# get audio from user
def get_audio():
    # This fuction uses the microphone as an input to speech and recognises it using speech recognition library
    # and it tries to recognise the speech using google recogniser and if it didn't recognise it returns the exception
    # else it returns the speech as text
    r = sr.Recognizer()
    r.energy_threshold = 1500 #Higher values mean that it will be less sensitive pypi documentary suggest values between 50 and 4000
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='en')
        print('User: ' + text + '\n')

    except sr.UnknownValueError:
        speak(" sorry I did not hear that, try typing the command")
        gui = subprocess.run(['python.exe', 'shared.py'], universal_newlines=True, stdout=subprocess.PIPE)
        text = gui.stdout
    return text


speak("initializng jarvis please wait a moment")


# greet user according to the time
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if 0 <= currentH < 12:
        speak('Good Morning!')

    if 12 <= currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH != 0:
        speak('Good Evening!')


# OPEN NOTEPAD TO WRITE IN IT
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])


# Authenticate google to begin searching events in user calender
def authenticate_google():
    """check user credintals in google and get them to log in to their google calender """
    creds = None
    if os.path.exists('token.pickle'): #if there is a pickle file open it and take creds from it
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:# dump creds in token file with creds in it
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


# function return time and date of the event
def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    # currently logged in user primary, iso format is shown format of date
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    # List of events on the calendar
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])  # get the hour the event starts
            if int(start_time.split(":")[0]) < 12:  # if the event is in the morning we don't need to convert it to 12 hours format
                start_time = start_time + "am"
            else:
                # int utc
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]  # convert 24 hour time to regular
                start_time = start_time + "pm"
            speak(event["summary"] + " at " + start_time)


def Date(text):
    text = text.lower()
    # To know where to start counting from
    today = datetime.date.today()
    tomorrow =today + datetime.timedelta(days=1)
    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    # To check if text said contains today.
    if "today" in text:
        return today
    elif "tomorrow" in text:
        return tomorrow

    for word in text.split():
        if word in Months:
            month = Months.index(word) + 1
        elif word in Days:
            day_of_week = Days.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DayExtension:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    # if month is before the month we are currently in , then the year will be next year (7amada helal reaction)
    if month < today.month and month != -1:
        year = year + 1

    # we have a day but not a month
    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

        # if we only found a date of the week which is terrible to deal with e7na mmkn n7ot lluser specify ashl :)
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        # if the day we are referring to is less than current day in index
        if dif < 0:
            dif += 7
            if "next" in text:
                dif += 7
        # represent duration
        return today + datetime.timedelta(dif)
    # avoid error of returning a negative month which could cause an error :)
    if month == -1 or day == -1:
        return None
    if day != -1:
        return datetime.date(month=month, day=day, year=year)


try:
    Service = authenticate_google()
except:
    speak("there is an authentication error please connect to the internet")
    print("google authentication is obligatory")
    speak("Jarvis embrace the power of the internet so I could not operate without it, thank you")
    speak("Good bye")
    sys.exit()
greetMe()

speak('Hello Sir, I am your voice assistant Jarvis ')
speak('How may i help you?')
print("for mathmatical operation or any equations it may be better to type as I am still learning so I may get it wrong")
print("Ready for you order")

if __name__ == '__main__':

    while True:

        text = get_audio()
        text = text.lower()
        for phrase in CalenderWords:
            if phrase in text:
                date = Date(text)
                if date:
                    get_events(date, Service)
                    speak("next command")
                    text = get_audio()
                    break
                else:
                    speak("Try again later ")
                    text = get_audio()
                    break

        # weather forecast
        for word in forecast:
            if word in text:
                reg_ex = re.search('weather forecast in (.*)', text.lower())
                if reg_ex:
                    city = reg_ex.group(1)
                    location = owm.weather_at_place(city)# if you get error in this part reinstall with this version pip install pyowm==2.10.0
                    weather = location.get_weather()

                    # temperature
                    temp = weather.get_temperature(unit='celsius')
                    # the api stores value like a dictionary
                    for key, val in temp.items():
                        print(f'{key} => {val}' + "celsius")
                        speak(f'{key} => {val}' + "celsius")
                        break

                    # humidity, wind, rain, snow
                    humidity = weather.get_humidity()
                    wind = weather.get_wind()
                    rain = weather.get_rain()

                    print(f'humidity = {humidity}')
                    speak(f'humidity = {humidity}' + "%")
                    print(f'wind = {wind}')
                    speak(f'wind = {wind}')

                    # clouds and rain
                    loc = owm.three_hours_forecast(city)

                    clouds = loc.will_have_clouds()
                    rains = loc.will_have_rain()

                    if rains == True:
                        speak("It will rain")
                    else:
                        speak("no rain")
                    if clouds == True:
                        speak("It will be cloudy")
                        speak("next command")
                        text = get_audio()
                        break
                    else:
                        speak("It will not be cloudy today")
                        speak("next command")
                        text = get_audio()
                        break

        for words in music:
            if words in text:
                speak("name of the song")
                query_string = urllib.parse.urlencode({"search_query": get_audio()})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
                try:
                    webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])
                except:
                    speak("could not find it at the moment try again later")
                speak("next command")
                text = get_audio()
                break

        else:
            if text in Note_jarvis:
                speak("what would you like me to write down sir")
                note_text = get_audio()
                note(note_text)
                speak("done sir")
            elif "take a photo" in text:
                # image is saved in same place as project : )
                capture = cv2.VideoCapture(0) # 0 or -1 indicates one camera if u want to use another camera pass 1 :D
                counter = 0
                cv2.namedWindow("test press escape to close or press enter to capture photo")
                while True:
                    ready, camera = capture.read()  # ready is just for checking so it will return none if it can't start the camera of frame for any reason
                    if not ready:  # since this was my second time using camera I wanted to know if it could capture frame or not because otherwise it would just close
                        print("failed to grab frame")
                        break
                    cv2.imshow(
                        "test press escape to close or press enter to capture photo or press g for grey filter effect : )",
                        camera)
                    key = cv2.waitKey(1)
                    if key == 13:  # key value for enter button
                        image = "PHOTO.png".format(counter)
                        #save image into project file
                        cv2.imwrite(image, camera)
                        print("{} done Sir!".format(image))
                        speak("{} done Sir!")
                        counter += 1
                    elif key == 27:  # key value for esc and to close window : )
                        capture.release()
                        cv2.destroyAllWindows()
                        break
                    elif key == 103:  # ascii(American Standard Code for Information Interchange) or key value for letter g : )
                        image = "Grey_filter.png".format(counter)
                        greyFilter = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)# open cv uses BGR not RGB
                        #save image with gray filter into project file
                        cv2.imwrite(image, greyFilter)
                        print("{} done Sir!".format(greyFilter))
                        speak("{} done Sir!")
                        counter += 1

            elif 'open youtube' in text:
                speak('okay')
                webbrowser.open('www.youtube.com')

            elif 'open google' in text:
                speak('okay')
                webbrowser.open('www.google.co.in')

            elif 'open gmail' in text:
                speak('okay')
                webbrowser.open('www.gmail.com')
            elif 'news' in text:
                webbrowser.open('https://www.bbc.com/news/world')
            elif "what\'s up" in text or 'how are you' in text:
                stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
                speak(random.choice(stMsgs))
            elif 'joke' in text:
                speak(random.choice(jokes))
            elif 'email' in text:
                speak('Who is the recipient? ')
                gui = subprocess.run(['python.exe', 'shared.py'], universal_newlines=True, stdout=subprocess.PIPE)
                recipient = gui.stdout
                speak("what is you google email address")
                gui = subprocess.run(['python.exe', 'shared.py'], universal_newlines=True, stdout=subprocess.PIPE)
                myemail = gui.stdout
                speak("what is your password")
                gui = subprocess.run(['python.exe', 'shared.py'], universal_newlines=True, stdout=subprocess.PIPE)
                password = gui.stdout
                # Allow less secure app in your google account to avoid being stuck in 4 hours of exception :)

                try:
                    speak('What should I say? ')
                    content = ('Hello, \n Hope this email finds you well ' + get_audio())

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(myemail, password)
                    server.sendmail(myemail, recipient, content)
                    server.close()
                    speak('Email sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')
                    speak("next command")
                    get_audio()
                    break

            elif 'nothing' in text or 'abort' in text or 'stop' in text:
                speak('okay')
                speak('Bye, have a nice day and stay safe.')
                sys.exit()

            elif 'hello' in text:
                speak('Hello Sir')

            elif 'bye' in text:
                speak('Bye, have a nice day and stay safe.')
                sys.exit()
            else:
                text = text
                speak('Searching...')
                try:
                    try:
                        res = client.query(text)
                        results = next(res.results).text
                        speak('Got it.')
                        speak('WOLFRAM-ALPHA says - ')
                        print(results)
                        speak(results)
                    except:
                        results = wikipedia.summary(text, sentences=2)
                        speak('Got it.')
                        speak('WIKIPEDIA says - ')
                        print(results)
                        speak(results)
                except:
                    # tld stands for domain because maybe we want to search in .com not scholar, pause is the time
                    # between each http request
                    query = text
                    for i in search(query, tld='com', lang='en', num=1, stop=1, pause=2.0):
                        print(i)
                        webbrowser.open(i)

            speak('Next Command! Sir!')
