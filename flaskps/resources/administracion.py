from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.models.administracion import Administracion
from flaskps.models.asistencia import Asistencia
from flaskps.models.configuracion import Configuracion
from flaskps.models.estudiante import Estudiante
from flaskps.models.docente import Docente
from flaskps.helpers.auth import authenticated
from flaskps.resources.api import calls
from flaskps.helpers.administracion import dia_semana
import datetime


def create():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    return render_template('administracion/new.html')

def new():
    if 'lectivo_new' not in session['permisos']:
        flash("No tiene permisos para crear un nuevo ciclo lectivo")
        return redirect(url_for('administracion_index'))
    set_db()
    Administracion.create(request.form)
    flash('Ciclo Lectivo Creado')
    return redirect(url_for('administracion_indexCiclos'))

def index():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    talleres = Administracion.all()
    clases = Administracion.allClases()
    permit = 'lectivo_index' in session['permisos']
    permitNew = 'lectivo_new' in session['permisos']
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i = 0
    elif (i * pag >= len(talleres)):
        i = i - 1
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template("administracion/index.html", clases=clases, talleres=talleres, permitIndex=permit,
                           permitNew=permitNew,
                           adm=adm, i=i, pag=pag)

def indexCiclos():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    ciclos = Administracion.allCiclos()
    permit = 'lectivo_index' in session['permisos']
    permitNew = 'lectivo_new' in session['permisos']
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i = 0
    elif (i * pag >= len(ciclos)):
        i = i - 1
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template("administracion/indexCiclos.html", ciclos=ciclos, permitIndex=permit, adm=adm,
                           permitNew=permitNew, i=i, pag=pag)

def is_estudiante_asigned(idTaller, idEstudiante, idCiclo=1):
    return Administracion.estudiante_asignado(idTaller, idEstudiante, idCiclo).get('count(estudiante_id)') == 1

def is_docente_asigned(idTaller, idDocente, idCiclo=1):
    return Administracion.docente_asignado(idTaller, idDocente, idCiclo).get('count(docente_id)') == 1

def is_ciclo_asigned(idTaller, ciclos):
    are = False
    for ciclo in ciclos:
       are = are or (Administracion.ciclo_asignado(idTaller,ciclo['id']).get('count(taller_id)') == 1)
    return are

def get_ciclo(idTaller):
    return Administracion.get_ciclo(idTaller)

def showAll(id):    #Mostras todos los semestres en un select y los estudiants y docents en un checklist
    set_db()
    Estudiante.db = get_db()
    Docente.db = get_db()
    estudiantes = Estudiante.all()
    docentes = Docente.all()
    ciclos = Administracion.allCiclos()
    adm = "configuracion_usarInhabilitado" in session['permisos']
    if is_ciclo_asigned(id, ciclos):
        oldCiclo = get_ciclo(id)['ciclo_lectivo_id']
        asigsCiclos = list(map(lambda ciclo: oldCiclo == ciclo['id'], ciclos)) 
        asigsEstudiantes = list(map(lambda est: is_estudiante_asigned(id, est['id'], oldCiclo), estudiantes)) #Pones un true si ya estaba asignado a ese taller y ese ciclo, esta hardcodeado el ciclo 1
        asigsDocentes = list(map(lambda doc: is_docente_asigned(id, doc['id'], oldCiclo), docentes))
    else:
        asigsCiclos = list(map(lambda ciclo: False, ciclos)) 
        asigsEstudiantes = list(map(lambda est: False, estudiantes)) #Pones un true si ya estaba asignado a ese taller y ese ciclo, esta hardcodeado el ciclo 1
        asigsDocentes = list(map(lambda doc: False, docentes))
    return render_template('administracion/assign.html', estudiantes=estudiantes, docentes=docentes,
                           asigsEstudiantes=asigsEstudiantes, asigsDocentes=asigsDocentes, ciclos=ciclos, idTaller=id,
                           asigsCiclos=asigsCiclos, adm=adm)

def showHorario(id):
    set_db()
    if 'horario_update' not in session['permisos']:
        flash("No tiene permisos para asignar horario a un taller")
        return redirect(url_for('administracion_index'))
    crudes = calls.get_feriados()
    ciclo_crude = Administracion.get_ciclo(id)
    if ciclo_crude is None:
        flash("  asignarle un ciclo al taller antes de asignar un horario")
        return redirect(url_for('administracion_index'))
    ciclo = Administracion.find_ciclo_by_id(ciclo_crude['ciclo_lectivo_id'])
    a = ciclo['fecha_ini'].date()
    b = ciclo['fecha_fin'].date()
    feriadosEnFechaInicio = list(filter(lambda date: a <= datetime.datetime.strptime(date, "%Y-%m-%d").date() <=b ,map(lambda item:  (item['inicio']), crudes)))
    feriadosEnFechaFin = list(filter(lambda date: a <= datetime.datetime.strptime(date[0], "%Y-%m-%d").date() <=b ,map(lambda item:  (item['fin'], item['nombre']), crudes)))
    feriadosInicioFin = list(zip(list(map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").date().weekday(), feriadosEnFechaInicio)), list(map(lambda date: (datetime.datetime.strptime(date[0], "%Y-%m-%d").date().weekday()), feriadosEnFechaFin)), list(map(lambda date: date[1], feriadosEnFechaFin))))
    cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado = 0,0,0,0,0,0
    feriadosDias=[[],[],[],[],[],[]]
    for feriado in feriadosInicioFin:
        ini, fin = feriado[0], feriado[1]
        if (0 in range(ini, fin)):
            cantLunes +=1
            feriadosDias[0].append(feriado[2])
        if (1 in range(ini, fin)):
            cantMartes +=1
            feriadosDias[1].append(feriado[2])
        if (2 in range(ini, fin)):
            cantMiercoles +=1
            feriadosDias[2].append(feriado[2])
        if (3 in range(ini, fin)):
            cantJueves +=1
            feriadosDias[3].append(feriado[2])
        if (4 in range(ini, fin)):
            cantViernes +=1
            feriadosDias[4].append(feriado[2])
        if (5 in range(ini, fin)):
            cantSabado +=1
            feriadosDias[5].append(feriado[2])
    cantidades = [cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado]
    nucleos = Administracion.allNucleos()
    adm = "configuracion_usarInhabilitado" in session['permisos']
    return render_template('administracion/assignHorario.html', id = id, nucleos = nucleos, adm = adm, cantFeriados = cantidades, feriados = feriadosDias)

def editHorario(id):
    set_db()
    print(id)
    if 'horario_update' not in session['permisos']:
        flash("No tiene permisos para asignar horario a un taller")
        return redirect(url_for('administracion_index'))
    crudes = calls.get_feriados()
    ciclo_crude = Administracion.get_ciclo(id)
    if ciclo_crude is None:
        flash("Debe asignarle un ciclo al taller antes de asignar un horario")
        return redirect(url_for('administracion_index'))
    ciclo = Administracion.find_ciclo_by_id(ciclo_crude['ciclo_lectivo_id'])
    a = ciclo['fecha_ini'].date()
    b = ciclo['fecha_fin'].date()
    feriadosEnFechaInicio = list(filter(lambda date: a <= datetime.datetime.strptime(date, "%Y-%m-%d").date() <=b ,map(lambda item:  (item['inicio']), crudes)))
    feriadosEnFechaFin = list(filter(lambda date: a <= datetime.datetime.strptime(date[0], "%Y-%m-%d").date() <=b ,map(lambda item:  (item['fin'], item['nombre']), crudes)))
    feriadosInicioFin = list(zip(list(map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").date().weekday(), feriadosEnFechaInicio)), list(map(lambda date: (datetime.datetime.strptime(date[0], "%Y-%m-%d").date().weekday()), feriadosEnFechaFin)), list(map(lambda date: date[1], feriadosEnFechaFin))))
    cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado = 0,0,0,0,0,0
    feriadosDias=[[],[],[],[],[],[]]
    for feriado in feriadosInicioFin:
        ini, fin = feriado[0], feriado[1]
        if (0 in range(ini, fin)):
            cantLunes +=1
            feriadosDias[0].append(feriado[2])
        if (1 in range(ini, fin)):
            cantMartes +=1
            feriadosDias[1].append(feriado[2])
        if (2 in range(ini, fin)):
            cantMiercoles +=1
            feriadosDias[2].append(feriado[2])
        if (3 in range(ini, fin)):
            cantJueves +=1
            feriadosDias[3].append(feriado[2])
        if (4 in range(ini, fin)):
            cantViernes +=1
            feriadosDias[4].append(feriado[2])
        if (5 in range(ini, fin)):
            cantSabado +=1
            feriadosDias[5].append(feriado[2])
    cantidades = [cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado]
    nucleos = Administracion.allNucleos()
    adm = "configuracion_usarInhabilitado" in session['permisos']
    """
    ciclo_crude = Administracion.get_ciclo(id)
    if ciclo_crude is None:
        flash("Debe asignarle un ciclo al taller antes de asignar un horario")
        return redirect(url_for('administracion_index'))
    """
    #ACA HAY UN PROBLEMA PORQUE PUEDO TENER VARIAS ASIGNACIONES
    taller = Administracion.get_taller_by_id(id)
    diaSeleccionado = taller['dia']
    nucleoSeleccionado = taller['nucleo_id']
    return render_template('administracion/editarHorario.html', id = id, nucleos = nucleos, adm = adm, cantFeriados = cantidades, feriados = feriadosDias, prevDia = diaSeleccionado, prevNucleo = nucleoSeleccionado)

def editHorarios(id):
    set_db()
    if 'horario_update' not in session['permisos']:
        flash("No tiene permisos para asignar horario a un taller")
        return redirect(url_for('administracion_index'))
    crudes = calls.get_feriados()
    ciclo_crude = Administracion.get_ciclo(id)
    if ciclo_crude is None:
        flash("Debe asignarle un ciclo al taller antes de asignar un horario")
        return redirect(url_for('administracion_index'))
    ciclo = Administracion.find_ciclo_by_id(ciclo_crude['ciclo_lectivo_id'])
    a = ciclo['fecha_ini'].date()
    b = ciclo['fecha_fin'].date()
    feriadosEnFechaInicio = list(filter(lambda date: a <= datetime.datetime.strptime(date, "%Y-%m-%d").date() <=b ,map(lambda item:  (item['inicio']), crudes)))
    feriadosEnFechaFin = list(filter(lambda date: a <= datetime.datetime.strptime(date[0], "%Y-%m-%d").date() <=b ,map(lambda item:  (item['fin'], item['nombre']), crudes)))
    feriadosInicioFin = list(zip(list(map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").date().weekday(), feriadosEnFechaInicio)), list(map(lambda date: (datetime.datetime.strptime(date[0], "%Y-%m-%d").date().weekday()), feriadosEnFechaFin)), list(map(lambda date: date[1], feriadosEnFechaFin))))
    cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado = 0,0,0,0,0,0
    feriadosDias=[[],[],[],[],[],[]]
    for feriado in feriadosInicioFin:
        ini, fin = feriado[0], feriado[1]
        if (0 in range(ini, fin)):
            cantLunes +=1
            feriadosDias[0].append(feriado[2])
        if (1 in range(ini, fin)):
            cantMartes +=1
            feriadosDias[1].append(feriado[2])
        if (2 in range(ini, fin)):
            cantMiercoles +=1
            feriadosDias[2].append(feriado[2])
        if (3 in range(ini, fin)):
            cantJueves +=1
            feriadosDias[3].append(feriado[2])
        if (4 in range(ini, fin)):
            cantViernes +=1
            feriadosDias[4].append(feriado[2])
        if (5 in range(ini, fin)):
            cantSabado +=1
            feriadosDias[5].append(feriado[2])
    cantidades = [cantLunes, cantMartes, cantMiercoles, cantJueves, cantViernes, cantSabado]
    nucleos = Administracion.allNucleos()
    adm = "configuracion_usarInhabilitado" in session['permisos']
    ciclo_crude = Administracion.get_ciclo(id)
    if Administracion.allNucleosByTaller(id) == ():
        flash("Debe asignarle un ciclo al taller antes de asignar un horario")
        return redirect(url_for('administracion_index'))
    #ACA HAY UN PROBLEMA PORQUE PUEDO TENER VARIAS ASIGNACIONES
    taller = Administracion.get_taller_by_id(id)
    diaSeleccionado = taller['dia']
    nucleoSeleccionado = taller['nucleo_id']
    talleres = Administracion.allNucleosByTaller(id)
    return render_template('administracion/editarHorarios.html', taller = taller, talleres = talleres, adm = adm, cantFeriados = cantidades, feriados = feriadosDias, prevDia = diaSeleccionado, prevNucleo = nucleoSeleccionado)


def assignCiclo(idTaller, idCiclo):
    Administracion.bind_taller_ciclo(idTaller, idCiclo)
    flash("Se asocio el taller NOMBRE al ciclo FECHAiN FECHAFIN")
    return True

def assignEstudiante(idTaller, idEstudiante, idCiclo):
    Administracion.bind_taller_estudiante(idTaller, idEstudiante, idCiclo)
    return True

def assignDocente(idTaller, idDocente, idCiclo):
    Administracion.bind_taller_docente(idDocente,idTaller, idCiclo)
    return True

def assignHorario(idTaller, idNucleo, idCiclo):
    return True


def deleteCiclo_taller(idTaller, idCiclo):
    Administracion.delete_taller_ciclo(idTaller, idCiclo)
    return True

def resetear_tabla(idTaller, oldCiclo):
    Administracion.delete_taller_docente(idTaller, oldCiclo)
    Administracion.delete_taller_estudiante(idTaller, oldCiclo)
    return True

def updateAll(id):
    estudiantesElegidos = request.form.getlist('estudiantesElegidos')
    docentesElegidos = request.form.getlist('docentesElegidos')
    idCiclo = request.form['semestre']
    ciclos = Administracion.allCiclos()
    if is_ciclo_asigned(id, ciclos):
        oldCiclo = get_ciclo(id)['ciclo_lectivo_id']
        deleteCiclo_taller(id, oldCiclo)
        resetear_tabla(id, oldCiclo)
    assignCiclo(id, idCiclo)
    for i in range(len(estudiantesElegidos)):
        assignEstudiante(id, estudiantesElegidos[i], idCiclo)#Y lo escribo de vuelta, aunque sean los mismos datos

    for i in range(len(docentesElegidos)):
        assignDocente(id, docentesElegidos[i], idCiclo)
    flash("Asignacion exitosa")
    return redirect(url_for('administracion_index'))

def updateHorario(id):    
    nucleo = request.form['nucleo']
    dia = request.form['dia']
    print(validate_taller_nucleo_day(id,nucleo,dia))
    if validate_taller_nucleo_day(id,nucleo,dia):
        idLista = Asistencia.create()
        Administracion.assignHorario(id, nucleo, dia, idLista)
        flash("Horario modificado con éxito")
    else:
        flash("No se puede modificar el horario, ya existe un taller en un nucleo para ese dia")
    return redirect(url_for('administracion_index'))

def submitEditHorario(id, diaId, nucleoId):
    nucleo = request.form['nucleo']
    dia = request.form['dia']
    print(validate_taller_nucleo_day(id,nucleo,dia))
    if validate_taller_nucleo_day(id,nucleo,dia):
        Administracion.editHorario(id, nucleo, dia, id, diaId, nucleoId)
        flash("Horario modificado con éxito")
    else:
        flash("No se puede modificar el horario, ya existe un taller en un nucleo para ese dia")
    return redirect(url_for('administracion_index'))

def editCiclo(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('/'))
    if 'lectivo_update' not in session['permisos']:
        flash("No tiene permisos para editar un ciclo")
        return redirect(url_for('administracion_indexCiclos'))
    set_db()
    Administracion.updateCiclo(request.form,id)
    return redirect(url_for('administracion_indexCiclos'))

def updateCiclo(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('/'))
    if 'lectivo_update' not in session['permisos']:
        flash("No tiene permisos para editar un ciclo")
        return redirect(url_for('administracion_indexCiclos'))
    set_db()
    ciclo = Administracion.find_ciclo_by_id(id)
    ciclo['fecha_ini'] = ciclo['fecha_ini'].date()
    ciclo['fecha_fin'] = ciclo['fecha_fin'].date()
    return render_template('administracion/edit.html', ciclo = ciclo)

def deleteCiclo(id):
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect(url_for('/'))
    if 'lectivo_destroy' not in session['permisos']:
        flash("No tiene permisos para eliminar un ciclo")
        return redirect(url_for('administracion_indexCiclos'))
    set_db()
    talleres = Administracion.all()
    for taller in talleres:
        Administracion.delete_taller_docente(taller['id'], id)
        Administracion.delete_taller_estudiante(taller['id'], id)
        Administracion.delete_taller_ciclo(taller['id'], id)

    Administracion.delete_ciclo(id)    
    return redirect(url_for('administracion_indexCiclos'))

def set_db():
    Administracion.db = get_db()
    Asistencia.db = get_db()

def validate_taller_nucleo_day(id, nucleo, dia):
    set_db()
    return Administracion.taller_nucleo_horario(id, nucleo, dia)['count(taller_id)'] == 0

