import os
import glob
import json
from termcolor import *
from telethon import *
import getch

import logo
import chat

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



def listDisplay(usersList):
  text = colored("Here's the list of all registered users:\n", 'green', attrs=['underline'])
  print(text)
  for i in range (0, len(usersList)):
      print(i+1, ")", usersList[i][2:len(usersList[i])-8])    #Extracts username from the .session file
  print("")



def splashScreen(api): #Main menu
    while True:
        cls()
        usersList = glob.glob("./*.session") #Selects all session files
        if len(usersList) == 0: #No users found
            createUser(api)
            usersList = glob.glob("./*.session") #Refresh the list

        logo.display()
        listDisplay(usersList)
        text = colored("C: Connect to an existing profile    N: New profile    D: Delete a profile", 'blue', attrs=['underline'])
        print(text)
        text = colored("Q: Quit\n", 'yellow', attrs=['underline'])
        print(text)

        key = getch.getch().lower()
        if key == 'c':
             #TODO Enter chat and stuff
             login(api, usersList)
        elif key == 'n':
            createUser(api)
            usersList = glob.glob("./*.session") #Refresh the list
        elif key == 'd':
            removeUser(usersList)
        elif key == 'q':
            break


            ###Sign in###
def login(api, usersList):
    quit = False
    login = False

    while True:
        cls()
        logo.display()
        listDisplay(usersList)

        userId = input("\n Choose an account (enter number) or enter Q to quit:")
        try:    #Verifies input validity
            intId = int(userId)
            if intId>0 and intId<=len(usersList):
                login = True
                break
        except ValueError:
            userId = userId.lower()
            if userId == 'q':
                break

    if login:
        username = usersList[intId-1][2:len(usersList[intId-1])-8]
        client = TelegramClient(username, api.id, api.hash)
        client.connect()

        if not client.is_user_authorized():
            with open("phones.json", 'r') as f:
                phones = json.load(f)
                phone = phones[username]

            cls()
            print("One moment please :-)...")
            client.send_code_request(phone)
            cls()
            client.sign_in(phone, input("Enter the code Telegram just sent you: "))

        chat.chatSelection(client)


        ###Sign up###
def createUser(api):
    connected = False
    firstTry = True
    correctPhone = False

    while not connected and not correctPhone:
        correctPhone = False

        cls()
        signupMessage(firstTry)
        phone = input("Enter your phone number (international format):")
        cls()
        signupMessage(firstTry)
        username = input("Enter your username:")

        if phone[0] == '+' and len(phone) == 12:
            correctPhone = True
            client = TelegramClient(username, api.id, api.hash)
            if client.connect():
                connected = True
        else:
             firstTry = False

    newPhone = {username: phone}    #Saving phone number for authentification
    with open('phones.json', 'r') as outfile:
        phones = json.load(outfile)
    phones[username] = phone
    with open('phones.json', 'w') as outfile:
        json.dump(phones, outfile)



def signupMessage(bool):
    logo.display()
    if bool:
          text = colored("It seems you're not logged in yet...\n", 'green', attrs=[])
          print(text)
    else:
          text = colored("Oops! Something went wrong =\\! Let's try again...\n", 'yellow', attrs=[])
          print(text)


            ###Remove user###
def removeUser(usersList):
    while True:
        cls()
        logo.display()
        listDisplay(usersList)
        text = colored("Enter the number of the user you want to delete or enter Q to quit:", "red", attrs=['underline'])

        key = input(text).lower()
        try:    #User has entered a number
            intId = int(key)

            if intId>0 and intId<=len(usersList):   #Remove entry from JSON
                username = usersList[intId-1][2:len(usersList[intId-1])-8]
                with open('phones.json', 'r') as f:
                    phones = json.load(f)

                phones.pop(username)
                with open('phones.json', 'w') as outfile:
                    phones = json.dump(phones, outfile)

                os.remove(username+".session")
                break

        except:
            if key == 'q':
                break
