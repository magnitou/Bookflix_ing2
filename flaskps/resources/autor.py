from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.autor import Autor

def new():
    return render_template('autor/new.html')

def create():
    set_db()
    Autor.create(request.form)
    flash("Autor cargado")
    return redirect(url_for("book_menu"))

def set_db():
    Autor.db = get_db()