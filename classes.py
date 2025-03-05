class Product():
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

products = []
        

class User():
    def __init__(self, name, username, password, permission):
        self.name = name
        self.username = username
        self.password = password
        self.permission = permission

users = []
loged_user = User('', '', '', '')

user1 = User('Nícolas Felipe', 'NicolasF', '111', 'administrator')
user2 = User('Juliano Emerson', 'JulianoE', '222', 'moderator')

users.append(user1)
users.append(user2)

# for user in users:
    # print('-' * 25)
    # print("Nome: " + user.name)
    # print("Usuário: " + user.username)
    # print("Senha: " + user.password)

# import sqlite3

# database = sqlite3.connect('database.db')

# cursor = database.cursor()

# name = 'abc'
# category = 'abc'
# price = 123

# cursor.execute(f'INSERT INTO products VALUES ({name}, {category}, {price})')
# database.commit()