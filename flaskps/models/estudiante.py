

class Estudiante(object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM estudiante;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def find_by_dni(cls, dni):
        sql = 'SELECT * FROM estudiante WHERE numero = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (dni))
        return cursor.fetchone()

    @classmethod
    def find_by_apellido(cls, apellido):
        sql = 'SELECT * FROM estudiante WHERE apellido LIKE %s%'
        cursor = cls.db.cursor()
        cursor.execute(sql, (apellido))
        return cursor.fetchall()
    
    @classmethod
    def find_by_id(cls, id):
        cursor = cls.db.cursor()
        dada = cursor.execute("SELECT * FROM estudiante AS u WHERE u.id =%s ", str(id))
        return cursor.fetchone()

    @classmethod
    def find_by_active(cls):
        sql = 'SELECT * FROM estudiante AS e WHERE e.activo = 1'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
        
    @classmethod
    def find_by_inactive(cls):
        sql = 'SELECT * FROM estudiante AS e WHERE e.activo = 0'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO estudiante (apellido, nombre, fecha_nac, lugar_nacimiento,localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero,responsable, tel, barrio_id, activo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s)'
        data = (data.get('apellido'),data.get('nombre'),data.get('fecha_nac'),data.get('lugar_nacimiento'),data.get('localidad_id'),data.get('nivel_id'),data.get('domicilio'),data.get('genero_id'),data.get('escuela_id'),data.get('tipo_doc_id'),data.get('numero'),data.get('responsable'),data.get('tel'),data.get('barrio_id'),1)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True    

    @classmethod
    def update(cls,data, id):
        sql = 'UPDATE estudiante SET apellido = %s, nombre = %s, fecha_nac = %s, lugar_nacimiento = %s, localidad_id = %s, nivel_id = %s, domicilio = %s, genero_id = %s, escuela_id = %s, tipo_doc_id = %s, numero = %s,responsable = %s, tel = %s, barrio_id = %s WHERE id = %s;'
        cursor = cls.db.cursor()
        data = (data.get('apellido'),data.get('nombre'), data.get('fecha_nac'),data.get('lugar_nacimiento'),data.get('localidad_id'),data.get('nivel_id'), data.get('domicilio'), data.get('genero_id'), data.get('escuela_id'), data.get('tipo_doc_id'), data.get('numero'), data.get('responsable'),data.get('tel'), data.get('barrio_id'), id)
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    
    @classmethod
    def delete(cls, id):
        sql = ' UPDATE estudiante SET activo = 0 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def active (cls, id):
        sql = ' UPDATE estudiante SET activo = 1 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    