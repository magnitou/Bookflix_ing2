from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.trailer import Trailer

def new():
    return render_template("trailers/new.html")

def create():
    set_db()


def create(): #Crea / Guarda un archivo de libro
    set_db()
    Trailer.create(request.form)
    flash("trailer cargado")
    return redirect(url_for("trailer_index"))

def index():
    set_db()
    trailer = Trailer.all()

    #novedades = Novedad.all()
    #admPermit = "configuracion_usarInhabilitado" in session['permisos']
    return render_template("trailer/menu.html")#, novedades=novedades, adm=admPermit)



def set_db():
    Trailer.db = get_db()