from peewee import *

class ConnectDatabase:

    def get_connect_string():
        try:
            with open("connect.txt", "r") as db_name:
                return db_name.readline().strip()
        except:
            print("You need a database and store its name in a file named 'connect.txt'")

    db = PostgresqlDatabase(get_connect_string())