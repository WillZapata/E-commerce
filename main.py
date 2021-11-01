from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask import redirect, url_for
from flask.wrappers import Request
from werkzeug import datastructures
from utils import isEmailValid, isUsernameValid, isPasswordValid
import yagmail as yagmail
from forms import Formulario_Login, Formulario_buscar
import os
from db import get_db
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            vnombre = request.form['Nombre']
            vusuario = request.form['Usuario']
            vsexo = request.form['Sexo']
            vemail = request.form['email']
            vcontraseña = request.form['password']

            error = None
            db = get_db()

            if not isUsernameValid(vusuario):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
            if not isEmailValid(vemail):
                error = "Correo invalido"
                flash(error)
            if not isPasswordValid(vcontraseña):
                error = "La contraseña debe contener al menos una minuscula, una mayuscula, un número, un simbolo y 5 caracteres"
                flash(error)

            user = db.execute('SELECT * FROM usuarios WHERE correo = ? ', (vemail,)).fetchone()
            if user is not None:
                error = "Correo electronico ya existe"
                flash(error)

            if error is not None:
                return render_template("registrarse.html")
            else:
                db.execute('INSERT INTO usuarios (nombre, usuario, correo, contraseña) VALUES(?, ?, ?, ?)', (vnombre, vusuario, vemail, vcontraseña)
                )
                db.commit()

                yag = yagmail.SMTP('realjosereyes10@gmail.com', 'croscros')
                yag.send(to=vemail, subject='Activa tu cuenta',
                    contents='Bienvenido, usa este link para activar tu cuenta')
                flash('Revisa tu correo para activar tu cuenta')       
                return redirect( url_for('login') )

        return render_template("registrarse.html")
    except:
        flash("Se generó un error en el proceso")
        return render_template("registrarse.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = Formulario_Login(request.form)
    if request.method == 'POST' and form.validate():
        db = get_db()
        Usuario = form.Usuario.data
        password = form.password.data

        error = None

        if not Usuario:
            error = "Usuario requerido"
            flash(error)
        if not password:
            error = "Contraseña requerida"
            flash(error)

        if error is not None:
            return render_template("login.html", form=form)
        else:
            user = db.execute('SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ? ', (Usuario, password)).fetchone()
            print(user)
            if user is None:
                flash('Usuario y contraseña no son correctos')
                return render_template("login.html", form=form)
            else:
                flash('Ahora puedes elegir tus productos favoritos y realizar tus compras con nosotros')
                return redirect(url_for('principal'))
                
    return render_template("login.html", form=form)

@app.route('/gracias/', methods=['GET'])
def gracias():
    return render_template("gracias.html")

@app.route('/principal/', methods=['GET', 'POST'])
def principal():
    form = Formulario_buscar(request.form)
    if request.method == 'POST' and form.validate():
        flash('Usted esta buscando el producto= {}'.format(form.Buscar.data))
        return redirect(url_for('principal'))


    return render_template("principal.html", form=form)

@app.route('/')
@app.route('/index/')
@app.route('/entrada/', methods=['GET', 'POST'])
def entrada():
    productos = sql_select_productos()
    return render_template("entrada.html", productos=productos)

@app.route('/agregar/', methods=['GET', 'POST'])
def agregar_producto():
    try:
        if request.method == 'POST':
            vid = request.form['id']
            vcategoria = request.form['id_categoria']
            vnombre = request.form['Nombre']
            vprecio = request.form['Precio']
            vcantidad = request.form['Cantidad']

            error = None
            db = get_db()

            if not vid:
                error = "Codigo requerido"
                flash(error)
            if not vcategoria:
                error = "Codigo requerido"
                flash(error)
            if not vnombre:
                error = "Nombre requerido"
                flash(error)
            if not vprecio:
                error = "Precio requerido"
                flash(error)
            if not vcantidad:
                error = "Cantidad requerida"
                flash(error)

            name = db.execute('SELECT * FROM productos WHERE id_producto = ? ', (vid)).fetchone()
            if name is not None:
                error = "Producto ya existe"
                flash(error)

            if error is not None:
                return render_template("registrar_producto.html")
            else:
                db.execute('INSERT INTO productos (id_producto, id_categoria, nombre_producto, precio, cantidad) VALUES(?, ?, ?, ?, ?)', (vid, vcategoria, vnombre, vprecio, vcantidad)
                )
                db.commit()
                flash('Producto agregado a base de datos')       
                return redirect( url_for('productos') )

        return render_template("registrar_producto.html")
    except:
        flash("Se generó un error en el proceso")
        return render_template("registrar_producto.html")

@app.route('/restapi/productos', methods=['GET'])
def get_productos():
    productos = sql_resapi_select_productos()
    return jsonify( {"productos": productos} )

@app.route('/usuarios')
def usuario():
    usuarios = sql_select_usuarios()
    return render_template("usuario.html", usuarios=usuarios)

def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        print("Conexion OK")
        return con
    except Error:
        print(Error)

def sql_select_productos():
    sql = strsql = "select * from productos"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(sql)
    productos = cursorObj.fetchall()
    return productos

def sql_select_usuario():
    sql = strsql = "select * from productos WHERE id=?"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(sql)
    usuario = cursorObj.fetchall()
    return usuario

def sql_resapi_select_productos():
    sql = strsql = "select * from productos"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(sql)
    productos = cursorObj.fetchall()
    lista_productos = [ { "id_producto": producto[0], "id_categoria": producto[1], "nombre_producto": producto[2], "precio": producto[3], "cantidad": producto[4] } for producto in productos ]
    return lista_productos


def sql_select_usuarios():
    sql = strsql = "select * from usuarios"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(sql)
    usuarios = cursorObj.fetchall()
    return usuarios

def select_usuario():
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("SELECT nombre, usuario, correo, contraseña FROM usuarios WHERE id=?;", (nombre, usuario, correo, contraseña))
    usuarios = cursorObj.fetchall()
    lista_usuarios = [ { "id": id, "nombre": nombre, "usuario": usuario, "correo": correo, "contraseña": contraseña } ]
    return lista_usuarios


# @app.route('/delete/<id>/', methods=['GET', 'POST'])
# def borrar_producto():
#     id = request.args.get('id')
#     sql_delete_usuario(id)
#     flash("Usuario id = {} eliminado".format(id))
#     return redirect(url_for('usuario'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def borrar_usuario(id):
    int(id)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM usuarios WHERE id=?", (id,))
    con.commit()
    flash("Usuario Eliminado Exitosamente")
    return redirect(url_for('usuario'))


# def sql_delete_usuario(id):
#     sql = "DELETE FROM usuarios WHERE id = '{}'".format(id)
#     print(sql)
#     con = sql_connection()
#     cursorObj = con.cursor()
#     cursorObj.execute(sql)
#     con.commit()
#     con.close()


@app.route('/actualizar_usuario/<id>/', methods=['GET'])
def actualizar_usuario(id):
    print("Hola mundo")
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM usuarios WHERE id=?;", (id,))
    usu = cursorObj.fetchone()
    # cursorObj.execute("UPDATE usuarios SET nombre = ?, usuario = ?, correo = ?, contraseña = ? WHERE id = ?", (nombre,usuario,correo,contraseña,id))
    con.commit()
    # flash("Usuario Actualizado Exitosamente")
    return render_template("actualizar.html",usu=usu)

@app.route('/editar/<id>/', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        usuario = request.form['Usuario']
        correo = request.form['email']
        contraseña = request.form['password']
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute("UPDATE usuarios SET nombre = ?, usuario = ?, correo = ?, contraseña = ? WHERE id = ?", (nombre,usuario,correo,contraseña,id))
        con.commit()
        flash("Usuario Actualizado Exitosamente")
        return redirect(url_for('usuario'))

# con = sql_connection()
#     cursorObj = con.cursor()
#     cursorObj.execute("SELECT nombre, usuario, correo, contraseña FROM usuarios WHERE id=?;", (nombre, usuario, correo, contraseña))
#     usuarios = cursorObj.fetchall()
#     lista_usuarios = [ { "id": id, "nombre": nombre, "usuario": usuario, "correo": correo, "contraseña": contraseña } ]

# def sql_edit_producto(id, nombre, precio, existencia):
#     sql = "UPDATE Producto SET nombre = '{}', precio = '{}', existencia = '{}' WHERE id = '{}'".format(nombre, precio, existencia, id)
#     print(sql)
#     con = sql_connection()
#     cursorObj = con.cursor()
#     cursorObj.execute(sql)
#     con.commit()
#     con.close()

@app.route('/actualizar/<id>', methods=['GET'])
def actualizar():
    return render_template("actualizar.html")