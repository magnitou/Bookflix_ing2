class Trailer(object):
    db = None
    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO trailer (titulo, archivo) VALUES (%s, %s)'
        data = (data.get('titulo'), data.get('descripcion'))
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    