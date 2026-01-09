import sqlite3

class DbContext:
    def __init__(self, db_name='storage/data/cofrin_database.db'):
        """
        Inicializa o DbContext, conectando-se ao banco de dados e criando as tabelas, se necessário.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row  # Permite acesso às colunas por nome
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """
        Cria as tabelas no banco de dados se elas não existirem.
        """
        # Tabela de Usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                login TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                saldo REAL DEFAULT 0.0,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Categorias
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                icone TEXT,
                cor TEXT,
                usuario_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')

        # Tabela de Operações
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS operacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                data TIMESTAMP NOT NULL,
                usuario_id INTEGER,
                categoria_id INTEGER,
                subcategoria_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL,
                FOREIGN KEY (subcategoria_id) REFERENCES subcategorias (id) ON DELETE SET NULL
            )
        ''')
        
        # Tabela de Subcategorias
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subcategorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                icone TEXT,
                cor TEXT,
                categoria_id INTEGER,
                usuario_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')
        
        # Tabela de Recorrências
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                data_inicio TEXT NOT NULL,
                data_fim TEXT,
                ativo INTEGER DEFAULT 1,
                usuario_id INTEGER,
                categoria_id INTEGER,
                subcategoria_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL,
                FOREIGN KEY (subcategoria_id) REFERENCES subcategorias (id) ON DELETE SET NULL
            )
        ''')
        self.conn.commit()

    def get_connection(self):
        """
        Retorna a conexão ativa com o banco de dados.
        """
        return self.conn

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conn:
            self.conn.close()

# Exemplo de como usar (opcional, para teste)
if __name__ == '__main__':
    db_context = DbContext()
    print("Banco de dados e tabelas criados com sucesso.")
    db_context.close_connection()
