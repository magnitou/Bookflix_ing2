class Docente (object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM docente;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def create(cls,data):
        sql = ' INSERT INTO docente (apellido,nombre, fecha_nac, localidad_id, domicilio,genero_id, tipo_doc_id, numero, tel, activo) VALUES (%s, %s, %s,%s, %s, %s, %s,%s,%s, %s)'
        data = (data.get('apellido'),data.get('nombre'),data.get('fecha_nac'), data.get('localidad_id'),data.get('domicilio'),data.get('genero_id'),data.get('tipo_doc_id'),data.get('numero'),data.get('tel'), 1)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True



    @classmethod
    def find_by_email_and_pass(cls, email, password):
        sql = """
            SELECT * FROM docente AS u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()

    @classmethod
    def find_by_email(cls, email):
        sql = """
            SELECT * FROM docente AS u
            WHERE u.email = %s 
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email))

        return cursor.fetchone()
    @classmethod
    def find_by_apellido(cls, nombre):
        cursor = cls.db.cursor()
        cursor.execute("SELECT * FROM docente AS d WHERE d.apellido LIKE '%s%%'" % apellido)
        usu = cursor.fetchall()
        return usu
    @classmethod
    def find_by_id(cls, id):
        cursor = cls.db.cursor()
        dada = cursor.execute("SELECT * FROM docente AS u WHERE u.id =%s ", str(id))
        return cursor.fetchone()

    @classmethod
    def find_by_active(cls):
        cursor = cls.db.cursor()
        data = cursor.execute("SELECT * FROM docente AS u WHERE u.activo = 1")
        return cursor.fetchall()

    @classmethod
    def  find_by_inactive(cls):
        cursor = cls.db.cursor()
        data = cursor.execute("SELECT * FROM docente AS u WHERE u.activo = 0")
        return cursor.fetchall()

    @classmethod
    def exist(cls,dni):
        sql = 'SELECT count(numero) FROM docente  WHERE numero = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (dni))
        return cursor.fetchone()

    @classmethod
    def update(cls, data, id):
        sql = 'UPDATE docente SET apellido = %s, nombre = %s, fecha_nac = %s, localidad_id = %s, domicilio = %s, genero_id = %s, tipo_doc_id = %s, numero = %s, tel = %s WHERE id = %s;'
        cursor = cls.db.cursor()
        data = (data.get('apellido'),data.get('nombre'),data.get('fecha_nac'), data.get('localidad_id'),data.get('domicilio'),data.get('genero_id'),data.get('tipo_doc_id'),data.get('numero'),data.get('tel'),str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True
        
    @classmethod
    def active (cls, id):
        sql = ' UPDATE docente SET activo = 1 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def delete(cls, id):
        sql = ' UPDATE docente SET activo = 0 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True