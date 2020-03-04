class Genero (object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM genero;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()