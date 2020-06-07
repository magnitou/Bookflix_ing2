class Novedad(object):
    db = None
    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO novedad (titulo, descripcion) VALUES (%s, %s)'
        data = (data.get('titulo'), data.get('descripcion'))
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    