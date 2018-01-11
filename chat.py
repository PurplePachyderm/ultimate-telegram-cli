from termcolor import *
from telethon import *
from telethon.utils import get_display_name
import getch
import logo


def chatSelection(client):

    dialogs, entities = client.get_dialogs(500)

    logo.display()
    text = colored("Here is the list of your current conversations:", 'green', attrs=['underline'])
    print(text)

    for i in range (0, len(entities)):
        print(i+1, ")", get_display_name(entities[i]))

    quit = False
    while not quit:
        getch.getch()
