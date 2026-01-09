from Context.DbContext import DbContext

class Categoria:
    def __init__(self, nome, usuario_id, descricao="", icone="", cor="", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.icone = icone
        self.cor = cor

    # ------------------ CRUD ------------------ #
    def save(self):
        """
        Salva a categoria no banco de dados (INSERT ou UPDATE).
        """
        db = DbContext()
        cursor = db.get_connection().cursor()
        
        if self.id is None:
            sql = 'INSERT INTO categorias (nome, descricao, icone, cor, usuario_id) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(sql, (self.nome, self.descricao, self.icone, self.cor, self.usuario_id))
            self.id = cursor.lastrowid
        else:
            sql = 'UPDATE categorias SET nome = ?, descricao = ?, icone = ?, cor = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?'
            cursor.execute(sql, (self.nome, self.descricao, self.icone, self.cor, self.id))
            
        db.get_connection().commit()
        db.close_connection()

    def delete(self):
        """
        Deleta a categoria do banco de dados.
        """
        if self.id is not None:
            db = DbContext()
            sql = 'DELETE FROM categorias WHERE id = ?'
            db.get_connection().cursor().execute(sql, (self.id,))
            db.get_connection().commit()
            db.close_connection()

    # ------------------ Métodos de Busca ------------------ #
    @classmethod
    def find_by_id(cls, cat_id):
        """
        Encontra uma categoria pelo seu ID.
        """
        db = DbContext()
        sql = 'SELECT * FROM categorias WHERE id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (cat_id,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(nome=row['nome'], usuario_id=row['usuario_id'], descricao=row['descricao'], 
                      icone=row['icone'], cor=row['cor'], id=row['id'])
        return None

    @classmethod
    def find_all_by_usuario_id(cls, usuario_id):
        """
        Encontra todas as categorias de um usuário específico.
        Retorna uma lista de objetos Categoria.
        """
        db = DbContext()
        sql = 'SELECT * FROM categorias WHERE usuario_id = ? ORDER BY nome'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(nome=row['nome'], usuario_id=row['usuario_id'], descricao=row['descricao'], 
                   icone=row['icone'], cor=row['cor'], id=row['id']) for row in rows]