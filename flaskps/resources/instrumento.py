from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.helpers.auth import authenticated
from flaskps.models.configuracion import Configuracion
from flaskps.models.instrumento import Instrumento
from flaskps.models.tipo_instrumento import Tipo_Instrumento
import os

def new():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'instrumento_new' not in session['permisos']:
        flash("No tiene permisos para crear instrumentos")
        return redirect(url_for('instrumento_index'))
    return render_template('instrumento/new.html', tipos_instrumentos = get_all_tipo_instrumentos() )

def create():
    set_db()
    if validate_instrumento(request.form.get('id_instrumento')):
        Instrumento.create(request.form, request.files)
        if request.files: 
            image = request.files['imagen']
            if image.filename not in os.listdir('flaskps/static/uploads'):
                image.save(os.path.join('flaskps/static/uploads', image.filename))
        flash("Instrumento creado con exito")
        if "instrumento_new" in session['permisos']: #Si está creando el administrador
            return redirect(url_for('instrumento_index'))
    else:
        flash("El Instrumento ya está registrado")
    return redirect(url_for('instrumento_index'))

def index():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/') 
    set_db()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    instrumentos = Instrumento.all()
    if (i == -1):
        i=0
    elif (i*pag >= len(instrumentos)):
        i = i - 1
    url = request.path
    permit = 'instrumento_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('instrumento/index.html', instrumentos=instrumentos, i=i, pag=pag, url=url, permit = permit, adm = adm)

def edit(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('/'))
    if 'instrumento_update' not in session['permisos']:
        flash("No tiene permisos para editar instrumentos")
        return redirect(url_for('instrumento_index'))
    set_db()
    instrumento = Instrumento.find_by_id(id)
    return render_template('instrumento/edit.html', instrumento = instrumento, tipos_instrumentos = get_all_tipo_instrumentos())

def submitEdit(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'instrumento_update' not in session['permisos']:
        flash("No tiene permisos para editar instrumentos")
        return redirect(url_for('instrumento_index'))
    set_db()    
    if request.files: 
        image = request.files['imagen']
        if image.filename == '':
            filename = Instrumento.get_filename(id)            
        else:
            filename = image.filename        
        Instrumento.update(request.form,filename, id)
        if filename not in os.listdir('flaskps/static/uploads'):            
            image.save(os.path.join('flaskps/static/uploads', filename))
    if not validate_instrumento(request.form['id']):
        flash("Ya existe un instrumento con ese identificador")
        return redirect(url_for('instrumento_index'))
    return redirect(url_for('instrumento_index'))

def delete(id):
    set_db()
    if 'instrumento_destroy' not in session['permisos']:
        flash("No tiene permisos para eliminar instrumentos")
        return redirect(url_for('instrumento_index'))
    Instrumento.delete(id)
    flash("Instrumento eliminado con exito")
    return redirect(url_for('instrumento_index'))

def active(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    Instrumento.active(id)
    flash("Estudiante reincorporado con exito")
    return redirect(url_for('estudiante_index'))

def searchActive():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    return render_template('instrumentos/searchByActive.html')


def searchByDNI(dni):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    instrumentos = Instrumento.find_by_dni(request.form['dni'])
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if not "instrumento_show" in session['permisos']:
        flash('No posee permiso para buscar')
        redirect(url_for('user_resource_index'))
    if (len(instrumentos) < 1):
        flash("No se encontraron instrumentos con ese username")
        return render_template('user/index.html', instrumentos=Instrumento.all(), i=i, pag=pag, adm=True)
    else:
        flash("Busqueda realizada con exito")
        return render_template('user/index.html', instrumentos=instrumentos, i=i, pag=pag, adm=True)    

def searchByApellido(apellido):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    instrumentos = Instrumento.find_by_apellido(request.form['apellido'])
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if not "instrumento_show" in session['permisos']:
        flash('No posee permiso para buscar')
        redirect(url_for('user_resource_index'))
    if (len(instrumentos) < 1):
        flash("No se encontraron instrumentos con ese username")
        return render_template('user/index.html', instrumentos=Instrumento.all(), i=i, pag=pag, adm=True)
    else:
        flash("Busqueda realizada con exito")
        return render_template('user/index.html', instrumentos=instrumentos, i=i, pag=pag, adm=True)    

def indexActive():
    url = request.path
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    instrumentos = Instrumento.find_by_active()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(instrumentos)):
        i = i - 1
    url = request.path
    permit = 'instrumento_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('estudiante/index.html', instrumentos=instrumentos,i=i, pag=pag, url = url, permit = permit, adm = adm)

def indexInactive():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    instrumentos = Instrumento.find_by_inactive()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(instrumentos)):
        i = i - 1
    url = request.path
    permit = 'instrumento_index' in session['permisos']
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('estudiante/index.html', instrumentos=instrumentos, i=i, pag=pag, url = url, permit = permit, adm = adm)

def get_all_tipo_instrumentos():
    set_tipo_instrumento_db()
    return Tipo_Instrumento.all()

def set_tipo_instrumento_db():
    Tipo_Instrumento.db = get_db()

def set_db():
    Instrumento.db = get_db()

def validate_instrumento(id):
    return len(Instrumento.validate_instrumento(id)) == 0

def serve_image(inst_id):
    set_db()
    img = Instrumento.find_by_id(inst_id)
    print (img)
    return img['imagen']