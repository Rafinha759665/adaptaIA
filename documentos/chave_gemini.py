import keyring


# Nome usado para identificar o aplicativo
NOME_APLICACAO = "AdaptaIA"

# Nome usado para armazenar a chave
NOME_CHAVE = "gemini_api_key"


def salvar_chave(chave: str) -> None:
    """
    Salva a chave da API do Gemini no armazenamento
    seguro do sistema operacional.
    """

    if not chave:
        raise ValueError(
            "A chave da API do Gemini não pode estar vazia."
        )

    chave = chave.strip()

    if not chave:
        raise ValueError(
            "A chave da API do Gemini não pode estar vazia."
        )

    keyring.set_password(
        NOME_APLICACAO,
        NOME_CHAVE,
        chave
    )


def obter_chave() -> str | None:
    """
    Recupera a chave da API do Gemini.

    Retorna:
        A chave configurada pelo professor
        ou None caso nenhuma chave esteja configurada.
    """

    return keyring.get_password(
        NOME_APLICACAO,
        NOME_CHAVE
    )


def existe_chave() -> bool:
    """
    Verifica se existe uma chave do Gemini configurada.
    """

    chave = obter_chave()

    return bool(chave)


def remover_chave() -> None:
    """
    Remove a chave do Gemini armazenada.
    """

    try:
        keyring.delete_password(
            NOME_APLICACAO,
            NOME_CHAVE
        )

    except keyring.errors.PasswordDeleteError:
        # Não existe uma chave para remover.
        pass