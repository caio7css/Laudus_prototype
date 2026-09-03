import sqlite3
import os

CAMINHO_DB = os.path.join(os.path.dirname(__file__), 'medicos.db')

# (nome, crm, senha, especializacao, acesso_exames_imagem)
DADOS_MEDICOS = [
    ('Ana Beatriz Ramos',      '123456', 'senha123', 'Cardiologia',       1),
    ('Carlos Eduardo Lima',    '234567', 'senha234', 'Dermatologia',      0),
    ('Milena Veiga',           '345678', 'senha345', 'Radiologia',        1),
    ('Rafael Costa Melo',      '456789', 'senha456', 'Oftalmologia',      0),
    ('Juliana Farias',         '567890', 'senha567', 'Neurologia',        1),
    ('Pedro Henrique Alves',   '678901', 'senha678', 'Gastroenterologia', 0),
    ('Fernanda Duarte',        '789012', 'senha789', 'Ortopedia',         1),
    ('Marcos Vinícius Souza',  '890123', 'senha890', 'Pediatria',         0),
    ('Larissa Nogueira',       '901234', 'senha901', 'Pneumologia',       0),
    ('Bruno Cavalcanti',       '012345', 'senha012', 'Urologia',          0),
]


def inicializar_banco():
    """Cria o banco de dados SQLite (ou migra um já existente) e popula com os dados dos médicos.

    A coluna `nome` foi adicionada para permitir assinar o laudo com o nome do
    médico responsável. Se o banco já existir na versão antiga (sem essa
    coluna), ela é adicionada automaticamente via ALTER TABLE.
    """
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL DEFAULT '',
            crm TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            especializacao TEXT NOT NULL,
            acesso_exames_imagem BOOLEAN NOT NULL
        )
    ''')

    # Migração: bancos criados antes de existir a coluna "nome"
    cursor.execute("PRAGMA table_info(medicos)")
    colunas = [linha[1] for linha in cursor.fetchall()]
    if 'nome' not in colunas:
        cursor.execute("ALTER TABLE medicos ADD COLUMN nome TEXT NOT NULL DEFAULT ''")
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM medicos')
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO medicos (nome, crm, senha, especializacao, acesso_exames_imagem) VALUES (?, ?, ?, ?, ?)',
            DADOS_MEDICOS
        )
        conn.commit()
        print("✓ Banco de dados criado e populado com sucesso!")
        print("\nMédicos com acesso a exames de imagem:")
        for nome, crm, senha, esp, acesso in DADOS_MEDICOS:
            if acesso:
                print(f"  - {nome} | CRM: {crm} | Senha: {senha} | Especialização: {esp}")
    else:
        # Preenche o nome de registros antigos que ainda estejam vazios, casando pelo CRM
        for nome, crm, *_ in DADOS_MEDICOS:
            cursor.execute(
                "UPDATE medicos SET nome = ? WHERE crm = ? AND (nome IS NULL OR nome = '')",
                (nome, crm)
            )
        conn.commit()
        print("✓ Banco de dados já inicializado (verificado/migrado).")

    conn.close()


if __name__ == "__main__":
    inicializar_banco()
