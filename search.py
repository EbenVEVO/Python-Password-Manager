#Adapted from teja156/Tech Raj

from utils.aesutil import decrypt
from utils.insert import computeMK
from utils.sqlconnection import sqlconnection
import pyperclip
from rich import print as printc
from rich.console import Console
from rich.table import Table
from utils.sqlconnection import sqlconnection
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

#searches for entries based on sitename and if sitename is not given it prints full table of entires
def searchEntries(mp, ds, search, decryptPassword = False):
    db = sqlconnection()
    cursor = db.cursor()

    query= ""

    if len(search) == 0:
        query = "SELECT * FROM pm.entries"
    else:
        query = "SELECT * FROM pm.entries WHERE sitename= '"
        query += search["sitename"]
        query += "'"

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        printc("[green][-][/green] No results for search")    
        return
    
    if(decryptPassword and len(results)>1) or (not decryptPassword):
        table = Table(title="Results")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0],i[1],i[2],i[3], "{hidden}")
        console = Console()
        console.print(table)
        return
    if len(results)==1 and decryptPassword:
        mk = computeMK(mp,ds)
        decrypted = decrypt(key = mk, source = results[0][4],keyType = "bytes")
        print("Your password for " + search["sitename"] + " is " + decrypted.decode())
        pyperclip.copy(decrypted.decode())
        print("Password copied to clipboard!")
    db.commit()
    db.close()