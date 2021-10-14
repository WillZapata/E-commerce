from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators

class Formulario_Login(Form):
    Usuario = StringField('Usuario', 
    [
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=8, max=25)
    ])
    password = PasswordField('Contraseña', [validators.DataRequired(message='Campo requerido.')])

    recordar = BooleanField('Recordar contraseña')
    enviar = SubmitField('Iniciar sesión')


class Formulario_buscar(Form):
    Buscar = StringField('Buscar', 
    [
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=8, max=25)
    ])

    enviar2 = SubmitField('Buscar producto')




