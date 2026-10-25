import sqlite3
from pathlib import Path


PASTA_DADOS = (
    Path(__file__).resolve().parent.parent / "dados"
)

PASTA_DADOS.mkdir(exist_ok=True)

CAMINHO_BANCO = PASTA_DADOS / "adaptaia.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    conexao.row_factory = sqlite3.Row

    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao


def inicializar_banco():

    conexao = conectar()

    cursor = conexao.cursor()

    # ========================================================
    # TABELA DE ALUNOS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            observacoes TEXT DEFAULT '',
            criado_em TEXT NOT NULL,
            atualizado_em TEXT NOT NULL
        )
    """)

    # ========================================================
    # NECESSIDADES PEDAGÓGICAS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS necessidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE
        )
    """)

    # ========================================================
    # DOCUMENTOS DOS ALUNOS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            nome_arquivo TEXT NOT NULL,
            caminho TEXT NOT NULL,
            criado_em TEXT NOT NULL,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE
        )
    """)

    # ========================================================
    # HISTÓRICO DE ATIVIDADES
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            aluno_id INTEGER,

            aluno_nome TEXT DEFAULT '',

            ano TEXT NOT NULL,

            disciplina TEXT NOT NULL,

            conteudo TEXT NOT NULL,

            objetivo TEXT DEFAULT '',

            quantidade INTEGER NOT NULL,

            tipo TEXT NOT NULL,

            resultado TEXT NOT NULL,

            criado_em TEXT NOT NULL,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE SET NULL
        )
    """)

    conexao.commit()

    conexao.close()


inicializar_banco()