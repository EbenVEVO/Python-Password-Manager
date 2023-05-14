#Adapted from teja156/Tech Raj


import getpass

from utils.sqlconnection import sqlconnection
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import utils.aesutil

#Encodes our master password for safety
def computeMK(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count = 1000000, hmac_hash_module = SHA512)
    return key

#adds user given entries to SQL table
def addEntries(mp, ds, sitename, url, email, username):

    password = getpass.getpass("Password: ")
    mk = computeMK(mp, ds)

    #encrypts entries password for saftey
    encrypted = utils.aesutil.encrypt(key = mk, source = password, keyType='bytes')

    db = sqlconnection()
    cursor = db.cursor()
    query = "INSERT INTO pm.entries (sitename, url, email, username, password) values (%s,%s,%s,%s,%s)"
    val = (sitename, url, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()

    print("ENTRY ADDED TO TABLE")