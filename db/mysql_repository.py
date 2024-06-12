import mysql.connector


class MysqlRepository:

    def __init__(self):
        config = {
            'user': 'root',
            'password': 'sakila',
            'host': 'localhost',  # When you run this on your machine change it to 'localhost'
            'port': '32000',  # When you run this on your machine change it to '32000'
            'database': 'sakila'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def getPuzzle(self, date):
        thisPuzzle = new PuzzleObject

    def __del__(self):
        self.connection.close()
