from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero

class Book(object):
    db = None
    @classmethod
    def create(cls, data, files,isbn):
        sql = ' INSERT INTO libro (isbn, archivo, available_from, available_to) VALUES (%s, %s, %s,%s)'
        data = (isbn,files['archivo'].filename,data.get('available_from'),data.get('available_to') if data.get('available_to')!='' else None)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    
    @classmethod
    def loadMeta(cls, data,id_autor, id_editorial, id_genero):
        sql = 'INSERT INTO metadato (isbn, titulo, autor_id, sinopsis, editorial_id, genero_id) VALUES (%s, %s, %s, %s,%s, %s)'
        data = (data.get('isbn'), data.get('titulo'), id_autor, data.get('sinopsis'), id_editorial, id_genero)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def updateMeta(cls, data, isbn, autor_id, editorial_id, genero_id):
        sql = 'UPDATE metadato SET titulo = %s, autor_id = %s, sinopsis = %s, editorial_id = %s, genero_id = %s WHERE isbn = %s '
        data = (data.get('titulo'), autor_id, data.get('sinopsis'), editorial_id, genero_id, isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def deleteMeta(cls, isbn):
        sql = "DELETE FROM metadato WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, isbn)
        cls.db.commit()
        return True
    #GETS
    @classmethod     
    def allMeta(cls):
        sql = 'SELECT * FROM metadato'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        metas = cursor.fetchall()
        for meta in metas:
            meta['autor_id'] = Autor.find_by_id(meta['autor_id'])['nombre']
            meta['editorial_id'] = Editorial.find_by_id(meta['editorial_id'])['nombre']
            meta['genero_id'] = Genero.find_by_id(meta['genero_id'])['nombre']
        return metas

    @classmethod
    def find_by_isbn(cls, isbn):
        sql = 'SELECT * FROM libro WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        return cursor.fetchone()

    @classmethod
    def find_meta_by_isbn(cls, isbn):
        sql = 'SELECT * FROM metadato WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        return cursor.fetchone()