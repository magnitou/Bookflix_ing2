from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.editorial import Editorial

def new():
    return render_template('editorial/new.html')

def create():
    set_db()
    if validate(request.form.get('nombre')):
        Editorial.create(request.form)
        flash("Editorial cargado")
    return redirect(url_for("book_menu"))

def set_db():
    Editorial.db = get_db()

def validate(name): 
    validate = True
    autores = Editorial.all()
    for user in autores:
        if user.get('nombre').lower() == name.lower():                                           
            validate = False
            break
    return validate