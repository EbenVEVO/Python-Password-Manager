import mysql.connector 
from rich.console import Console
console = Console()



def sqlconnection():
  #connects to mysql server
  try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="0725"
    )

  except Exception as e:
    console.print_exception(show_locals=True)

  return mydb