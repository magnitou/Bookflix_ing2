class Nivel (object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM nivel;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()