class Instrumento(object):
    db = None
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM instrumento inner join (SELECT id as tipo_instrumento_id, nombre as tipo_instrumento_nombre from tipo_instrumento) t on t.tipo_instrumento_id = instrumento.tipo_id where activo = 1 '
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def create(cls, data, files):
        sql = ' INSERT INTO instrumento(id,nombre, tipo_id,imagen,activo) VALUES (%s,%s,%s,%s,%s)'
        print (files)
        data = (data.get('id_instrumento'),data.get('nombre'),data.get('tipo_id'),files['imagen'].filename,1)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True  
    
    @classmethod
    def delete(cls, id):
        sql = ' UPDATE instrumento SET activo = 0 where id = %s'
        cursor = cls.db.cursor()
        data = (str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    
    @classmethod
    def find_by_id(cls, id):
        cursor = cls.db.cursor()
        dada = cursor.execute("SELECT * FROM instrumento AS i WHERE i.id =%s and i.activo = 1", str(id))
        return cursor.fetchone()

    @classmethod
    def get_filename(cls, id):
        sql = 'SELECT imagen FROM instrumento where instrumento.id = %s AND instrumento.activo = 1'
        cursor = cls.db.cursor()
        cursor.execute(sql, str(id))
        return cursor.fetchone()['imagen']

    @classmethod
    def validate_instrumento(cls, id):
        sql = 'SELECT * FROM instrumento as i where i.id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql,str(id))
        return cursor.fetchall()
    
    @classmethod
    def update(cls,data, filename, id):
        sql = 'UPDATE instrumento SET id = %s, nombre = %s, tipo_id = %s, imagen = %s WHERE id = %s;'
        cursor = cls.db.cursor()
        data = (data.get('id'),data.get('nombre'), data.get('tipo_instrumento'),filename, id)
        cursor.execute(sql, data)
        cls.db.commit()
        return True