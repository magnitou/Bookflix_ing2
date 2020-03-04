class Barrio (object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM barrio;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()