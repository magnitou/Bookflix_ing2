from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.models.docente import Docente
from flaskps.models.genero import Genero
from flaskps.models.configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.rols import mapRol
from flaskps.resources.auth import hasPermit
from flaskps.resources.api import calls



def index():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/') 
    set_db()
    docentes = Docente.all()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(docentes)):
        i = i - 1
    url = request.path
    permit = 'docentes_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('docente/index.html', docentes=docentes, i=i, pag=pag, url=url, adm=adm, permit=permit)

def indexDocente():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    docentes = Docente.find_by_apellido(request.form['apellido']) 
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    permit = 'docentes_show' in session['permisos']
    return render_template('docente/index.html', docentes=docentes, i=i, pag=pag, permit = permit)


def indexActive():
    url = request.path
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    docentes = Docente.find_by_active()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(docentes)):
        i = i - 1
    url = request.path
    permit = 'docentes_show' in session['permisos']
    return render_template('docente/index.html', docentes=docentes,i=i, pag=pag, url = url, permit = permit)

def indexInactive():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    docentes = Docente.find_by_inactive()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(docentes)):
        i = i - 1
    url = request.path
    permit = 'docentes_show' in session['permisos']
    return render_template('docente/index.html', docentes=docentes, i=i, pag=pag, url = url, permit = permit)


def new():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'docentes_new' not in session['permisos']:
        flash('No tiene permisos para crear un nuevo docente')
        redirect(url_for('docente_index'))
    set_db()
    if not validate_docente(request.form.get('numero')):
        Docente.create(request.form)
        flash("Docente creado con exito")
    else:
        flash("Ya existe un docente con ese DNI ya registrado")
    return redirect(url_for('docente_index'))

def delete(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'docentes_destroy' not in session['permisos']:
        flash('No tiene permisos para eliminar un docente')
        redirect(url_for('docente_index'))
    set_db()
    Docente.delete(id)
    flash("Docente: '" + Docente.find_by_id(id).get('apellido') + ", " + Docente.find_by_id(id).get('nombre') + "' deshabilitado con exito")
    return redirect(url_for('docente_index'))

def edit(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'docentes_update' not in session['permisos']:
        flash('No tiene permisos para editar un docente')
        redirect(url_for('docente_index'))
    set_db()
    Docente.update(request.form, id)
    return redirect(url_for('docente_index'))

def create():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/') 
    if 'docentes_new' not in session['permisos']:
        flash('No tiene permisos para crear un nuevo docente')
        redirect(url_for('docente_index'))
    localidades = calls.get_localidad()
    tipos_documento = calls.get_tipo_documentos()
    set_genero_db()
    generos = Genero.all()
    return render_template('docente/new.html', localidades = localidades, tipos_documento = tipos_documento, generos = generos)

def active(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'docentes_destroy' not in session['permisos']:
        flash('No tiene permisos para restaurar un docente eliminado')
        redirect(url_for('docente_index'))
    set_db()
    Docente.active(id)
    flash("Docente: '" + Docente.find_by_id(id).get('apellido') + ", " + Docente.find_by_id(id).get(
        'nombre') + "' habilitado con exito")
    return redirect(url_for('docente_index'))

def set_db():
    Docente.db = get_db()

def set_genero_db():
    Genero.db = get_db()

def validate_docente(dni):
    return Docente.exist(dni).get('count(numero)') == 1

def update(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'docentes_update' not in session['permisos']:
        flash('No tiene permisos para editar un docente')
        return redirect(url_for('docente_index'))
    set_db()
    docente = Docente.find_by_id(id)
    set_genero_db()
    generos = Genero.all()
    localidades = calls.get_localidad()
    tipos_de_documentos = calls.get_tipo_documentos()
    return render_template('docente/edit.html', docente = docente, localidades = localidades, tipos_de_documentos = tipos_de_documentos, generos = generos)