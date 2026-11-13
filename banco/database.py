
import sqlite3
from pathlib import Path
import os


# ============================================================
# PASTA DE DADOS DO USUÁRIO
# ============================================================

# No Windows, os dados do AdaptaIA ficam na pasta:
#
# C:\Users\SEU_USUARIO\AppData\Local\AdaptaIA\dados
#
# Dessa forma, o banco e os dados do usuário não ficam dentro
# da pasta de instalação do programa.

PASTA_APPDATA = Path(
    os.environ.get(
        "LOCALAPPDATA",
        Path.home() / "AppData" / "Local"
    )
)

PASTA_DADOS = PASTA_APPDATA / "AdaptaIA" / "dados"


# Cria a pasta caso ela ainda não exista.
PASTA_DADOS.mkdir(
    parents=True,
    exist_ok=True
)


# Caminho do banco de dados.
CAMINHO_BANCO = PASTA_DADOS / "adaptaia.db"


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

def conectar():

    conexao = sqlite3.connect(
        CAMINHO_BANCO
    )

    # Permite acessar as colunas pelo nome.
    conexao.row_factory = sqlite3.Row

    # Ativa as chaves estrangeiras.
    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao


# ============================================================
# INICIALIZAÇÃO DO BANCO
# ============================================================

def inicializar_banco():

    conexao = conectar()

    cursor = conexao.cursor()

    # ========================================================
    # TABELA DE ALUNOS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alunos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            turma TEXT,

            observacoes TEXT,

            criado_em TEXT DEFAULT CURRENT_TIMESTAMP,

            atualizado_em TEXT

        )
        """
    )

    # ========================================================
    # TABELA DE NECESSIDADES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS necessidades (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            aluno_id INTEGER NOT NULL,

            descricao TEXT NOT NULL,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE

        )
        """
    )

    # ========================================================
    # TABELA DE DOCUMENTOS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documentos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            aluno_id INTEGER NOT NULL,

            nome_arquivo TEXT NOT NULL,

            caminho TEXT NOT NULL,

            criado_em TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE

        )
        """
    )

    # ========================================================
    # TABELA DE HISTÓRICO
    # ========================================================

    # Esta é a estrutura utilizada pelo
    # historico/repositorio.py.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS historico_atividades (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            aluno_id INTEGER,

            aluno_nome TEXT,

            ano TEXT,

            disciplina TEXT,

            conteudo TEXT,

            objetivo TEXT,

            quantidade INTEGER,

            tipo TEXT,

            resultado TEXT,

            criado_em TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE SET NULL

        )
        """
    )

    # ========================================================
    # MIGRAÇÃO DA TABELA ALUNOS
    # ========================================================

    colunas_alunos = [
        coluna[1]
        for coluna in cursor.execute(
            "PRAGMA table_info(alunos)"
        ).fetchall()
    ]

    # Adiciona atualizado_em em bancos antigos.
    if "atualizado_em" not in colunas_alunos:

        cursor.execute(
            """
            ALTER TABLE alunos
            ADD COLUMN atualizado_em TEXT
            """
        )

    # Preenche atualizado_em dos registros antigos.
    cursor.execute(
        """
        UPDATE alunos

        SET atualizado_em = COALESCE(
            atualizado_em,
            criado_em
        )

        WHERE atualizado_em IS NULL
        """
    )

    # ========================================================
    # MIGRAÇÃO DA TABELA DOCUMENTOS
    # ========================================================

    colunas_documentos = [
        coluna[1]
        for coluna in cursor.execute(
            "PRAGMA table_info(documentos)"
        ).fetchall()
    ]

    # Adiciona nome_arquivo em bancos antigos.
    if "nome_arquivo" not in colunas_documentos:

        cursor.execute(
            """
            ALTER TABLE documentos
            ADD COLUMN nome_arquivo TEXT
            """
        )

        # Tenta recuperar o nome utilizando o caminho.
        cursor.execute(
            """
            UPDATE documentos

            SET nome_arquivo = caminho

            WHERE nome_arquivo IS NULL
            """
        )

    # ========================================================
    # MIGRAÇÃO DA TABELA HISTÓRICO
    # ========================================================

    # Descobre quais colunas já existem.
    colunas_historico = [
        coluna[1]
        for coluna in cursor.execute(
            "PRAGMA table_info(historico_atividades)"
        ).fetchall()
    ]

    # --------------------------------------------------------
    # aluno_nome
    # --------------------------------------------------------

    if "aluno_nome" not in colunas_historico:

        cursor.execute(
            """
            ALTER TABLE historico_atividades
            ADD COLUMN aluno_nome TEXT
            """
        )

    # --------------------------------------------------------
    # ano
    # --------------------------------------------------------

    if "ano" not in colunas_historico:

        cursor.execute(
            """
            ALTER TABLE historico_atividades
            ADD COLUMN ano TEXT
            """
        )

    # --------------------------------------------------------
    # resultado
    # --------------------------------------------------------

    if "resultado" not in colunas_historico:

        cursor.execute(
            """
            ALTER TABLE historico_atividades
            ADD COLUMN resultado TEXT
            """
        )

    # ========================================================
    # RECUPERAÇÃO DE DADOS ANTIGOS
    # ========================================================

    # Recupera o nome dos alunos nos históricos antigos.
    cursor.execute(
        """
        UPDATE historico_atividades

        SET aluno_nome = (
            SELECT nome
            FROM alunos
            WHERE alunos.id = historico_atividades.aluno_id
        )

        WHERE aluno_nome IS NULL
          AND aluno_id IS NOT NULL
        """
    )

    # Caso exista uma coluna "atividade" de uma versão
    # anterior do banco, tenta aproveitar o conteúdo
    # para preencher "resultado".
    colunas_historico_atualizadas = [
        coluna[1]
        for coluna in cursor.execute(
            "PRAGMA table_info(historico_atividades)"
        ).fetchall()
    ]

    if "atividade" in colunas_historico_atualizadas:

        cursor.execute(
            """
            UPDATE historico_atividades

            SET resultado = atividade

            WHERE resultado IS NULL
              AND atividade IS NOT NULL
            """
        )

    # ========================================================
    # FINALIZAÇÃO
    # ========================================================

    conexao.commit()

    conexao.close()


# ============================================================
# INICIALIZAÇÃO AUTOMÁTICA
# ============================================================

inicializar_banco()
