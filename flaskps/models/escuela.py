class Escuela(object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM escuela;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()