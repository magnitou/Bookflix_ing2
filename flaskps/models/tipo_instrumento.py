class Tipo_Instrumento(object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM tipo_instrumento;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()