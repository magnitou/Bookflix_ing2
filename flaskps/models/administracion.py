class Administracion (object):
    db = None
    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO ciclo_lectivo (fecha_ini, fecha_fin, semestre) VALUES (%s, %s, %s)'
        data = (data.get('fecha_ini'), data.get('fecha_fin'), 1)#(data.get('fecha_ini'), data.get('fecha_fin'), data.get('semestre'))
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    
    @classmethod
    def updateCiclo(cls,data, id):
        sql = 'UPDATE ciclo_lectivo SET fecha_ini = %s, fecha_fin = %s, semestre = %s WHERE id = %s'
        data = (data.get('fecha_ini'), data.get('fecha_fin'), data.get('semestre'), id)
        cursor = cls.db.cursor()
        cursor.execute(sql, (data))
        cls.db.commit()
        return True
    
    @classmethod
    def editHorario(cls, idTaller, idNucleo, dia, id, diaId, nucleoId):
        sql = 'UPDATE taller_nucleo_horario SET nucleo_id = %s, dia = %s WHERE taller_id = %s AND dia = %s AND nucleo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idNucleo, dia, idTaller, diaId, nucleoId))
        cls.db.commit()
        return True

    @classmethod
    def assignHorario(cls, idTaller, idNucleo, dia, id):
        sql = 'INSERT INTO taller_nucleo_horario (taller_id, nucleo_id, dia, lista_id) VALUES (%s, %s, %s, %s)'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTaller, idNucleo, dia, id))
        cls.db.commit()
        return True


    @classmethod
    def get_taller_by_id(cls, id):
        sql = 'SELECT * FROM taller_nucleo_horario inner join taller on taller.id = taller_nucleo_horario.taller_id WHERE taller_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchone()

    @classmethod
    def all(cls):
        sql = 'SELECT * FROM taller'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    @classmethod
    def allNucleosByTaller(cls, idTaller):
        sql = 'SELECT * FROM taller_nucleo_horario inner join (SELECT id as nucleo_id, nombre as nucleo_nombre from nucleo) t on t.nucleo_id = taller_nucleo_horario.nucleo_id where taller_nucleo_horario.taller_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTaller))
        return cursor.fetchall()
    @classmethod
    def allAlumnos(cls, idTaller):
        sql = 'SELECT * FROM estudiante_taller et inner join estudiante e on et.estudiante_id = e.id where et.taller_id = %s '
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTaller))
        return cursor.fetchall()

    @classmethod
    def allPresentes(cls, idLista):
        sql = 'SELECT * FROM presente p inner join estudiante e on p.estudiante_id = e.id where p.lista_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, idLista)
        return cursor.fetchall()

    @classmethod
    def allClases(cls):
        sql = 'SELECT * FROM taller_nucleo_horario'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def allCiclos(cls):
        sql = 'SELECT * FROM ciclo_lectivo'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def allNucleos(cls):
        sql = 'SELECT * FROM nucleo'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def find_ciclo_by_id(cls, id):
        sql = 'SELECT * FROM ciclo_lectivo WHERE id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchone()

    @classmethod
    def get_ciclo(cls, idTaller):
        sql = 'SELECT (ciclo_lectivo_id) FROM ciclo_lectivo_taller WHERE taller_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTaller))
        return cursor.fetchone()

    @classmethod
    def bind_taller_ciclo(cls, idTaller, idCiclo):
        sql = 'INSERT INTO ciclo_lectivo_taller (taller_id, ciclo_lectivo_id) VALUES (%s, %s)'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTaller, idCiclo))
        cls.db.commit()
        return True

    @classmethod
    def delete_taller_ciclo(cls, idTaller, idCiclo):
        sql = ' DELETE FROM ciclo_lectivo_taller WHERE taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idTaller, idCiclo) )
        cls.db.commit()
        return True

    @classmethod
    def delete_ciclo(cls, idCiclo):
        sql = ' DELETE FROM ciclo_lectivo WHERE id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idCiclo) )
        cls.db.commit()
        return True

    

    @classmethod
    def bind_taller_estudiante(cls, idTaller, idEst, idCiclo):
        sql = 'INSERT INTO estudiante_taller (estudiante_id, ciclo_lectivo_id, taller_id) VALUES (%s, %s, %s)'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idEst,idCiclo, idTaller))
        cls.db.commit()
        return True

    @classmethod
    def delete_taller_estudiante(cls, idTaller, idCiclo):
        sql = ' DELETE FROM estudiante_taller WHERE taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idTaller,  idCiclo) )
        cls.db.commit()
        return True

    @classmethod
    def bind_taller_docente(cls, idDoc, idTaller, idCiclo):
        sql = 'INSERT INTO docente_responsable_taller (docente_id, ciclo_lectivo_id, taller_id) VALUES (%s, %s, %s)'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idDoc,idCiclo, idTaller))
        cls.db.commit()
        return True

    @classmethod
    def delete_taller_docente(cls, idTaller, idCiclo):
        sql = ' DELETE FROM docente_responsable_taller WHERE taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idTaller, idCiclo) )
        cls.db.commit()
        return True

    @classmethod
    def estudiante_asignado(cls, idTaller, idEst, idCiclo): # metodos que preguntan si ya estan asignados al curso
        sql = 'SELECT count(estudiante_id) FROM estudiante_taller WHERE estudiante_id = %s AND taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idEst,idTaller, idCiclo) )
        return cursor.fetchone()

    @classmethod
    def docente_asignado(cls, idTaller, idDoc, idCiclo):
        sql = 'SELECT count(docente_id) FROM docente_responsable_taller WHERE docente_id = %s AND taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idDoc,idTaller, idCiclo) )
        return cursor.fetchone()

    @classmethod
    def ciclo_asignado(cls, idTaller, idCiclo):
        sql = 'SELECT count(taller_id) FROM ciclo_lectivo_taller WHERE taller_id = %s AND ciclo_lectivo_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,(idTaller, idCiclo) )
        return cursor.fetchone()
    
    @classmethod
    def taller_nucleo_horario(cls, idTaller, idNucleo, dia):
        sql = 'SELECT count(taller_id) FROM taller_nucleo_horario WHERE taller_id = %s AND nucleo_id = %s AND dia = %s '
        cursor = cls.db.cursor()
        cursor.execute(sql,(idTaller, idNucleo, dia) )
        return cursor.fetchone()