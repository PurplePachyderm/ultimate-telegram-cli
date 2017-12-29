import os
import glob
import json
from termcolor import *
from telethon import *
import getch

import logo

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



def listDisplay(usersList):
  cls()
  logo.display()
  text = colored("Here's the list of all registered users:\n", 'green', attrs=['underline'])
  print(text)
  for i in range (0, len(usersList)):
      print(i+1, ")", usersList[i][2:len(usersList[i])-8])    #Extracts username from the .session file
  print("")



def splashScreen(api): #Main menu
    while True:
        usersList = glob.glob("./*.session") #Selects all session files
        if len(usersList) == 0: #No users found
            createUser(api)
            usersList = glob.glob("./*.session") #Refresh the list

        listDisplay(usersList)
        cprint("C: Connect to an existing profile    N: New profile    D: Delete a profile    ", "white", "on_green")
        cprint("Q: Quit", "white", "on_yellow")

        key = getch.getch().lower()
        if key == 'c':
             #TODO Enter chat and stuff
             continue
        elif key == 'n':
            createUser(api)
            usersList = glob.glob("./*.session") #Refresh the list
        elif key == 'd':
            removeUser(usersList)
        elif key == 'q':
            break


            ###Sign in###
def login(api, usersList):  #TODO Menu with option to quit, otherwise redirects to chats
    quit = False
    login = False

    while not quit:
        listDisplay(usersList)

        userId = input("\n Choose an account (enter number):")
        try:    #Verifies input validity
            intId = int(userId)
            if intId>0 and intId<=len(usersList):
                quit = True
                login = True
        except ValueError:
            continue

    username = usersList[intId-1][2:len(usersList[intId-1])-8]
    client = TelegramClient(username, api.id, api.hash)

    if not client.is_user_authorized():
        with open("phones.json", 'r') as f:
            phones = json.load(f)
            phone = phones[username]
            cls()
        myself = client.sign_in(phone, input("Enter the code Telegram just sent you: "))


        ###Sign up###
def createUser(api):
    connected = False
    firstTry = True
    correctPhone = False

    while not connected and not correctPhone:
        correctPhone = False

        signupMessage(firstTry)
        phone = input("Enter your phone number (international format):")

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
    cls()
    logo.display()
    if bool:
          text = colored("It seems you're not logged in yet...\n", 'green', attrs=[])
          print(text)
    else:
          text = colored("Oops! Something went wrong =\\! Let's try again...\n", 'yellow', attrs=[])
          print(text)


            ###Remove user###
def removeUser(usersList):
    quit = False
    while not quit:
        cls()
        logo.display()
        listDisplay(usersList)
        cprint("Enter the number of the user you want to delete.    Q: Quit", "white", "on_red")
        key = getch.getch().lower()
        try:    #User has entered a number
            intId = int(key)
            username = usersList[intId-1][2:len(usersList[intId-1])-8]

            if intId>0 and intId<=len(usersList):   #Remove entry from JSON
                with open('phones.json', 'r') as f:
                    phones = json.load(f)

                phones.pop(username)
                with open('phones.json', 'w') as outfile:
                    phones = json.dump(phones, outfile)

                os.remove(username+".session")
                quit = True

        except ValueError as e:
            print("Trying to quit...")
            print(e)
            getch.getch()
            if key == 'q':
                quit = True
