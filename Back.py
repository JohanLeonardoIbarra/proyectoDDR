from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from werkzeug import secure_filename
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = 'Johan'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'empresa'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = '3306'
app.config['UPLOAD_FOLDER'] = './static/Productos'

mysql.init_app(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('select * from producto LIMIT 9')
    data = cur.fetchall()
    mysql.connection.commit()
    return render_template('index.html', productos = data)

@app.route('/Catalogo')
def catalogo():
    cur = mysql.connection.cursor()
    cur.execute('Select * from producto')
    cur2 = mysql.connection.cursor()
    cur2.execute('Select * from categoria')
    data = cur.fetchall()
    cat = cur2.fetchall()
    mysql.connection.commit()
    return render_template('Catalogo.html', productos = data, categorias = cat)

@app.route('/Catalogo/<string:id>')
def catalogoconid(id):
    cur = mysql.connection.cursor()
    cur.execute('Select * from producto where categoria_id = '+id)
    cur2 = mysql.connection.cursor()
    cur2.execute('Select * from categoria')
    data = cur.fetchall()
    cat = cur2.fetchall()
    mysql.connection.commit()
    return render_template('Catalogo.html', productos = data, categorias = cat)

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
                    return Administrador()
        return render_template('admin.html')

@app.route('/Administrador')
def Administrador():
    cur = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur.execute('Select * from categoria')
    cur2.execute('Select * from producto')
    data = cur.fetchall()
    prod = cur2.fetchall()
    mysql.connection.commit()
    return render_template('registro.html', categorias = data, productos = prod)

@app.route('/Eliminar/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('Delete From producto Where id = {0}'.format(id))
    mysql.connection.commit()
    return Administrador()


@app.route('/RegistrarProducto_Subida', methods=['POST'])
def RegistrarProducto_Subida():
    if request.method == 'POST':
        nombre = request.form['name']
        referencia = request.form['referencia']
        descripcion = request.form['descripcion']
        detalle = request.form['detalle']
        valor = request.form['valor']
        categ = request.form['categ']
        imagen = request.files['imagen']
        imagenname = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagenname))
        cur = mysql.connection.cursor()
        cur.execute('insert into producto (id, referencia, nombre, descripcioncorta, detalle, valor, imagen, categoria_id) Values (null,%s,%s,%s,%s,%s,%s,%s)',(referencia, nombre, descripcion, detalle, valor, imagenname, categ))
        mysql.connection.commit()
        flash('PRODUCTO CREADO SATISFACTORIAMENTE')
        return Administrador()


if __name__ == '__main__':
    app.run(port = 3000, debug = True)