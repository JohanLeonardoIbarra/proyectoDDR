from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = 'Johan'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'empresa'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = '3306'

mysql.init_app(app)


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/admin')
def index():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('Select * from admin')
        data = cur.fetchall()
        nombre = request.form['userAdmin']
        password = request.form['passAdmin']
        for dato in data:
            if nombre == dato[0] :
                if password == dato[1] :
                    return render_template('registro.html')
        return render_template('admin.html')
    

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['name']

if __name__ == '__main__':
    app.run(port = 3000, debug = True)