from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.user_model import Usuario
from flaskps.models.perfil import Perfil

def render_menu():
    Perfil.db = get_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    print(perfiles)
    return render_template("perfil/menu.html", perfiles=perfiles)

def select(id):
    session['perfil'] = id
    return redirect(url_for("book_menu"))

def new():    
    return render_template("perfil/new.html")

def create():
    Perfil.db = get_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    plan = Usuario.find_by_id(session['usuario_id'])
    if plan == 'Basico' and len(perfiles)==2:
        flash("Su plan no permite más perfiles")
        return redirect(url_for("perfil_menu"))
    if plan == 'Premium' and len(perfiles)==4:
        flash("No se puede tener más de 4 perfiles")
        return redirect(url_for("perfil_menu"))    
    Perfil.create(request.form.get("nombre"), session['usuario_id'])
    return redirect(url_for("perfil_menu"))
