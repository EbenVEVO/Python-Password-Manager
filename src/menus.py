import getpass
import hashlib
from utils.search import searchEntries
from utils.insert import addEntries
from utils.passwordgenerator import generate
from utils.sqlconnection import sqlconnection
import utils.insert
import utils.search

def main():
    print('-'*30)
    print(('-'*10) + 'Main  Menu'+ ('-' *10))
    print('1. Create new password')
    print('2. Create an entry')
    print('3. Find a password for a site or app')
    print('X. Exit')
    print('-'*30)
    return input(": ")

#Password validator function adapted from teja156/Tech Raj
def inputAndValidateMasterPassword():
	mp = getpass.getpass("MASTER PASSWORD: ")
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

	db = sqlconnection()
	cursor = db.cursor()
	query = "SELECT * FROM pm.secrets"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	if hashed_mp != result[0]:
		print("  WRONG PASSWORD! ")
		return None

	return [mp,result[1]]

def insert():

    res = inputAndValidateMasterPassword()
    if res is not None:
        sitename = input("Enter sitename: ")
        url = input('Please paste site url: ')
        email = input('Enter the email for this app or site: ')
        username = input('Enter the username for this app or site (if applicable): ')
        if username == None:
            username = ''
        addEntries(res[0],res[1],sitename,url,email,username)  

def findPass():
    res = inputAndValidateMasterPassword()
    if res is not None:    
        search = {}
        sitename = input("Enter sitename of password you would like to find(Enter x to print full table): ")
        if sitename != "":
            if sitename == 'x':
                search = {}
            else:       
                search["sitename"] = sitename    
        searchEntries(res[0],res[1],search,decryptPassword=False)
        if len(search) != 0:
            ans = input("Do you want to copy the password to clipboard Y/N: ")
            confim = inputAndValidateMasterPassword()
            if res is not None:
                if ans == 'Y':
                    searchEntries(confim[0], confim[1], search, decryptPassword = True)
                else:
                    return
def generatePass():
    print("Program will now assist you in generating a strong password")
    generate()
   
    
          