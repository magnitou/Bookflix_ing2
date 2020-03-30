from os import path
from flaskps.db import get_db
from flask import Flask, render_template, g, redirect, url_for, session
from flaskps.helpers.auth import authenticated
from flaskps.resources import user_resource
from flaskps.resources import auth
from flaskps.resources import configuracion

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
app.add_url_rule("/configuration/deactive", 'configuracion_deactive', configuracion.deactive)
app.add_url_rule("/configuration/active", 'configuracion_active', configuracion.active)
app.add_url_rule("/configuration/toggle", 'configuracion_toggleActive', configuracion.toggleActive)
app.add_url_rule("/configuration/edit", 'configuracion_edit', configuracion.editarInformacion, methods=['POST'])
app.add_url_rule("/configuration/edit", 'configuracion_render_edit', configuracion.renderEditarInformacion)

# Usuarios
app.add_url_rule("/usuarios", 'user_resource_index', user_resource.index)
app.add_url_rule("/usuarios", 'user_resource_create', user_resource.create, methods=['POST'])
app.add_url_rule("/config", 'configuracion_changePage', configuracion.changePage, methods=['POST'])
app.add_url_rule("/usuarios/search_by_username", 'user_resource_indexUser', user_resource.indexUser, methods=['POST'])
app.add_url_rule("/usuarios/index_by_active", 'user_resource_indexActive', user_resource.indexActive)
app.add_url_rule("/usuarios/index_by_inactive", 'user_resource_indexInactive', user_resource.indexInactive)
app.add_url_rule("/usuarios/create", 'user_resource_adminCreate', user_resource.adminCreate)
app.add_url_rule("/usuario/new", 'user_resource_new', user_resource.new)
app.add_url_rule("/usuarios/editar/<int:id>", 'user_resource_edit', user_resource.edit)
app.add_url_rule("/usuarios/asignar/<string:user>/<string:rol>", 'user_resource_asignarRol', user_resource.assign)
app.add_url_rule("/usuarios/asignar", 'user_resource_indexAssign', user_resource.indexAssign)
app.add_url_rule("/usuarios/eliminarRol", 'user_resource_indexDeleterol', user_resource.indexDeleteRol)
app.add_url_rule("/usuarios/eliminarRol/<string:user>/<string:rol>", 'user_resource_deleteRol', user_resource.deleteRol)

app.add_url_rule("/editar/<int:id>", 'user_resource_edit2', user_resource.edit2, methods=['POST'])
app.add_url_rule("/usuarios/delete/<int:id>", 'user_resource_delete', user_resource.delete)
app.add_url_rule("/usuarios/active/<int:id>", 'user_resource_active', user_resource.active)



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
     
