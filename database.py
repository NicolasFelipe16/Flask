import sqlite3

database = sqlite3.connect('database.db')

cursor = database.cursor()

cursor.execute('''
               
               DELETE from users WHERE name = 'Joao Silva'
               
               ''')

database.commit()