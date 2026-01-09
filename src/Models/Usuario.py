import hashlib
import os
from Context.DbContext import DbContext

class Usuario:
    def __init__(self, nome, email, login, senha, saldo=0.0, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.login = login
        self.senha = senha
        self.saldo = saldo

    # ------------------ CRUD ------------------ #
    def save(self):
        """
        Salva o usuário no banco de dados.
        Se o ID for None, cria um novo usuário (INSERT).
        Se o ID existir, atualiza o usuário existente (UPDATE).
        """
        db = DbContext()
        cursor = db.get_connection().cursor()
        
        if self.id is None:
            # Novo usuário: hashear a senha antes de salvar
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', self.senha.encode('utf-8'), salt, 100000)
            storage = salt.hex() + '$' + key.hex()
            sql = 'INSERT INTO usuarios (nome, email, login, senha, saldo) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(sql, (self.nome, self.email, self.login, storage, self.saldo))
            self.id = cursor.lastrowid # Recupera o ID gerado
        else:
            # Usuário existente
            sql = 'UPDATE usuarios SET nome = ?, email = ?, login = ?, saldo = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?'
            cursor.execute(sql, (self.nome, self.email, self.login, self.saldo, self.id))
            
        db.get_connection().commit()
        db.close_connection()

    def delete(self):
        """
        Deleta o usuário do banco de dados.
        """
        if self.id is not None:
            db = DbContext()
            sql = 'DELETE FROM usuarios WHERE id = ?'
            db.get_connection().cursor().execute(sql, (self.id,))
            db.get_connection().commit()
            db.close_connection()

    # ------------------ Autenticação ------------------ #
    def verificar_senha(self, senha_plana):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        Retorna False se a senha/hashes estiverem malformados.
        """
        senha_raw = self.senha.decode("utf-8") if isinstance(self.senha, (bytes, bytearray)) else str(self.senha)
        try:
            salt_hex, key_hex = senha_raw.split('$')
            salt = bytes.fromhex(salt_hex)
            key = bytes.fromhex(key_hex)
        except Exception:
            return False

        new_key = hashlib.pbkdf2_hmac('sha256', senha_plana.encode('utf-8'), salt, 100000)
        
        return key == new_key

    # ------------------ Métodos de Busca ------------------ #
    @classmethod
    def find_by_login(cls, login):
        """
        Encontra um usuário pelo seu login.
        Retorna um objeto Usuario ou None se não for encontrado.
        """
        db = DbContext()
        sql = 'SELECT * FROM usuarios WHERE login = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (login,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(nome=row['nome'], email=row['email'], login=row['login'], senha=row['senha'], saldo=row['saldo'], id=row['id'])
        return None

    @classmethod
    def find_by_id(cls, user_id):
        """
        Encontra um usuário pelo seu ID.
        Retorna um objeto Usuario ou None se não for encontrado.
        """
        db = DbContext()
        sql = 'SELECT * FROM usuarios WHERE id = ?'
        cursor = db.get_connection().cursor()
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        db.close_connection()
        if row:
            return cls(nome=row['nome'], email=row['email'], login=row['login'], senha=row['senha'], saldo=row['saldo'], id=row['id'])
        return None
