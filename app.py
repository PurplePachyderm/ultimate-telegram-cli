import telethon

import connection

class apiData:
    def __init__(self): #Your own ID and hash go here
        self.id = 123456
        self.hash = 'This is a random hash'
api = apiData()

connection.splashScreen(api)
