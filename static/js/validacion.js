function validar_formulario() {
    bnombre = document.getElementById("Nombre").value;
    busuario = document.getElementById("Usuario").value;
    bsexo = document.getElementById("Sexo").value;
    bemail = document.getElementById("email").value;
    bpassword = document.getElementById("password").value;
    bcondiciones = document.getElementById("Condiciones").value;
    var expreg = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;

        if (busuario == ""){
            alert("El campo usuario no debe estar vacio");
            return false;
        }else if (busuario.length < 8){
            alert("El campo usuario debe tener mínimo 8 caracteres");
            return false;
        }else if (bemail == ""){
            alert("El campo correo electrónico no debe estar vacio");
            return false;
        }else if (expreg.test(bemail) == false) {
            alert("No es un correo electrónico valido"); 
            return false;
        }else if (bpassword == ""){
            alert("El campo contraseña no debe estar vacio");
            return false;
        }else if (bpassword.length < 8){
            alert("El campo contraseña debe tener mínimo 8 caracteres");
            return false;
        }
}

function mostrarpassword() {
    var obj = document.getElementById("password");
    obj.type = "text"
}

function ocultarpassword() {
    var obj = document.getElementById("password");
    obj.type = "password"
}

