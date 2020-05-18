from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.editorial import Editorial

def new():
    return render_template('editorial/new.html')

def create():
    set_db()
    Editorial.create(request.form)
    flash("Editorial cargado")
    return redirect(url_for("book_menu"))

def set_db():
    Editorial.db = get_db()