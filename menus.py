from dadata import Dadata
import os

import DBwork

def VerifyOptions(token, secretToken, language):
    if token != '' and secretToken != '' and language != '':
        return True
    
    return False

def print_press_to_continue():
    print('\nPress any button to continue')
    wait = input()
    
def print_latitude_longitude(list_dict):
    print('Latitude: ' + list_dict[0]['data']['geo_lat'] + '\nLongitude: ' + list_dict[0]['data']['geo_lon'])

def print_menu_points(dict):
    for key in dict:
        print(key, '-', dict[key])
        
def enter_index_list(lenList):
    addressNumber = None
    
    while True:
        try:
            addressNumber = int(input())
            
            if addressNumber < 0 or addressNumber > (lenList - 1):
                raise IndexError
            
            break
        except ValueError:
            print('That was no valid number. Try again')
        except IndexError:
            print('Index out of range. Try again')
            
    return addressNumber

class Menu:
    # constants variables for menu options
    
    ENTER_TOKEN = '1'
    ENTER_SECRET_TOKEN = '2'
    SELECT_LANGUAGE = '3'
    SAVE_OPTIONS = '4'
    EXIT_OPTIONS = '5'
    
    INDEX_ENGLISH_LANGUAGE = '1'
    INDEX_RUSSIAN_LANGUAGE = '2'
    
    @staticmethod
    def try_get_request():
        token, secretToken, userLanguage = DBwork.DB.TryGetOptionsFromDataBase()
        
        if VerifyOptions(token, secretToken, userLanguage) == True:
            Menu.get_request(token, secretToken, userLanguage)
        else:
            print('Error. You need to enter all the options')
            print_press_to_continue()
    
    @staticmethod
    def get_request(token, secretToken, userLanguage):
        print('Enter the desired street: ', end='')
        userRequest = input()

#         with Dadata(token, secretToken) as dadata:

        try:
            dadata = Dadata(token, secretToken)
            
            data = dadata.suggest(name='address', query=userRequest, language=userLanguage)

            for i in range(0, len(data)):
                print(str(i) + ' - ' + data[i]['value'])

            print('\nSelect the desired street (enter index): ', end='')
            addressNumber = enter_index_list(len(data))
                    
            result = dadata.suggest(name='address', query=data[addressNumber]['value'], count=1, language=userLanguage)
            
            print_latitude_longitude(result)
            print_press_to_continue()
            
        except Exception as e:
            print(e)
            print('Verify your options "token" and "secret token"')
            print_press_to_continue()
            
    @staticmethod
    def try_save_options(token, secretToken, userLanguage):        
        if VerifyOptions(token, secretToken, userLanguage) == True:
            DBwork.DB.SaveOptionsDataBase(token, secretToken, userLanguage)
        else:
            print('Error. You need to enter all the options')
            print_press_to_continue()
            
    @staticmethod
    def options():
        token, secretToken, userLanguage = DBwork.DB.TryGetOptionsFromDataBase()
    
        while True:
            os.system('cls')

            print('\tOptions:')
            print('Token:', token)
            print('Secret token:', secretToken)
            print('Language:', userLanguage)
            print("\n")

            print(Menu.ENTER_TOKEN, '- Enter token')
            print(Menu.ENTER_SECRET_TOKEN, '- Enter secret token') 
            print(Menu.SELECT_LANGUAGE, '- Select language')
            print(Menu.SAVE_OPTIONS, '- Save options to dataBase')
            print(Menu.EXIT_OPTIONS, '- Exit to menu')
            optionMenu = input()

            if optionMenu == Menu.ENTER_TOKEN:
                token = input()

            elif optionMenu == Menu.ENTER_SECRET_TOKEN:
                secretToken = input()

            elif optionMenu == Menu.SELECT_LANGUAGE:
                userLanguage = Menu.enter_language()

                os.system('cls')
            
            elif optionMenu == Menu.SAVE_OPTIONS:
                Menu.try_save_options(token, secretToken, userLanguage)

            elif optionMenu == Menu.EXIT_OPTIONS:
                break
            
            else:
                print('Wrong number.')
                print_press_to_continue()
                
    @staticmethod
    def enter_language():
        while True:
            print(Menu.INDEX_ENGLISH_LANGUAGE, '- English')
            print(Menu.INDEX_RUSSIAN_LANGUAGE, '- Russian')
            languageMenu = input()

            if languageMenu == Menu.INDEX_ENGLISH_LANGUAGE:
                return 'en'

            elif languageMenu == Menu.INDEX_RUSSIAN_LANGUAGE:
                return 'ru'
            
            else:
                print('Wrong number.')
                print_press_to_continue()