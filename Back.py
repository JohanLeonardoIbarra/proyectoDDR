from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = 'Johan'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'empresa'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = '3306'

mysql.init_app(app)

app.secret_key = "mysecretkey"

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

@app.route('/Add_Producto')
def Add_Producto():
    cur = mysql.connection.cursor()
    cur.execute('Select * from categoria')
    data = cur.fetchall()
    return render_template('registro.html', categorias = data)

@app.route('/Subir_Producto', methods=['POST'])
def Subir_Producto():
    if request.method == 'POST':
        nombre = request.form['name']
        referencia = request.form['referencia']
        descripcion = request.form['descripcion']
        detalle = request.form['detalle']
        valor = request.form['valor']
        categ = request.form['categ']
        imagen = request.files['imagen']
        cur = mysql.connection.cursor()
        cur.execute('insert into producto (id, referencia, nombre, descripcioncorta, detalle, valor, imagen, categoria_id) Values (null,%s,%s,%s,%s,%s,%s,%s)',(referencia, nombre, descripcion, detalle, valor, imagen, categ))
        mysql.connection.commit()
        flash('PRODUCTO CREADO SATISFACTORIAMENTE')
        return render_template('index.html')


if __name__ == '__main__':
    app.run(port = 3000, debug = True)