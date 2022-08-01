import os

import menus

def main():
    # Menu constants
    
    GET_REQUEST = '1'
    OPTIONS = '2'
    EXIT_PROGRAM = '3'

    while True:
        os.system('cls')
        
        print('Select the desired point (enter index (number))\n')
        print(GET_REQUEST, '- Get request from dadata.ru')
        print(OPTIONS, '- Options')
        print(EXIT_PROGRAM, '- Exit')
        valueMenu = input()

        os.system('cls')

        try:
            if valueMenu == GET_REQUEST:
                menus.Menu.try_get_request()
                
            elif valueMenu == OPTIONS:
                menus.Menu.options()
            
            elif valueMenu == EXIT_PROGRAM:
                break
            
            else:
                print('Wrong number.')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()