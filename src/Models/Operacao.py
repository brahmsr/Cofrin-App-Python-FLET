from Context.DbContext import DbContext

class Operacao:
    def __init__(self, tipo, valor, data, usuario_id, categoria_id=None, id=None, subcategoria_id=None):
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.subcategoria_id = subcategoria_id
        
    # ------------------ CRUD ------------------ #
    def save(self):
        """
        Salva a operação no banco de dados (INSERT ou UPDATE).
        """
        db = DbContext()
        cursor = db.get_connection().cursor()
        
        if self.id is None:
            sql = 'INSERT INTO operacoes (tipo, valor, data, usuario_id, categoria_id, subcategoria_id) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(sql, (self.tipo, self.valor, self.data, self.usuario_id, self.categoria_id, self.subcategoria_id))
            self.id = cursor.lastrowid
        else:
            sql = 'UPDATE operacoes SET tipo = ?, valor = ?, data = ?, usuario_id = ?, categoria_id = ?, subcategoria_id = ? WHERE id = ?'
            cursor.execute(sql, (self.tipo, self.valor, self.data, self.usuario_id, self.categoria_id, self.subcategoria_id, self.id))
            
        db.get_connection().commit()
        db.close_connection()

    def delete(self):
        """
        Deleta a operação do banco de dados.
        """
        if self.id is not None:
            db = DbContext()
            sql = 'DELETE FROM operacoes WHERE id = ?'
            db.get_connection().cursor().execute(sql, (self.id,))
            db.get_connection().commit()
            db.close_connection()

    # ------------------ Métodos de Busca ------------------ #
    @classmethod
    def find_by_id(cls, op_id):
        """
        Encontra uma operação pelo seu ID.
        """
        db = DbContext()
        sql = 'SELECT * FROM operacoes WHERE id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (op_id,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(tipo=row['tipo'], valor=row['valor'], data=row['data'], usuario_id=row['usuario_id'], 
                      categoria_id=row['categoria_id'], id=row['id'], subcategoria_id=row['subcategoria_id'])
        return None

    @classmethod
    def find_all_by_usuario_id(cls, usuario_id):
        """
        Encontra todas as operações de um usuário específico.
        Retorna uma lista de objetos Operacao.
        """
        db = DbContext()
        sql = 'SELECT * FROM operacoes WHERE usuario_id = ? ORDER BY data DESC'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(tipo=row['tipo'], valor=row['valor'], data=row['data'], usuario_id=row['usuario_id'], 
                   categoria_id=row['categoria_id'], id=row['id'], subcategoria_id=row['subcategoria_id']) for row in rows]

    @classmethod
    def find_all_by_categoria_id(cls, categoria_id):
        """
        Encontra todas as operações de uma categoria específica.
        Retorna uma lista de objetos Operacao.
        """
        db = DbContext()
        sql = 'SELECT * FROM operacoes WHERE categoria_id = ? ORDER BY data DESC'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (categoria_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(tipo=row['tipo'], valor=row['valor'], data=row['data'], usuario_id=row['usuario_id'], 
                   categoria_id=row['categoria_id'], id=row['id'], subcategoria_id=row['subcategoria_id']) for row in rows]
    
    @classmethod
    def find_all_by_subcategoria_id(cls, subcategoria_id):
        """
        Encontra todas as operações de uma subcategoria específica.
        Retorna uma lista de objetos Operacao.
        """
        db = DbContext()
        sql = 'SELECT * FROM operacoes WHERE subcategoria_id = ? ORDER BY data DESC'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (subcategoria_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(tipo=row['tipo'], valor=row['valor'], data=row['data'], usuario_id=row['usuario_id'], 
                   categoria_id=row['categoria_id'], id=row['id'], subcategoria_id=row['subcategoria_id']) for row in rows]