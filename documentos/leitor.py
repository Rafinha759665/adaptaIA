import fitz
from pathlib import Path


def extrair_texto_pdf(caminho):
    """
    Abre um PDF e extrai o texto de todas as páginas.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            "O arquivo selecionado não foi encontrado."
        )

    documento = fitz.open(caminho)

    textos = []

    for pagina in documento:
        texto = pagina.get_text()

        if texto.strip():
            textos.append(texto)

    documento.close()

    return "\n".join(textos)


def ler_documento(caminho):
    """
    Função principal para leitura do documento.
    """

    caminho = Path(caminho)

    if caminho.suffix.lower() != ".pdf":
        return {
            "sucesso": False,
            "texto": "",
            "mensagem": "Por enquanto, a leitura automática está disponível apenas para PDF."
        }

    texto = extrair_texto_pdf(caminho)

    if not texto.strip():
        return {
            "sucesso": False,
            "texto": "",
            "mensagem": (
                "O PDF foi aberto, mas não possui texto selecionável. "
                "Ele pode ser um documento digitalizado."
            )
        }

    return {
        "sucesso": True,
        "texto": texto,
        "mensagem": "Documento lido com sucesso."
    }