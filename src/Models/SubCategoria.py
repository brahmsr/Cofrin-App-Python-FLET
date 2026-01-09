from Context.DbContext import DbContext

class Subcategoria:
    def __init__(self, nome, categoria_id, usuario_id, descricao="", id=None, icone="", cor=""):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.icone = icone
        self.cor = cor
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id
        
    # ------------------ CRUD ------------------ #
    def save(self): 
        db = DbContext()
        cursor = db.get_connection().cursor()
        
        if self.id is None:
            sql = 'INSERT INTO subcategorias (nome, descricao, categoria_id, usuario_id, icone, cor) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(sql, (self.nome, self.descricao, self.categoria_id, self.usuario_id, self.icone, self.cor))
            self.id = cursor.lastrowid
        else:
            sql = 'UPDATE subcategorias SET nome = ?, descricao = ?, categoria_id = ?, usuario_id = ?, icone = ?, cor = ? WHERE id = ?'
            cursor.execute(sql, (self.nome, self.descricao, self.categoria_id, self.usuario_id, self.icone, self.cor, self.id))
            
        db.get_connection().commit()
        db.close_connection()
        
    def delete(self):
        if self.id is not None:
            db = DbContext()
            sql = 'DELETE FROM subcategorias WHERE id = ?'
            db.get_connection().cursor().execute(sql, (self.id,))
            db.get_connection().commit()
            db.close_connection()
            
    # ------------------ Métodos de Busca ------------------ #
    @classmethod
    def find_by_id(cls, subcat_id):
        db = DbContext()
        sql = 'SELECT * FROM subcategorias WHERE id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (subcat_id,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(nome=row['nome'], categoria_id=row['categoria_id'], usuario_id=row['usuario_id'], 
                      descricao=row['descricao'], id=row['id'], icone=row['icone'], cor=row['cor'])
        return None

    @classmethod
    def find_all_by_usuario_id(cls, usuario_id):
        db = DbContext()
        sql = 'SELECT * FROM subcategorias WHERE usuario_id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(nome=row['nome'], categoria_id=row['categoria_id'], usuario_id=row['usuario_id'], 
                   descricao=row['descricao'], id=row['id'], icone=row['icone'], cor=row['cor']) for row in rows]

