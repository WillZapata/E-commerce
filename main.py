from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask.wrappers import Request
from werkzeug import datastructures
from utils import isEmailValid, isUsernameValid, isPasswordValid
import yagmail as yagmail
from forms import Formulario_Login, Formulario_buscar


app = Flask(__name__)
app.secret_key = "Will"

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            vusuario = request.form['Usuario']
            vemail = request.form['email']
            vcontraseña = request.form['password']

            error = None

            if not isUsernameValid(vusuario):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
            if not isEmailValid(vemail):
                error = "Correo invalido"
                flash(error)
            if not isPasswordValid(vcontraseña):
                error = "La contraseña debe contener al menos una minuscula, una mayuscula, un número y 8 caracteres"
                flash(error)

            if error is not None:
                return render_template("registrarse.html")
            else:
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
        Usuario = form.Usuario.data
        password = form.password.data
        flash('Inicio de sesión solicitado por el usuario {}, recordar={}'.format(form.Usuario.data, form.recordar.data))
        return redirect(url_for('gracias'))


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
    return render_template("entrada.html")