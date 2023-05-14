#Adapted from teja156/Tech Raj

import string
import sys
import getpass
import hashlib
import random

from utils.sqlconnection import sqlconnection
from rich.console import Console
from rich import print as printc
console = Console()

def createDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def launch():
    #Creates database
    db = sqlconnection()
    cursor = db.cursor()


    printc("[green][+] Creating config [/green]")
    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] Error making db")
        console.print_exception(show_locals=True)   
        sys.exit(0)
    printc("[green][+][/green] Database pm created")    


    #Creating tables
    #Table that holds hash of the masterkey and device secret
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+] Table secrets created [/green]")

    #Table of user password data
    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, url TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+] Table entries created [/green]")

    #recieves master passwrd
    while 1:
        mp = getpass.getpass("Enter MASTER PASSWORD: ")
        if mp == getpass.getpass("Re-Enter Password: ") and mp!='':
            break
        printc(("[green][-] try another password [/green]"))

    #Hashing our master password
    hash_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+] Master password encrypted [/green]")

    #Generate Device Secret and add to our database
    ds = createDeviceSecret()
    printc("[green][+] Device secret created [/green]")
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s, %s)"
    val = (hash_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+] Added to database [/green]")
    db.close()
launch()