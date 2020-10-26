from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug import secure_filename
import os, smtplib

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
    cur2 = mysql.connection.cursor()
    cur = mysql.connection.cursor()
    cur.execute('select * from producto LIMIT 9')
    cur2.execute('select * from empresa')
    data = cur.fetchall()
    data2 = cur2.fetchall()
    mysql.connection.commit()
    return render_template('index.html', productos = data, empresa = data2)

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

@app.route('/Empresa')
def empresa():
    cur = mysql.connection.cursor()
    cur.execute('select * from empresa')
    dato = cur.fetchall()
    mysql.connection.commit()
    return render_template('Empresa.html', empresa = dato)

@app.route('/ActualizarEmpresa', methods=['POST'])
def empresaupdate():
    if request.method == 'POST':
        nombre = request.form['nombre']
        qs = request.form['QuienesSomos']
        email = request.form['email']
        dir = request.form['dir']
        cel = request.form['cel']
        fb = request.form['facebook']
        tt = request.form['twitter']
        ig = request.form['instagram']
        cur = mysql.connection.cursor()
        cur.execute('Update * from empresa where id = 0 Values (0,%s,%s,%s,%s,%s,%s,%s,%s)', (nombre , qs , email, dir, cel, fb, tt, ig))
        mysql.connection.commit()
        return Empresa()

@app.route('/Contacto')
def contacto():
    return render_template('Contacto.html')

@app.route('/Correo', methods=['POST'])
def correo():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('select emailcontacto from empresa where id = 0')
        dato = cur.fetchone()[0]
    
        msg = MIMEMultipart()
        message = request.form['cuerpo']+'   '+request.form['email']
    
        password = "1234johan"
        msg['From'] = 'johanfalsoemail@gmail.com'
        msg['To'] = 'johanleon950@gmail.com'
        msg['Subject'] = request.form['asunto']
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        return contacto()


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
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('Select * from admin')
        data = cur.fetchall()
        mysql.connection.commit()
        nombre = request.form['userAdmin']
        password = request.form['passAdmin']
        for dato in data:
            if nombre == dato[1] :
                if password == dato[2] :
                    return Administrador()
        return render_template('admin.html')

@app.route('/User')
def userAdmin():
    cur = mysql.connection.cursor()
    cur.execute('Select * from admin')
    data = cur.fetchall()
    mysql.connection.commit()
    return render_template('User.html', usuarios = data)

@app.route('/User_Delete/<string:id>')
def del_user(id):
    if id == '0':
        return userAdmin()
    cur = mysql.connection.cursor()
    cur.execute('delete from admin Where id = {0}'.format(id))
    cur.connection.commit()
    return userAdmin()

@app.route('/Crear_Usuario', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute('insert into admin values(null,%s,%s)', (user, passw))
        mysql.connection.commit()
        return userAdmin()

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

@app.route('/Producto/<string:id>')
def Producto(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from producto where id = '+id)
    dato = cur.fetchall()
    mysql.connection.commit()
    return render_template('Producto.html', producto = dato)

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