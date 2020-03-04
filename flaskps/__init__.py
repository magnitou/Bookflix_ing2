from os import path
from flaskps.db import get_db
from flask import Flask, render_template, g, redirect, url_for, session
from flaskps.helpers.auth import authenticated
from flaskps.resources import user_resource
from flaskps.resources import auth
from flaskps.resources import instrumento
from flaskps.resources import configuracion
from flaskps.resources import docente
from flaskps.resources import estudiante
from flaskps.resources import administracion
from flaskps.resources import asistencia
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

# Asistencia
app.add_url_rule("/asistencia", 'asistencia_index', asistencia.index)
app.add_url_rule("/asistencia/presente<int:idLista>", 'asistencia_presente', asistencia.presente, methods=['POST'])
app.add_url_rule("/asistencia/tomarAsistencia", 'asistencia_tomarAsistencia', asistencia.tomar)
app.add_url_rule("/asistencia/verAsistencia", 'asistencia_verAsistencia', asistencia.ver)




#Instrumento
app.add_url_rule("/instrumentos/new", 'instrumento_new', instrumento.new)
app.add_url_rule("/instrumentos", 'instrumento_index', instrumento.index)
app.add_url_rule("/instrumentos/editar/<int:id>", 'instrumento_edit', instrumento.edit)
app.add_url_rule("/instrumentos/editar/<int:id>", 'instrumento_submitEdit', instrumento.submitEdit, methods=['POST'])
app.add_url_rule("/instrumentos/search_by_active", 'instrumento_searchActive', instrumento.searchActive)
app.add_url_rule("/instrumentos/index_by_active", 'instrumento_indexActive', instrumento.indexActive)
app.add_url_rule("/instrumentos/index_by_inactive", 'instrumento_indexInactive', instrumento.indexInactive)
app.add_url_rule("/instrumentos/active/<int:id>", 'instrumento_active', instrumento.active)
app.add_url_rule("/instrumentos/crear", 'instrumento_create', instrumento.create, methods=['POST'])
app.add_url_rule("/instrumentos/delete/<int:id>", 'instrumento_delete', instrumento.delete)


# Estudiante
app.add_url_rule("/estudiantes/crear", 'estudiante_create', estudiante.create, methods=['POST'])
app.add_url_rule("/estudiantes/new", 'estudiante_new', estudiante.new, methods=['GET', 'POST'])
app.add_url_rule("/estudiantes/editar/<int:id>", 'estudiante_edit', estudiante.edit)
app.add_url_rule("/estudiantes/editar/<int:id>", 'estudiante_submitEdit', estudiante.submitEdit, methods=['POST'])
app.add_url_rule("/estudiantes", 'estudiante_index', estudiante.index)
app.add_url_rule("/estudiantes/delete/<int:id>", 'estudiante_delete', estudiante.delete)
app.add_url_rule("/estudiantes/search_by_active", 'estudiante_searchActive', estudiante.searchActive)
app.add_url_rule("/estudiantes/index_by_active", 'estudiante_indexActive', estudiante.indexActive)
app.add_url_rule("/estudiantes/index_by_inactive", 'estudiante_indexInactive', estudiante.indexInactive)
app.add_url_rule("/estudiantes/active/<int:id>", 'estudiante_active', estudiante.active)

# Docente
app.add_url_rule("/docentes/new", 'docente_new', docente.new, methods=['POST'])
app.add_url_rule("/docentes/create", 'docente_create', docente.create)
app.add_url_rule("/edit/<int:id>", 'docente_edit', docente.edit, methods=['POST'])
app.add_url_rule("/docentes", 'docente_index', docente.index)
app.add_url_rule("/docentes/delete/<int:id>", 'docente_delete', docente.delete)
app.add_url_rule("/docentes/index_by_active", 'docente_indexActive', docente.indexActive)
app.add_url_rule("/docentes/index_by_inactive", 'docente_indexInactive', docente.indexInactive)
app.add_url_rule("/docente/active/<int:id>", 'docente_active', docente.active)
app.add_url_rule("/editar/<int:id>", 'docente_update', docente.update)


# Administracion
app.add_url_rule("/administracion", "administracion_index", administracion.index)
app.add_url_rule("/administracionCiclos", "administracion_indexCiclos", administracion.indexCiclos)
app.add_url_rule("/administracionCiclosUpdate/<int:id>", "administracion_updateCiclos", administracion.updateCiclo)
app.add_url_rule("/administracionCiclosUpdate/<int:id>", "administracion_editCiclos", administracion.editCiclo, methods=['POST'])
app.add_url_rule("/administracionCiclosDelete/<int:id>", "administracion_deleteCiclos", administracion.deleteCiclo)
app.add_url_rule("/administracion/new", 'administracion_new', administracion.new, methods=['POST'])
app.add_url_rule("/administracion/create", 'administracion_create', administracion.create)
app.add_url_rule("/administracion/asignar_ciclo", "administracion_assignCiclo", administracion.assignCiclo)
app.add_url_rule("/administracion/asignar/<int:id>", "administracion_showAll", administracion.showAll)
app.add_url_rule("/administracion/asignarHorario/<int:id>", "administracion_showHorario", administracion.showHorario)
app.add_url_rule("/administracion/editHorario/<int:id>", "administracion_editHorario", administracion.editHorario)
app.add_url_rule("/administracion/editHorarios/<int:id>", "administracion_editHorarios", administracion.editHorarios)
app.add_url_rule("/administracion/editHorario/<int:id>/<string:diaId>/<int:nucleoId>", "administracion_submitEditHorario", administracion.submitEditHorario, methods=['POST'])
app.add_url_rule("/administracion/update/<int:id>", "administracion_updateAll", administracion.updateAll, methods=['POST'])
app.add_url_rule("/administracion/updateHorario/<int:id>", "administracion_updateHorario", administracion.updateHorario, methods=['POST'])


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

app.add_url_rule("/img/<int:inst_id>", 'instrumento_serve_image', instrumento.serve_image)

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
     
