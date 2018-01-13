from termcolor import *
from telethon import *
from telethon.utils import get_display_name
import getch
import logo

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


    #List of conversations
def chatSelection(client):
    cls()
    dialogs, entities = client.get_dialogs(500)
    nPages = (len(entities) - len(entities)%10) / 10 + 1
    currentPage = 0

    while True:
        cls()
        logo.display()
        text = colored("Here is the list of your current conversations:", 'green', attrs=['underline'])
        print(text)

        minRange = currentPage * 10
        maxRange = currentPage * 10 + 10
        if maxRange > len(entities):
            maxRange = len(entities)

        for i in range (minRange, maxRange):
            print(i+1, ")", get_display_name(entities[i]))

        text = colored("Page"+str(currentPage+1)+"/"+str(int(nPages))+"\n", 'green', attrs=['underline'])
        print(text)


        text = colored("Use + and - to navigate between pages", 'blue', attrs=['underline'])
        print(text)
        text = colored("J: Join a conversation", 'blue', attrs=['underline'])
        print(text)
        text = colored("Q: Quit\n", 'yellow', attrs=['underline'])
        print(text)

        key=getch.getch().lower()
        if key == '+' and currentPage < nPages-1:
            currentPage+=1
        if key == '-' and currentPage > 0:
            currentPage-=1
        if key == 'j':
            #TODO chat function
            continue
        elif key == 'q':
            break
