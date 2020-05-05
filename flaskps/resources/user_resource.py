from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.models.user_model import Usuario
from flaskps.models.configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.rols import mapRol
from flaskps.resources.auth import hasPermit


def show(id): #mostrar datos de un usuario
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/') 
    set_db()
    usuario = Usuario.find_by_id(id)
    return render_template('/user/show.html', usuario=usuario)

def index():
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/') 
    set_db()
    usuarios = Usuario.all()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(usuarios)):
        i = i - 1
    admPermit = "configuracion_usarInhabilitado" in session['permisos']
    return render_template('user/index.html', usuarios=usuarios, i=i, pag=pag, url=request.path, adm= admPermit, permit = admPermit) # Solo el admin puede usar Inhabilitade asi que usamos eso para saber si es admin

def indexUser(): #mostrar usuario con cierto nombre
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    usuarios = Usuario.find_by_username(request.form['username'])
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if not "usuario_show" in session['permisos']:
        flash('No posee permiso para buscar')
        redirect(url_for('user_resource_index'))
    admPermit = "configuracion_usarInhabilitado" in session['permisos']
    if (len(usuarios) < 1):
        flash("No se encontraron usuarios con ese username")
        return render_template('user/index.html', usuarios=Usuario.all(), i=i, pag=pag, adm=admPermit, permit = admPermit)
    else:
        flash("Busqueda realizada con exito")
        return render_template('user/index.html', usuarios=usuarios, i=i, pag=pag, adm=admPermit , permit = admPermit)

def indexActive(): #mostrar todos los usuarios activos
    url = request.path
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    usuarios = Usuario.find_by_active()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(usuarios)):
        i = i - 1
    url = request.path
    adm = False
    if "usuario_index" in session['permisos']:
        adm = True
    return render_template('user/index.html', usuarios=usuarios, i=i, pag=pag, url=url, adm=adm, permit = "configuracion_usarInhabilitado" in session['permisos'])

def indexInactive(): #mostrar usuarios inactivos
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    usuarios = Usuario.find_by_inactive()
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag > len(usuarios)):
        i = i - 1
    url = request.path
    adm = False
    if "usuario_index" in session['permisos']:
        adm = True
    return render_template('user/index.html', usuarios=usuarios, i=i, pag=pag, url=url, adm=adm, permit = "configuracion_usarInhabilitado" in session['permisos'])

def new(): #Levanta la vista de creacion de usuario
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    if 'usuario_new' not in session['permisos']:
        flash("No tiene permisos para crear un usuario")
        return redirect(url_for('user_resource_index'))
    return render_template('user/new.html')


def edit(id): #levanta la vista de editar usuario
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    usuario = Usuario.find_by_id(id)
    adm = False
    if "usuario_edit" in session['permisos']:
        adm = True
    return render_template('user/edit.html', usuario=usuario, adm=adm)

def assign(user, rol): #asignacion de rol
    set_db()
    user_id = Usuario.get_id_by_username(user)
    rol_id = mapRol(rol)
    
    Usuario.change_rol(user_id, rol_id)
    newrol = Usuario.get_rol(user_id)
    
    return redirect(url_for('user_resource_indexAssign'))


def deleteRol(user, rol): #sacar rol
    set_db()
    user_id = Usuario.get_id_by_username(user)
    rol_id = mapRol(rol)
    Usuario.delete_rol(user_id, rol_id)
    newrol = Usuario.get_rol(user_id)
    if 'usuario_asignar_rol' not in session['permisos']:
        flash("No tiene permisos para editar un usuario")
        return redirect(url_for('user_resource_index'))
    #usuario_destroy
    return redirect(url_for('user_resource_indexAssign'))

def indexAssign():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/') 
    set_db()
    usuarios = Usuario.all()
    i = int(request.args.get('i',0))
    if (i == -1):
        i=0
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    rols = Configuracion.get_users_rols()
    userRolsDict = {}
    for pair in rols:
        id = pair['usuario_id'] 
        if id not in userRolsDict.keys():
            userRolsDict[pair['usuario_id']] = []
        userRolsDict[id].append(pair['rol_id'])
    if 'usuario_asignar_rol' not in session['permisos']:
        flash('No tienes permisos para acceder')
        return redirect('/')
    return render_template('user/rols.html', usuarios = usuarios, delete = False, i=i, pag=pag, mapIdRol=userRolsDict)


def executeEdit(id): #baja la edición al modelo
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('user_resource_index'))
    print(session['permisos'])
    if 'usuario_update' not in session['permisos']:
        flash("No tiene permisos para editar un usuario")
        return redirect(url_for('user_resource_index'))
    set_db()
    Usuario.update(request.form, id)
    flash("Se modifico al usuario "+ request.form.get('username') + " correctamente")
    return redirect(url_for('user_resource_index'))


def create(): #crea un usuario
    set_db()
    if "usuario_new" in session['permisos']: #Si está creando el administrador
        if validate_user(request.form.get('username'), request.form.get('email')):
            Usuario.create(request.form)
            flash("Usuario creado con exito")
        else:
            flash("Usuario/Correo ya registrado")
    return redirect(url_for('user_resource_index'))

def delete(id): #inhabilita un usuario a usar la pagina
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    if 'usuario_destroy' not in session['permisos']:
        flash("No tiene permisos para deshabilitar usuarios")
        return redirect(url_for('user_resource_index'))
    Usuario.delete(id)
    return redirect(url_for('user_resource_index'))

def active(id): #Habilita a un usuario inhabilitado para usar la pagina
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    if 'usuario_activar' not in session['permisos']:
        flash("No tiene permisos para deshabilitar usuarios")
        return redirect(url_for('user_resource_index'))
    Usuario.active(id)
    return redirect(url_for('user_resource_index'))


def validate_user(username, email): # valida que haya un usuario en el sistema con ese mail o nombre de usuario
    validate = True
    for user in get_all_users() :
        if user.get('username') == username or user.get('email') == email:
            validate = False
            break
    return validate

def get_all_users():
    set_db()
    usuarios = Usuario.all()
    return usuarios

def set_db():
    Usuario.db = get_db()

def loggedIn():
    if not authenticated(session):
        flash("no inicio sesion")
        return redirect('/') 
    return None