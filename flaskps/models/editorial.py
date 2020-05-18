class Editorial(object):
    db = None
    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO editorial (nombre) VALUES (%s)'
        data = (data.get('nombre'))
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    #GETS
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM editorial;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM editorial AS u
            WHERE u.nombre = %s 
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (name))
        return cursor.fetchone()
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM editorial AS u
            WHERE u.id = %s 
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchone()