from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug import secure_filename
import os, smtplib, DetallesDAO

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
    Productos = DetallesDAO.listaPocosProductos()
    Empresa = DetallesDAO.Empresa()
    return render_template('index.html', productos = Productos , empresa = Empresa)

@app.route('/Catalogo')
def catalogo():
    Productos = DetallesDAO.listaProductos()
    Categorias = DetallesDAO.ListaCategorias()
    return render_template('Catalogo.html', productos = Productos, categorias = Categorias)

@app.route('/EditProducto/<string:id>')
def edit_producto(id):
    Producto = DetallesDAO.UnProducto(id)
    return render_template('EditProducto.html', producto = Producto)

@app.route('/Empresa')
def empresa():
    Empresa = DetallesDAO.Empresa()
    return render_template('Empresa.html', empresa = Empresa)

@app.route('/Categorias')
def categorias():
    Categorias = DetallesDAO.ListaCategorias()
    return render_template('Categorias.html', categoria = Categorias)

@app.route('/Catalogo/<string:id>')
def catalogoconid(id):
    Productos = DetallesDAO.ProductosPorCategoria(id)
    Categorias = DetallesDAO.ListaCategorias()
    return render_template('Catalogo.html', productos = Productos, categorias = Categorias)

@app.route('/Administrador')
def Administrador():
    Productos = DetallesDAO.listaProductos()
    Categorias = DetallesDAO.ListaCategorias()
    return render_template('registro.html', categorias = Categorias, productos = Productos)

@app.route('/Producto/<string:id>')
def Producto(id):
    Producto = DetallesDAO.UnProducto(id)
    return render_template('Producto.html', producto = Producto)

@app.route('/Crear_Usuario', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute('insert into admin values(null,%s,%s)', (user, passw))
        mysql.connection.commit()
        return userAdmin()

@app.route('/Categoria_Delete/<string:id>')
def del_categorias(id):
    DetallesDAO.BorrarCategoria(id)
    return categorias()

@app.route('/Eliminar/<string:id>')
def delete_producto(id):
    DetallesDAO.BorrarProducto(id)
    return Administrador()


#Usuarios y Login

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        Admins = DetallesDAO.Administradores()
        nombre = request.form['userAdmin']
        password = request.form['passAdmin']
        for dato in Admins:
            if nombre == dato[1] :
                if password == dato[2] :
                    return Administrador()
        return render_template('admin.html')

@app.route('/User')
def userAdmin():
    Admins = DetallesDAO.Administradores()
    return render_template('User.html', usuarios = Admins)

@app.route('/User_Delete/<string:id>')
def del_user(id):
    if id == '0':
        return userAdmin()
    DetallesDAO.BorrarAdmin(id)
    return userAdmin()

#Actualizacion en la Base de Datos

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
        cur.execute('Update empresa Set nombre = %s, quienessomos = %s, emailcontacto = %s, direccion = %s, telefonocontacto = %s, facebook = %s, twitter = %s, instagram = %s where id = 0', (nombre , qs , email, dir, cel, fb, tt, ig))
        mysql.connection.commit()
        return empresa()

@app.route('/EditarProducto', methods = ['POST'])
def editarProducto():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        ref = request.form['referencia']
        desc = request.form['descripcion']
        detail = request.form['detalle']
        valor = request.form['valor']
        cur = mysql.connection.cursor()
        cur.execute('Update producto Set nombre = %s, referencia = %s, descripcioncorta = %s, detalle = %s, valor = %s Where id = '+ id, (name, ref, desc, detail, valor))
        mysql.connection.commit()
        return Administrador()


#Insersiones en la Base de datos

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

@app.route('/Crear_Categoria', methods = ['POST'])
def crear_categoria():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute('Insert into categoria values (%s, %s, %s)', (id, nombre, 1))
        mysql.connection.commit()
        return categorias()



#Formulario De Contacto y Envio de Correo

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


if __name__ == '__main__':
    app.run(port = 3000, debug = True)