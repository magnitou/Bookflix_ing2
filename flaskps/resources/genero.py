from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.genero import Genero

def new():
    return render_template('genero/new.html')

def create():
    set_db()
    if validate(request.form.get('nombre')):
        Genero.create(request.form) 
        flash("Genero cargado")
    return redirect(url_for("book_menu"))

def set_db():
    Genero.db = get_db()

def validate(name): 
    validate = True
    autores = Genero.all()
    for user in autores:
        if user.get('nombre').lower() == name.lower():                                           
            validate = False
            break
    return validate