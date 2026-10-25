from datetime import datetime
from pathlib import Path
import shutil

from banco.database import conectar, PASTA_DADOS


# ============================================================
# PASTA DOS DOCUMENTOS
# ============================================================

PASTA_DOCUMENTOS = PASTA_DADOS / "documentos"

PASTA_DOCUMENTOS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DATA ATUAL
# ============================================================

def data_atual():

    return datetime.now().isoformat(
        timespec="seconds"
    )


# ============================================================
# CADASTRAR ALUNO
# ============================================================

def cadastrar_aluno(
    nome,
    turma,
    necessidades,
    observacoes="",
    caminho_documento=""
):

    conexao = conectar()

    cursor = conexao.cursor()

    agora = data_atual()

    cursor.execute(
        """
        INSERT INTO alunos
        (
            nome,
            turma,
            observacoes,
            criado_em,
            atualizado_em
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nome,
            turma,
            observacoes,
            agora,
            agora
        )
    )

    aluno_id = cursor.lastrowid

    # --------------------------------------------------------
    # NECESSIDADES
    # --------------------------------------------------------

    for necessidade in necessidades:

        cursor.execute(
            """
            INSERT INTO necessidades
            (
                aluno_id,
                descricao
            )
            VALUES (?, ?)
            """,
            (
                aluno_id,
                necessidade
            )
        )

    conexao.commit()

    conexao.close()

    # --------------------------------------------------------
    # DOCUMENTO
    # --------------------------------------------------------

    if caminho_documento:

        adicionar_documento(
            aluno_id,
            caminho_documento
        )

    return aluno_id


# ============================================================
# LISTAR ALUNOS
# ============================================================

def listar_alunos():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            turma,
            observacoes,
            criado_em,
            atualizado_em
        FROM alunos
        ORDER BY nome
        """
    )

    alunos = cursor.fetchall()

    conexao.close()

    return alunos


# ============================================================
# BUSCAR ALUNO
# ============================================================

def buscar_aluno(
    aluno_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            turma,
            observacoes,
            criado_em,
            atualizado_em
        FROM alunos
        WHERE id = ?
        """,
        (
            aluno_id,
        )
    )

    aluno = cursor.fetchone()

    conexao.close()

    return aluno


# ============================================================
# BUSCAR NECESSIDADES
# ============================================================

def buscar_necessidades(
    aluno_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            descricao
        FROM necessidades
        WHERE aluno_id = ?
        ORDER BY id
        """,
        (
            aluno_id,
        )
    )

    necessidades = cursor.fetchall()

    conexao.close()

    return necessidades


# ============================================================
# BUSCAR DOCUMENTOS
# ============================================================

def buscar_documentos(
    aluno_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome_arquivo,
            caminho,
            criado_em
        FROM documentos
        WHERE aluno_id = ?
        ORDER BY id DESC
        """,
        (
            aluno_id,
        )
    )

    documentos = cursor.fetchall()

    conexao.close()

    return documentos


# ============================================================
# ATUALIZAR ALUNO
# ============================================================

def atualizar_aluno(
    aluno_id,
    nome,
    turma,
    necessidades,
    observacoes=""
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE alunos
        SET
            nome = ?,
            turma = ?,
            observacoes = ?,
            atualizado_em = ?
        WHERE id = ?
        """,
        (
            nome,
            turma,
            observacoes,
            data_atual(),
            aluno_id
        )
    )

    # Remove necessidades antigas

    cursor.execute(
        """
        DELETE FROM necessidades
        WHERE aluno_id = ?
        """,
        (
            aluno_id,
        )
    )

    # Insere necessidades atuais

    for necessidade in necessidades:

        cursor.execute(
            """
            INSERT INTO necessidades
            (
                aluno_id,
                descricao
            )
            VALUES (?, ?)
            """,
            (
                aluno_id,
                necessidade
            )
        )

    conexao.commit()

    conexao.close()


# ============================================================
# ADICIONAR DOCUMENTO
# ============================================================

def adicionar_documento(
    aluno_id,
    caminho_original
):

    caminho_original = Path(
        caminho_original
    )

    if not caminho_original.exists():

        raise FileNotFoundError(
            "O documento selecionado não foi encontrado."
        )

    pasta_aluno = (
        PASTA_DOCUMENTOS
        / str(aluno_id)
    )

    pasta_aluno.mkdir(
        parents=True,
        exist_ok=True
    )

    destino = (
        pasta_aluno
        / caminho_original.name
    )

    # Se já existir, cria outro nome

    contador = 1

    while destino.exists():

        destino = (
            pasta_aluno
            / f"{caminho_original.stem}_{contador}"
            f"{caminho_original.suffix}"
        )

        contador += 1

    shutil.copy2(
        caminho_original,
        destino
    )

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO documentos
        (
            aluno_id,
            nome_arquivo,
            caminho,
            criado_em
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            aluno_id,
            destino.name,
            str(destino),
            data_atual()
        )
    )

    conexao.commit()

    conexao.close()


# ============================================================
# EXCLUIR ALUNO
# ============================================================

def excluir_aluno(
    aluno_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM alunos
        WHERE id = ?
        """,
        (
            aluno_id,
        )
    )

    conexao.commit()

    conexao.close()

    # --------------------------------------------------------
    # EXCLUIR DOCUMENTOS FÍSICOS
    # --------------------------------------------------------

    pasta_aluno = (
        PASTA_DOCUMENTOS
        / str(aluno_id)
    )

    if pasta_aluno.exists():

        shutil.rmtree(
            pasta_aluno
        )