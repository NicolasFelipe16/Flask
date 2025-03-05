from flask import render_template, request, redirect, session, flash, url_for, g
from main import app
# from classes import loged_user
import sqlite3

database = sqlite3.connect('database.db')

cursor = database.cursor()

database.close()

# Função para obter a conexão com o banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row  # Isso ajuda a manipular os dados como dicionários
    return g.db

# Fechar a conexão após a requisição
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
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

    cursor.execute('INSERT INTO users (name, username, password, permission) VALUES (?, ?, ?, ?)', (name, username, password, permission))
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
                   name TEXT,
                   category TEXT,
                   price INTEGER
               )
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

    cursor.execute('SELECT name, username, password, permission FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        if password == user['password']:
            session['username'] = user['name']
            flash('Olá, ' + session['username'] + '!')
            return redirect(url_for('dashboard'))
        else:
            flash('Senha incorreta. Tente novamente...')
    else:
        flash('Não foi possível logar esse usuário. Tente novamente...')
        return redirect(url_for('signin'))


@app.route('/createproduct', methods=['POST'])
def createproduct():
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']

    db = get_db()
    cursor = db.cursor()

    cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', (name, category, price))
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

    user_firstletter = session['username']

    return render_template('products.html', products=products, user_firstletter=user_firstletter)

@app.route('/users')
def users_list():
    if 'username' not in session or session['username'] == None:
        return redirect(url_for('dashboard'))
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT name, username, password, permission FROM users WHERE name = ?', (session['username'],))
    loged_user = cursor.fetchone()

    cursor.execute('SELECT name, username, password, permission FROM users')
    users = cursor.fetchall()

    user_firstletter = session['username']

    if loged_user['permission'] == 'administrator':
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
    cursor.execute('SELECT name, username, password, permission FROM users WHERE name = ?', (session['username'],))
    user = cursor.fetchone()

    user_firstletter = session['username']

    return render_template('account.html', user_firstletter=user_firstletter, user=user)  