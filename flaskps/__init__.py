from os import path
from flaskps.db import get_db
from flask import Flask, render_template, g, redirect, url_for, session
from flaskps.helpers.auth import authenticated
from flaskps.resources import user_resource
from flaskps.resources import auth
from flaskps.resources import configuracion
from flaskps.resources import book
from flaskps.resources import autor
from flaskps.resources import editorial
from flaskps.resources import genero

from flaskps.models.configuracion import Configuracion
from flaskps.config import Config
from flaskps.resources.api import calls


# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Autenticación
app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login)
app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)
app.add_url_rule(
    "/autenticacion",
    'auth_authenticate',
    auth.authenticate,
    methods=['POST']
)



#Configuracion
app.add_url_rule("/configuracion", 'configuracion_config', configuracion.config)
app.add_url_rule("/configuration/toggle", 'configuracion_toggleActive', configuracion.toggleActive)
app.add_url_rule("/configuration/edit", 'configuracion_edit', configuracion.editarInformacion, methods=['POST'])
app.add_url_rule("/configuration/edit", 'configuracion_render_edit', configuracion.renderEditarInformacion)
app.add_url_rule("/config", 'configuracion_changePage', configuracion.changePage, methods=['POST'])
# Usuarios

#Metodos para mostrar tablas de usuarios
app.add_url_rule("/usuarios", 'user_resource_index', user_resource.index)
app.add_url_rule("/usuarios/search_by_username", 'user_resource_indexUser', user_resource.indexUser, methods=['POST'])
app.add_url_rule("/usuarios/index_by_active", 'user_resource_indexActive', user_resource.indexActive)
app.add_url_rule("/usuarios/index_by_inactive", 'user_resource_indexInactive', user_resource.indexInactive)
#CRUD de usuarios
app.add_url_rule("/usuarios", 'user_resource_create', user_resource.create, methods=['POST']) #realiza creacion en el modelo
app.add_url_rule("/usuario/new", 'user_resource_new', user_resource.new) #levanta vista de creacion
app.add_url_rule("/usuarios/editar/<int:id>", 'user_resource_edit', user_resource.edit)#levanta vista de edicion
app.add_url_rule("/editar/<int:id>", 'user_resource_execute_edit', user_resource.executeEdit, methods=['POST']) #crea edicion en el modelo
app.add_url_rule("/usuarios/mostrar/<int:id>", 'user_resource_show', user_resource.show) #mostrar datos de usuario
app.add_url_rule("/usuarios/delete/<int:id>", 'user_resource_delete', user_resource.delete)#Baja logica
app.add_url_rule("/usuarios/active/<int:id>", 'user_resource_active', user_resource.active)#activacion de baja logica

#Asignacion de roles
app.add_url_rule("/usuarios/asignar", 'user_resource_indexAssign', user_resource.indexAssign) #listar usuarios y roles
app.add_url_rule("/usuarios/asignar/<string:user>/<string:rol>", 'user_resource_asignarRol', user_resource.assign) #asignar un rol
app.add_url_rule("/usuarios/eliminarRol/<string:user>/<string:rol>", 'user_resource_deleteRol', user_resource.deleteRol) #desasignar un rol

#CRUD de libros
app.add_url_rule("/libros/new/<string:isbn>", 'book_new', book.new)
app.add_url_rule("/libros/<string:isbn>", 'book_create', book.create, methods=['POST'])
app.add_url_rule("/libros/meta", 'book_meta', book.render_meta)
app.add_url_rule("/libros/meta", 'book_load_meta', book.load_meta, methods=['POST'])
app.add_url_rule("/libros/editar_meta/<string:isbn>", "book_meta_edit", book.edit_meta)
app.add_url_rule("/libros/editar_meta/<string:isbn>", "book_load_meta_edit", book.load_edit_meta, methods=['POST'])
app.add_url_rule("/libros/eliminar/<string:isbn>", "book_meta_remove", book.remove_meta)
#Manejo de libros
app.add_url_rule("/libros", 'book_menu', book.render_menu)
app.add_url_rule("/libros/ver", 'book_open', book.open_book)

#CRUD autor
app.add_url_rule("/autor/new", 'author_new', autor.new)
app.add_url_rule("/autor/create", "author_create", autor.create,methods=['POST'])
#CRUD editorial
app.add_url_rule("/editorial/new", 'editorial_new', editorial.new)
app.add_url_rule("/editorial/create", "editorial_create", editorial.create,methods=['POST'])
#CRUD genero
app.add_url_rule("/genero/new", 'genero_new', genero.new)
app.add_url_rule("/genero/create", "genero_create", genero.create,methods=['POST'])




@app.route("/")
def hello():
    Configuracion.db = get_db
    info = Configuracion.get_information()
    if(info.get('habilitado')):
        if not authenticated(session):
            return render_template('home.html', titulo=info.get('titulo'), descripcion=info.get('descripcion'), mail = info.get('mail_orquesta'))
        else:
            return redirect(url_for("user_resource_index"))
    else:
        return render_template('home_inactive.html') 
     
