from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.models.estudiante import Estudiante
from flaskps.models.barrio import Barrio
from flaskps.models.genero import Genero
from flaskps.models.responsable import Responsable
from flaskps.models.escuela import Escuela
from flaskps.models.nivel import Nivel
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
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    estudiantes = Estudiante.all()
    if (i == -1):
        i=0
    elif (i*pag >= len(estudiantes)):
        i = i - 1
    url = request.path
    permit = 'estudiantes_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('estudiante/index.html', estudiantes=estudiantes, i=i, pag=pag, url=url, permit = permit, adm = adm)

def new():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'estudiantes_new' not in session['permisos']:
        flash("No tiene permisos para crear estudiantes")
        return redirect(url_for('user_resource_index'))
    return render_template('estudiante/new.html', localidades = calls.get_localidad(),barrios= get_all_barrios(),generos = get_all_generos(),responsables = get_all_responsables(), escuelas = get_all_escuelas() , niveles = get_all_niveles(), tipos_de_documentos = calls.get_tipo_documentos())

def create():
    set_db()
    if True: #validate_user(request.form.get('username'), request.form.get('email')):
        Estudiante.create(request.form)
        flash("Estudiante creado con exito")
        if False:#"Estudiante_new" in session['permisos']: #Si está creando el administrador
            return redirect(url_for('user_resource_adminCreate'))
    else:
        flash("Estudiante/Correo ya registrado")
    return redirect(url_for('estudiante_index'))

def edit(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('/'))
    if 'estudiantes_update' not in session['permisos']:
        flash("No tiene permisos para editar estudiantes")
        return redirect(url_for('estudiante_index'))
    set_db()
    estudiante = Estudiante.find_by_id(id)
    return render_template('estudiante/edit.html', estudiante = estudiante, localidades = calls.get_localidad(),barrios= get_all_barrios(),generos = get_all_generos(),responsables = get_all_responsables(), escuelas = get_all_escuelas() , niveles = get_all_niveles(), tipos_de_documentos = calls.get_tipo_documentos())

def submitEdit(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'estudiantes_update' not in session['permisos']:
        flash("No tiene permisos para editar estudiantes")
        return redirect(url_for('estudiante_index'))
    set_db()
    Estudiante.update(request.form, id)
    return redirect(url_for('estudiante_index')) #redirect(url_for('estudiante_index'))
def delete(id):
    set_db()
    if 'estudiantes_destroy' not in session['permisos']:
        flash("No tiene permisos para eliminar estudiantes")
        return redirect(url_for('estudiante_index'))
    Estudiante.delete(id)
    flash("Estudiante eliminado con exito")
    return redirect(url_for('estudiante_index'))

def active(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    Estudiante.active(id)
    flash("Estudiante reincorporado con exito")
    return redirect(url_for('estudiante_index'))

def searchActive():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    return render_template('estudiantes/searchByActive.html')


def searchByDNI(dni):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    estudiantes = Estudiante.find_by_dni(request.form['dni'])
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if not "estudiantes_show" in session['permisos']:
        flash('No posee permiso para buscar')
        redirect(url_for('user_resource_index'))
    if (len(estudiantes) < 1):
        flash("No se encontraron estudiantes con ese username")
        return render_template('user/index.html', estudiantes=Estudiante.all(), i=i, pag=pag, adm=True)
    else:
        flash("Busqueda realizada con exito")
        return render_template('user/index.html', estudiantes=estudiantes, i=i, pag=pag, adm=True)    

def searchByApellido(apellido):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    estudiantes = Estudiante.find_by_apellido(request.form['apellido'])
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if not "estudiantes_show" in session['permisos']:
        flash('No posee permiso para buscar')
        redirect(url_for('user_resource_index'))
    if (len(estudiantes) < 1):
        flash("No se encontraron estudiantes con ese username")
        return render_template('user/index.html', estudiantes=Estudiante.all(), i=i, pag=pag, adm=True)
    else:
        flash("Busqueda realizada con exito")
        return render_template('user/index.html', estudiantes=estudiantes, i=i, pag=pag, adm=True)    

def indexActive():
    url = request.path
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    estudiantes = Estudiante.find_by_active()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(estudiantes)):
        i = i - 1
    url = request.path
    permit = 'estudiantes_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('estudiante/index.html', estudiantes=estudiantes,i=i, pag=pag, url = url, permit = permit, adm = adm)

def indexInactive():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    estudiantes = Estudiante.find_by_inactive()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(estudiantes)):
        i = i - 1
    url = request.path
    permit = 'estudiantes_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('estudiante/index.html', estudiantes=estudiantes, i=i, pag=pag, url = url, permit = permit, adm = adm)

def set_db():
    Estudiante.db = get_db()

def set_barrio_db():
    Barrio.db = get_db()

def set_genero_db():
    Genero.db = get_db()

def set_responsable_db():
    Responsable.db = get_db()

def set_escuela_db():
    Escuela.db = get_db()

def set_nivel_db():
    Nivel.db = get_db()

def get_all_barrios():
    set_barrio_db()
    return Barrio.all()
def get_all_generos():
    set_genero_db()
    return Genero.all()
def get_all_responsables():
    set_responsable_db()
    return Responsable.all()
def get_all_escuelas():
    set_escuela_db()
    return Escuela.all()
def get_all_niveles():
    set_nivel_db()
    return Nivel.all()
