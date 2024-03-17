from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)

# Database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
__mysql = MySQL(app)

# Route
@app.route('/')
def dashboard():
    cur = __mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', users=data)

@app.route('/user/create')
def create():
    return render_template('create.html')

@app.route('/user', methods=['POST'])
def store():
    # catch data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cur = __mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    __mysql.connection.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/user/edit/<id>')
def edit(id):
    cur = __mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id))
    data = cur.fetchall()
    cur.close()

    return render_template('edit.html', user=data[0])

@app.route('/user/edit', methods=['POST'])
def update():
    # catch data
    username = request.form['username']
    email = request.form['email']
    user_id = request.form['id']

    cur = __mysql.connection.cursor()
    cur.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (username, email, user_id))
    __mysql.connection.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/user/delete/<id>', methods=['POST'])
def destroy(id):
    cur = __mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id))
    __mysql.connection.commit()

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug = True)