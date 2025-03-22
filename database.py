# import psycopg2
# from urllib.parse import urlparse

# # Substitua com a URL fornecida pelo Render
# database_url = "postgresql://meu_banco_t32u_user:gxacHJu3kKndEv6mTJmCoA7DcToa2iac@dpg-cvf1985ds78s73ffs7j0-a.oregon-postgres.render.com/meu_banco_t32u"

# # Parse a URL para obter os componentes
# url = urlparse(database_url)

# # Conectando ao banco de dados usando os parâmetros extraídos da URL
# post_database = psycopg2.connect(
#     host=url.hostname,
#     port=url.port,
#     database=url.path[1:],  # O nome do banco de dados é após a primeira barra
#     user=url.username,
#     password=url.password
# )

# post_cursor = post_database.cursor()

# # Criando a tabela e inserindo dados
# post_cursor.execute('''
#                     CREATE TABLE users (
#                     name varchar(100) not null,
#                     username varchar(30) not null,
#                     password varchar(20) not null,
#                     permission varchar(20)
#                     );''')

# post_cursor.execute('''INSERT INTO users (name, username, password, permission) VALUES('Nícolas Felipe', 'Nick', '123', 'administrator')''')

# # Consultando os dados inseridos
# post_cursor.execute('''SELECT * FROM users''')
# a = post_cursor.fetchall()
# for i in a:
#     print(i)

# post_cursor.close()
# post_database.close()



import psycopg2

render_hostname = 'dpg-cvf1985ds78s73ffs7j0-a.oregon-postgres.render.com'
render_port = 5432
render_database = 'meu_banco_t32u'
render_username = 'meu_banco_t32u_user'
render_password = 'gxacHJu3kKndEv6mTJmCoA7DcToa2iac'


post_database = psycopg2.connect(
    host=render_hostname,
    port=render_port,
    database=render_database,
    user=render_username,
    password=render_password)

post_cursor = post_database.cursor()

post_cursor.execute('''
                    CREATE TABLE users (
                    name varchar(100) not null,
                    username varchar(30) not null,
                    password varchar(20) not null,
                    permission varchar(20)
                    );''')

post_cursor.execute('''INSERT INTO users (name, username, password, permission) VALUES('Nícolas Felipe', 'Nick', '123', 'administrator')''')

post_cursor.execute('''SELECT * FROM users''')
a = post_cursor.fetchall()
for i in a:
    print(i)

post_cursor.close()
post_database.close()




# import sqlite3

# database = sqlite3.connect('database.db')

# cursor = database.cursor()

# cursor.execute('''
               
#                DELETE from users WHERE name = 'Joao Silva'
               
#                ''')

# database.commit()