from Back import mysql

def listaProductos():
    productosPreload = mysql.connection.cursor()
    productosPreload.execute('select * from producto')
    Productos = productosPreload.fetchall()
    mysql.connection.commit()
    return Productos

def listaPocosProductos():
    productosPreload = mysql.connection.cursor()
    productosPreload.execute('select * from producto LIMIT 9')
    Productos = productosPreload.fetchall()
    mysql.connection.commit()
    return Productos

def Empresa():
    empresa = mysql.connection.cursor()
    empresa.execute('select * from empresa')
    empresa = empresa.fetchall()
    mysql.connection.commit()
    return empresa

def ListaCategorias():
    categorias = mysql.connection.cursor()
    categorias.execute('Select * from categoria')
    categorias = categorias.fetchall()
    mysql.connection.commit()
    return categorias

def UnProducto(id):
    producto = mysql.connection.cursor()
    producto.execute('Select * from producto where id = {0}'.format(id))
    producto = producto.fetchone()
    mysql.connection.commit()
    return producto

def ProductosPorCategoria(id):
    producto = mysql.connection.cursor()
    producto.execute('Select * from producto where categoria_id = '+id)
    producto = producto.fetchall()
    mysql.connection.commit()
    return producto

def Administradores():
    admins = mysql.connection.cursor()
    admins.execute('Select * from admin')
    admins = admins.fetchall()
    mysql.connection.commit()
    return admins

def BorrarAdmin(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from admin Where id = {0}'.format(id))
    cur.connection.commit()
    return 'true'

def BorrarProducto(id):
    cur = mysql.connection.cursor()
    cur.execute('Delete From producto Where id = {0}'.format(id))
    mysql.connection.commit()
    return 'true'

def BorrarCategoria(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from categoria where id = {0}'.format(id))
    mysql.connection.commit()
    return 'true'