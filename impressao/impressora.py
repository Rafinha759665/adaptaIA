import os
from pathlib import Path


def imprimir_pdf(caminho_pdf):

    caminho_pdf = Path(caminho_pdf)

    if not caminho_pdf.exists():
        raise FileNotFoundError(
            "O arquivo PDF não foi encontrado."
        )

    if os.name != "nt":
        raise OSError(
            "A impressão direta está disponível "
            "apenas no Windows."
        )

    try:

        os.startfile(
            str(caminho_pdf),
            "print"
        )

    except Exception as erro:

        raise RuntimeError(
            "Não foi possível enviar o PDF "
            "para a impressora padrão do Windows."
        ) from erro