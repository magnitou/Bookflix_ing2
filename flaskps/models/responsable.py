class Responsable (object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM responsable;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()