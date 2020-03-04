class Asistencia(object):
    db = None

    @classmethod
    def all(cls):
        sql = 'SELECT t.lista_id as lista, t.dia as dia, ta.nombre as taller, n.nombre as nucleo FROM (taller_nucleo_horario t inner join taller ta on t.taller_id = ta.id) inner join nucleo n on t.nucleo_id = n.id'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def create(cls):
        sql = 'INSERT INTO lista(id) VALUES (NULL)'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        cls.db.commit()
        return cursor.lastrowid

    @classmethod
    def presente(cls, fecha, alumno, lista):
        sql = ' INSERT INTO presente (fecha,estudiante_id,lista_id) VALUES (%s, %s, %s)'
        cursor = cls.db.cursor()
        cursor.execute(sql, (fecha, alumno, lista))
        cls.db.commit()
        return True



    @classmethod
    def delete(cls, id):
        sql = ' UPDATE instrumento SET activo = 0 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def find_by_id(cls, id):
        cursor = cls.db.cursor()
        dada = cursor.execute("SELECT * FROM instrumento AS i WHERE i.id =%s and i.activo = 1", str(id))
        return cursor.fetchone()

    @classmethod
    def allEstudiantes(cls, idLista):
        sql = 'SELECT * FROM alumno WHERE lista_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idLista))
        return cursor.fetchall()

    @classmethod
    def get_presentes_by_lista(cls, idLista):
        sql = 'SELECT * FROM presente WHERE lista_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idLista))
        return cursor.fetchall()

    @classmethod    
    def get_taller_by_lista(cls, idLista):
        sql = 'SELECT (taller_id) FROM taller_nucleo_horario WHERE lista_id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idLista))
        return cursor.fetchone()


    @classmethod
    def validate_alumno(cls, fecha, alumno):
        sql = 'SELECT count(estudiante_id) FROM presente AS p WHERE p.estudiante_id = %s AND p.fecha = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (alumno, fecha))        
        return cursor.fetchone()



    @classmethod
    def update(cls, data, filename, id):
        sql = 'UPDATE instrumento SET id = %s, nombre = %s, tipo_id = %s, imagen = %s WHERE id = %s;'
        cursor = cls.db.cursor()
        data = (data.get('id'), data.get('nombre'), data.get('tipo_instrumento'), filename, id)
        cursor.execute(sql, data)
        cls.db.commit()
        return True
