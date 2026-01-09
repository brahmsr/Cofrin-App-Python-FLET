from Context.DbContext import DbContext

class Recorrencia:
    def __init__(self, tipo, valor, data_inicio, usuario_id, categoria_id=None, 
                 data_fim=None, ativo=1, id=None, subcategoria_id=None):
        self.id = id
        self.tipo = tipo  # "entrada" ou "saida"
        self.valor = valor
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.ativo = ativo
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.subcategoria_id = subcategoria_id
        
    # ------------------ CRUD ------------------ #
    def save(self):
        """
        Salva a recorrência no banco de dados (INSERT ou UPDATE).
        """
        db = DbContext()
        cursor = db.get_connection().cursor()
        
        if self.id is None:
            sql = '''INSERT INTO recorrencias (tipo, valor, data_inicio, data_fim, ativo, 
                     usuario_id, categoria_id, subcategoria_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(sql, (self.tipo, self.valor, self.data_inicio, self.data_fim, 
                                self.ativo, self.usuario_id, self.categoria_id, self.subcategoria_id))
            self.id = cursor.lastrowid
        else:
            sql = '''UPDATE recorrencias SET tipo = ?, valor = ?, data_inicio = ?, 
                     data_fim = ?, ativo = ?, usuario_id = ?, categoria_id = ?, subcategoria_id = ? WHERE id = ?'''
            cursor.execute(sql, (self.tipo, self.valor, self.data_inicio, self.data_fim, 
                                self.ativo, self.usuario_id, self.categoria_id, self.subcategoria_id, self.id))
            
        db.get_connection().commit()
        db.close_connection()

    def delete(self):
        """
        Deleta a recorrência do banco de dados.
        """
        if self.id is not None:
            db = DbContext()
            sql = 'DELETE FROM recorrencias WHERE id = ?'
            db.get_connection().cursor().execute(sql, (self.id,))
            db.get_connection().commit()
            db.close_connection()

    # ------------------ Métodos de Busca ------------------ #
    @classmethod
    def find_by_id(cls, rec_id):
        """
        Encontra uma recorrência pelo seu ID.
        """
        db = DbContext()
        sql = 'SELECT * FROM recorrencias WHERE id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (rec_id,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(tipo=row['tipo'], valor=row['valor'],
                      data_inicio=row['data_inicio'], usuario_id=row['usuario_id'], 
                      categoria_id=row['categoria_id'], data_fim=row['data_fim'], 
                      ativo=row['ativo'], id=row['id'], subcategoria_id=row['subcategoria_id'])
        return None

    @classmethod
    def find_all_by_usuario_id(cls, usuario_id):
        """
        Encontra todas as recorrências de um usuário específico.
        """
        db = DbContext()
        sql = 'SELECT * FROM recorrencias WHERE usuario_id = ? ORDER BY data_inicio DESC'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(tipo=row['tipo'], valor=row['valor'],
                   data_inicio=row['data_inicio'], usuario_id=row['usuario_id'], 
                   categoria_id=row['categoria_id'], data_fim=row['data_fim'], 
                   ativo=row['ativo'], id=row['id'], subcategoria_id=row['subcategoria_id']) for row in rows]

    @classmethod
    def find_all_ativas_by_usuario_id(cls, usuario_id):
        """
        Encontra todas as recorrências ativas de um usuário.
        """
        db = DbContext()
        sql = 'SELECT * FROM recorrencias WHERE usuario_id = ? AND ativo = 1 ORDER BY data_inicio DESC'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        db.close_connection()
        return [cls(tipo=row['tipo'], valor=row['valor'],
                   data_inicio=row['data_inicio'], usuario_id=row['usuario_id'], 
                   categoria_id=row['categoria_id'], data_fim=row['data_fim'], 
                   ativo=row['ativo'], id=row['id'], subcategoria_id=row['subcategoria_id']) for row in rows]
