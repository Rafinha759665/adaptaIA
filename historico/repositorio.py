from datetime import datetime

from banco.database import conectar


def data_atual():
    return datetime.now().isoformat(
        timespec="seconds"
    )


def salvar_atividade(atividade, resultado):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO historico_atividades (
            aluno_id,
            aluno_nome,
            ano,
            disciplina,
            conteudo,
            objetivo,
            quantidade,
            tipo,
            resultado,
            criado_em
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            atividade.aluno_id,
            atividade.aluno_nome,
            atividade.ano,
            atividade.disciplina,
            atividade.conteudo,
            atividade.objetivo,
            atividade.quantidade,
            atividade.tipo,
            resultado,
            data_atual()
        )
    )

    conexao.commit()

    id_atividade = cursor.lastrowid

    conexao.close()

    return id_atividade


def listar_historico():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            aluno_id,
            aluno_nome,
            ano,
            disciplina,
            conteudo,
            objetivo,
            quantidade,
            tipo,
            resultado,
            criado_em

        FROM historico_atividades

        ORDER BY criado_em DESC
        """
    )

    historico = cursor.fetchall()

    conexao.close()

    return historico


def buscar_historico(id_atividade):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            aluno_id,
            aluno_nome,
            ano,
            disciplina,
            conteudo,
            objetivo,
            quantidade,
            tipo,
            resultado,
            criado_em

        FROM historico_atividades

        WHERE id = ?
        """,
        (id_atividade,)
    )

    atividade = cursor.fetchone()

    conexao.close()

    return atividade


def listar_historico_aluno(aluno_id):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            aluno_id,
            aluno_nome,
            ano,
            disciplina,
            conteudo,
            objetivo,
            quantidade,
            tipo,
            resultado,
            criado_em

        FROM historico_atividades

        WHERE aluno_id = ?

        ORDER BY criado_em DESC
        """,
        (aluno_id,)
    )

    historico = cursor.fetchall()

    conexao.close()

    return historico


def excluir_historico(id_atividade):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM historico_atividades
        WHERE id = ?
        """,
        (id_atividade,)
    )

    conexao.commit()

    conexao.close()