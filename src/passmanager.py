import getpass
import hashlib
import sys

from utils.sqlconnection import sqlconnection
from menus import insert,main
from menus import findPass, generatePass


choice = main()
while choice != 'X':
    if choice == '1':
        generatePass()
    if choice == '2':
        insert()
    if choice == '3':
        findPass()
        choice = main()
    else:
        choice = main()
sys.exit(0)