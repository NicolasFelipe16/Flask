from flask import render_template, request, redirect, session, flash, url_for, g
from main import app
import psycopg2

# import sqlite3

# database = sqlite3.connect('database.db')

# cursor = database.cursor()

# database.close()

# Função para obter a conexão com o banco de dados
# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect('database.db')
#         g.db.row_factory = sqlite3.Row  # Isso ajuda a manipular os dados como dicionários
#     return g.db

# # Fechar a conexão após a requisição
# @app.teardown_appcontext
# def close_db(error):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()





render_hostname = 'dpg-cvf1985ds78s73ffs7j0-a.oregon-postgres.render.com'
render_port = 5432
render_database = 'meu_banco_t32u'
render_username = 'meu_banco_t32u_user'
render_password = 'gxacHJu3kKndEv6mTJmCoA7DcToa2iac'

database = psycopg2.connect(
    host=render_hostname,
    port=render_port,
    database=render_database,
    user=render_username,
    password=render_password)

cursor = database.cursor()

# Função para obter a conexão com o banco de dados PostgreSQL
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host='dpg-cvf1985ds78s73ffs7j0-a.oregon-postgres.render.com',  # Endereço do servidor PostgreSQL
            port=5432,  # Porta padrão do PostgreSQL
            database='meu_banco_t32u',  # Nome do banco de dados
            user='meu_banco_t32u_user',  # Usuário do banco de dados
            password='gxacHJu3kKndEv6mTJmCoA7DcToa2iac'  # Senha do banco de dados
        )
    return g.db

# Fechar a conexão após a requisição
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, 'db', None)  # Obtém a conexão armazenada no contexto da requisição
    if db is not None:  # Se houver uma conexão aberta, fecha ela
        db.close()



@app.before_request
def create_tables():
    db = get_db()
    cursor = db.cursor()

    # Criação da tabela 'users' se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,  -- Adicionando um id autoincremento
        name VARCHAR(100) NOT NULL,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(20) NOT NULL,
        permission VARCHAR(20)
    );
    ''')
    db.commit()

    # Criação da tabela 'products' se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,  -- Adicionando um id autoincremento
        name VARCHAR(255),
        category VARCHAR(255),
        price INTEGER
    );
    ''')
    db.commit()


@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                    name varchar(100) not null,
                    username varchar(30) not null,
                    password varchar(20) not null,
                    permission varchar(20)
                   );
                   ''')
    
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/createuser', methods=['POST'])
def createuser():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    permission = 'user'

    db = get_db()
    cursor = db.cursor()

    cursor.execute('INSERT INTO users (name, username, password, permission) VALUES (%s, %s, %s, %s)', (name, username, password, permission))
    db.commit()

    # session['username'] = user['name']
    # flash('Olá, ' + session['username'] + '!')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('index'))

    user_firstletter = session['username']

    return render_template('dashboard.html', user_firstletter=user_firstletter)

@app.route('/newproduct')
def newproduct():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products (
                    name VARCHAR(255),
                    category VARCHAR(255),
                    price INTEGER
                   );
                   ''')


    user_firstletter = session['username']

    return render_template('newproduct.html', user_firstletter=user_firstletter)

@app.route('/signout')
def signout():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))

    session['username'] = None
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('dashboard'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT name, username, password, permission FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user:
        # if password == user['password']:
        if password == user[2]:
            # session['username'] = user['name']
            session['username'] = user[0]
            flash('Olá, ' + session['username'] + '!')
            return redirect(url_for('dashboard'))
        else:
            flash('Senha incorreta. Tente novamente...')
            return redirect(url_for('signin'))
    else:
        flash('Esse usuário não existe. Tente novamente ou crie uma conta...')
        return redirect(url_for('signin'))


@app.route('/createproduct', methods=['POST'])
def createproduct():
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']

    db = get_db()
    cursor = db.cursor()

    cursor.execute('INSERT INTO products (name, category, price) VALUES (%s, %s, %s)', (name, category, price))
    db.commit()

    return redirect(url_for('products_list'))

@app.route('/products')
def products_list():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, category, price FROM products')
    products = cursor.fetchall()

    # print(products)

    # for p in products:
    #     print(p[0])
    #     print(p[1])
    #     print(p[2])


    user_firstletter = session['username']

    return render_template('products.html', products=products, user_firstletter=user_firstletter)

@app.route('/users')
def users_list():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT name, username, password, permission FROM users WHERE name = %s', (session['username'],))
    loged_user = cursor.fetchone()

    cursor.execute('SELECT name, username, password, permission FROM users')
    users = cursor.fetchall()

    user_firstletter = session['username']

    # if loged_user['permission'] == 'administrator':
    if loged_user[3] == 'administrator':
        user_firstletter = session['username']
        return render_template('users.html', users=users, user_firstletter=user_firstletter)  
    
    else:
        flash('Você não tem acesso à esta página')
        return redirect(url_for('dashboard'))
 
    # return render_template('users.html', users=users, user_firstletter=user_firstletter)


@app.route('/account')
def account():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, username, password, permission FROM users WHERE name = %s', (session['username'],))
    user = cursor.fetchone()

    user_firstletter = session['username']

    return render_template('account.html', user_firstletter=user_firstletter, user=user)  