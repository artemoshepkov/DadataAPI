from dadata import Dadata
import sqlite3 as sq
import os

# Options parameters
token = None
secretToken = None
userLanguage = None

paramDadata = 'address'

titleTable = 'options'

# Menu constants

GET_REQUEST = 1
OPTIONS = 2
EXIT_PROGRAM = 3

ENTER_TOKEN = 1
ENTER_SECRET_TOKEN = 2
SELECT_LANGUAGE = 3
SAVE_OPTIONS = 4
EXIT_OPTIONS = 5

INDEX_ENGLISH_LANGUAGE = 1
INDEX_RUSSIAN_LANGUAGE = 2

def VerifyOptions():
    if token != None and secretToken != None:
        return True
    else:
        return False

def TryGetOptionsFromDataBase():
    global token
    global secretToken 
    global userLanguage

    with sq.connect('OptionsAPI.db') as con:
        cur = con.cursor()

        cur.execute(f"""CREATE TABLE IF NOT EXISTS  {titleTable} (
                        token text, 
                        secretToken text, 
                        language text);
        """)

        cur.execute(f"""SELECT * FROM {titleTable};
        """)
        prevRecord = cur.fetchone()

        if prevRecord != None:
            token = prevRecord[0]
            secretToken = prevRecord[1]
            userLanguage = prevRecord[2]    

def SaveOptionsDataBase(token, secretToken, language):
    with sq.connect('OptionsAPI.db') as con:
        cur = con.cursor()

        cur.execute(f"""CREATE TABLE IF NOT EXISTS  {titleTable} (
                        token text, 
                        secretToken text, 
                        language text);
        """)

        cur.execute(f"""DELETE FROM {titleTable};
        """)

        cur.execute(f"""INSERT INTO {titleTable} (token, secretToken, language) VALUES (?, ?, ?);
            """, (token, secretToken, language))

        con.commit()


TryGetOptionsFromDataBase()

while True:
    print('Select the desired point (enter index (number))')
    print(GET_REQUEST, '- Get request from dadata.ru')
    print(OPTIONS, '- Options')
    print(EXIT_PROGRAM, '- Exit')
    valueMenu = int(input())

    os.system('cls')

    if valueMenu == GET_REQUEST:
        if VerifyOptions() == True:
            print('Enter the desired street: ', end='')
            userRequest = input()
            print('\n')

            with Dadata(token, secretToken) as dadata:
                data = dadata.suggest(name=paramDadata, query=userRequest, language=userLanguage)

                for i in range(0, len(data)):
                    print(str(i) + ' - ' + data[i]['value'])

                print('\nSelect the desired street (enter index): ', end='')
                addressNumber = int(input())

                result = dadata.suggest(name=paramDadata, query=data[addressNumber]['value'], count=1, language=userLanguage)
                
                print('Latitude: ' + result[0]['data']['geo_lat'] + '\nLongitude: ' + result[0]['data']['geo_lon'])

                print('Press any button to continue')
                wait = input()
        else:
            print('Error. You need to enter all the options')
            print('Press any button to continue')
            wait = input()
            
        
    elif valueMenu == OPTIONS:
        while True:
            os.system('cls')

            print('Options:')
            print('Token:', token)
            print('Secret token:', secretToken)
            print('Language:', userLanguage)
            print('\n')

            print(ENTER_TOKEN, '- Enter token')
            print(ENTER_SECRET_TOKEN, '- Enter secret token') 
            print(SELECT_LANGUAGE, '- Select language')
            print(SAVE_OPTIONS, '- Save options to dataBase')
            print(EXIT_OPTIONS, '- Exit to menu')
            optionMenu = int(input())

            if optionMenu == ENTER_TOKEN:
                token = input()

            elif optionMenu == ENTER_SECRET_TOKEN:
                secretToken = input()

            elif optionMenu == SELECT_LANGUAGE:
                while True:
                    print(INDEX_ENGLISH_LANGUAGE, '- English')
                    print(INDEX_RUSSIAN_LANGUAGE, '- Russian')
                    languageMenu = int(input())

                    if languageMenu == INDEX_ENGLISH_LANGUAGE:
                        userLanguage = 'en'
                        break

                    elif languageMenu == INDEX_RUSSIAN_LANGUAGE:
                        userLanguage = 'ru'
                        break

                os.system('cls')
            
            elif optionMenu == SAVE_OPTIONS:
                if VerifyOptions() == True:
                    SaveOptionsDataBase(token, secretToken, userLanguage)
                
                else:
                    print('Error. You need to enter all the options')
                    print('Press any button to continue')
                    wait = input()

            elif optionMenu == EXIT_OPTIONS:
                break

    
    elif valueMenu == EXIT_PROGRAM:
        break
        
    os.system('cls')

wait = input()