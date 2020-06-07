from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.novedad import Novedad

def new():
    return render_template("novedad/new.html")
 
def create():
    set_db()    
    Novedad.create(request.form)
    flash("Novedad cargada")
    return redirect(url_for("novedad_index"))

def index():
    set_db()
    #novedades = Novedad.all()
    #admPermit = "configuracion_usarInhabilitado" in session['permisos']
    return render_template("novedad/menu.html")#, novedades=novedades, adm=admPermit)

def set_db():
    Novedad.db = get_db()

