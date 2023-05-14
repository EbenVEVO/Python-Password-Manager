import string
import random

import pyperclip

#Generates randome password bassed on user constraints and copies it to user clipboard
def generate():
    length = int(input("Enter password length: "))

    print('''To generate your password we need a character set
    Choose from these following conditions and press F when finished:
                1. Digits
                2. Characters
                3. Special Characters
                F. Finish
    ''')

    charList = ''

    while 1:
        set = input()
        if set == '1' :
            charList += string.digits
        elif set == '2':
            charList += string.ascii_letters
        elif set == '3':
            charList += string.punctuation
        elif set == 'F':
            break
        else:
            print("Enter valid condition!")
    password = ""

    if charList == '':
        print("ERROR: COULD NOT MAKE PASSWORD")
        return 
    password = randomize(length, charList)
    print("Your generated password is: " + password)
    pyperclip.copy(password)
    print("Password copied to clipboard!!!") 

def randomize(length, charList):
    password = ""
    digitCount = 0
    rerandomize = True
    for i in range (length):
        char = random.choice(charList)
        password += char
    for i in password:
        if i.isdigit():
            digitCount = digitCount + 1
    if digitCount < 2:
        password = randomize(length, charList)
    return password

