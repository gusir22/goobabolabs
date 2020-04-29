from cryptography.fernet import Fernet
import sys

def masterkey_check():
    '''Checks if this is the first time user is login in.
    If so, the masterkey_check will create the crypto key'''

    try:

        file_name = 'Key.txt'   #name Key.txt file
        with open(file_name) as txt:    #look for Key.txt file in the folder
            contents = txt.readline()   #store into contents

    except FileNotFoundError:   #if Key.txt file is not found,

        key = Fernet.generate_key() #create a new fernet key,
        decoded_key = key.decode()  #decode key byte to store in txt file,

        with open(file_name, 'w') as txt:   #create Key.txt file in the folder
            txt.write(decoded_key)  #store decoded string key in Key.txt file

    else:   #if found Key.txt file,

        with open(file_name) as txt:    #open Key.txt file,
            contents = txt.readline()   #restore decode string key from Key.txt file,

        saved_key = contents.encode()   #enconde the decoded string key for later use,
        return saved_key #return encoded byte key to a variable


def passphrase_check():
    '''Checks if a master password has been set.
    If not, passphrase_check will ask the user to set one'''

    try:

        file_name = 'Passphrase.txt'    #name Passphrase.txt file,
        with open(file_name) as txt:    #look for Passphrase.txt file in the folder,
            contents = txt.readline()   #store into contents for later use,

    except FileNotFoundError:   #if Passphrase.txt file is not found,

        message = '''   
            Welcome to Password Manager! Let's get you set up!
    
        To secure your passwords, first we need to set your secret passphrase.
    Yes, passPHRASE. In order to keep your account secure, it is strongly
    suggested that you do not use a password. If you've never seen a passphrase 
    before, you can visit https://getapassphrase.com/generate/ to create your 
    own with a random generator. NOTE! It's also recommended you create a 
    passphrase with at least 45 bit of entropy. You can select the wanted bit 
    setting using step 2 from the website. Pick one you can visualize and remember. 
    This will be the key to ALL your passwords! Commit it to memory and never EVER 
    share this passphrase!
            '''     #compose welcome message,
        print(message)  #print welcome message,

        passphrase_validation = False   #set passphrase requirements validation flag for while loop below,

        while not passphrase_validation:    #init passphrase validation loop,

            passphrase = input('\n\tSet Passphrase:\t') #ask user for passphrase,

            if len(passphrase) < 10:    #if passphrase is less than 10 chars,
                print('\n\tPassphrase must include at least 10 chars')  #print reject message, ask again(loop)
            else:   #if passphrase is more than 10 chars,
                print('\n\tPassphrase set!')    #print accept message,

                with open(file_name, 'w') as txt:  #create Passphrase.txt file in the folder,
                    txt.write(passphrase)   #store passphrase to Passphrase.txt file,
                passphrase_validation = True    #flip flag to true/break validation requirements loop

    else:   #if found Passphrase.txt file,

        login_validation = False    #create login validation flag
        login_attempts = 0  #create login attempts counter

        while not login_validation: #init passphrase match loop,

            login = input('\n\tEnter Passphrase:\t')   #ask user for passphrase,

            if login == contents:   #if the user input(login) is the same as the passphrase stored into contents,

                print('\n\tWelcome Back!')  #print welcome back message
                login_validation = True #flip flag to true/break login validation loop

            else:   #if the user input(login) is the NOT same as the passphrase stored into contents,

                attempts_left = 2 - login_attempts  #calculate attempts left
                message = '''\n\tIncorrect Passhphrase, try again...'''    #compose incorrect passphrase message
                print(message)  #print incorrect passphrase message
                login_attempts += 1 #increase login attempts by 1

                if login_attempts == 3: #if user enters incorrect passphrase wrong 3 times,

                    sys.exit('\ttoo many attempts') #exit system
                    #needs some kind of timed lock out feature

                print(f'\t{attempts_left} attempt(s) left') #print attempts left for user



#body
mkey = masterkey_check() #restore/create master crypto key
passphrase_check()  #restore/create passphrase
