class Permit(object):
    db = None
    @classmethod
    def get_permits(cls, user):
        permits = []
        iduser = user['id']
        sql = "SELECT rol_id FROM usuario_tiene_rol WHERE usuario_id = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (iduser))
        rols = cursor.fetchall()
        for idrol in rols:
            sql = "SELECT permiso_id FROM rol_tiene_permiso WHERE rol_id = %s" 
            cursor.execute(sql, (idrol['rol_id']))
            for perm in cursor.fetchall():
                sql = "SELECT nombre FROM permiso WHERE id = %s" 
                cursor.execute(sql, (perm['permiso_id']))
                permits.append(cursor.fetchone()['nombre'])
        return permits
