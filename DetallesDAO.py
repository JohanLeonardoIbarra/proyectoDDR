from back import mysql

def conexion():
    return mysql.connection.cursor()

def listaProductos():
    productosPreload = conexion()
    productosPreload.execute('select * from producto')
    Productos = productosPreload.fetchall()
    mysql.connection.commit()
    return Productos

def listaPocosProductos():
    productosPreload = conexion()
    productosPreload.execute('select * from producto LIMIT 9')
    Productos = productosPreload.fetchall()
    mysql.connection.commit()
    return Productos

def Empresa():
    empresa = conexion()
    empresa.execute('select * from empresa')
    empresa = empresa.fetchall()
    mysql.connection.commit()
    return empresa

def ListaCategorias():
    categorias = conexion()
    categorias.execute('Select * from categoria')
    categorias = categorias.fetchall()
    mysql.connection.commit()
    return categorias

def UnProducto(id):
    producto = conexion()
    producto.execute('Select * from producto where id = {0}'.format(id))
    producto = producto.fetchone()
    mysql.connection.commit()
    return producto

def ProductosPorCategoria(id):
    producto = conexion()
    producto.execute('Select * from producto where categoria_id = '+id)
    producto = producto.fetchall()
    mysql.connection.commit()
    return producto

def Administradores():
    admins = conexion()
    admins.execute('Select * from admin')
    admins = admins.fetchall()
    mysql.connection.commit()
    return admins

def BorrarAdmin(id):
    cur = conexion()
    cur.execute('delete from admin Where id = {0}'.format(id))
    cur.connection.commit()
    return 'true'

def BorrarProducto(id):
    cur = conexion()
    cur.execute('Delete From producto Where id = {0}'.format(id))
    mysql.connection.commit()
    return 'true'

def BorrarCategoria(id):
    cur = conexion()
    cur.execute('delete from categoria where id = {0}'.format(id))
    mysql.connection.commit()
    return 'true'