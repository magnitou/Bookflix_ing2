from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.helpers.auth import authenticated
from flaskps.models.administracion import Administracion
from flaskps.models.configuracion import Configuracion
from flaskps.models.asistencia import Asistencia
from datetime import date


def new():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    return render_template('asistencia/new.html')


def set_db():
    Asistencia.db = get_db()
    Administracion.db = get_db()


def tomar():
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/')
    set_db()
    idLista = request.args.get('id')
    alumnos = Administracion.allAlumnos(idLista)
    print (alumnos)
    i = int(request.args.get('i', 0))
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    today = date.today()
    if (i == -1):
        i = 0
    elif i * pag >= len(alumnos):
        i = i - 1
    return render_template('asistencia/tomarAsistencia.html', alumnos=alumnos, i=i, pag=pag, fecha=today, idLista = idLista)


def ver():
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/')
    set_db()
    lista = request.args.get('id')
    estudiantes = list(map(lambda fullEstudiante : fullEstudiante['estudiante_id'],Administracion.allAlumnos(Asistencia.get_taller_by_lista(lista)['taller_id'])))
    nombres_estudiantes = list (map(lambda fullEstudiante :  fullEstudiante['apellido'] + ", " + fullEstudiante['nombre'],Administracion.allAlumnos(Asistencia.get_taller_by_lista(lista)['taller_id'])))
    presentes = Asistencia.get_presentes_by_lista(lista)
    asistencias = {}
    print ("Los presentes son :" + str(presentes))
    for asistencia in presentes:
        unaFecha = asistencia['fecha']
     #   print (unaFecha)
        if unaFecha in asistencias:
            asistencias[unaFecha].append(asistencia['estudiante_id'])
        else:
            asistencias[unaFecha] = []
            asistencias[unaFecha].append(asistencia['estudiante_id'])
    #print(asistencias)
    fechas = []
    estudiantesPorFecha = []
    allChecked = []
    print(estudiantes)
    print ("Los estudiantes son asi: " + str(estudiantes))
    for fecha, estudiantes_asistencia in asistencias.items():
        fechas.append(fecha)
        estudiantesPorFecha.append(estudiantes_asistencia)
        allChecked.append(list(map(lambda x : x in estudiantes_asistencia, estudiantes)))
    print (allChecked)
    i = int(request.args.get('i', 0))
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    if (i == -1):
        i = 0
    elif i * pag >= len(presentes):
        i = i - 1
    return render_template('asistencia/verAsistencia.html',nombres_estudiantes = nombres_estudiantes,estudiantes = estudiantes,estudiantesPorFecha = estudiantesPorFecha ,allChecked = allChecked, fechas = fechas, presentes=presentes, i=i, pag=pag)


def presente(idLista):
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/')
    set_db()
    
    alumnos = request.form.getlist('alumnosElegidos')
    fecha = request.form['fecha']
    if alumnos is not None:
        for alumno in alumnos:
            #if (Asistencia.validate_alumno(alumno, fecha)==0):
                Asistencia.presente(fecha, alumno, idLista)
        flash("Presentes cargados correctamente")
    else:
        flash("Parece que no hay alumnos cargados a este taller")
        
    return redirect(url_for('asistencia_index'))



def index():
    if not authenticated(session):
        flash("No puede ingresar sin iniciar sesion")
        return redirect('/')
    set_db()
    i = int(request.args.get('i', 0))
    Configuracion.db = get_db()
    pag = Configuracion.get_page_size()
    listados = Asistencia.all()
    if (i == -1):
        i = 0
    elif (i * pag >= len(listados)):
        i = i - 1
    url = request.path
    adm = 'configuracion_usarInhabilitado' in session['permisos']
    return render_template('asistencia/index.html', listados=listados, i=i, pag=pag, url=url, adm=adm)
