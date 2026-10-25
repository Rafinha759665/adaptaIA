from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Preformatted
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def configurar_fontes():
    """
    Tenta utilizar uma fonte com suporte a caracteres especiais.
    """

    fontes = [
        (
            "DejaVu",
            "C:/Windows/Fonts/DejaVuSans.ttf"
        ),
        (
            "Arial",
            "C:/Windows/Fonts/arial.ttf"
        )
    ]

    for nome, caminho in fontes:
        if Path(caminho).exists():
            pdfmetrics.registerFont(
                TTFont(nome, caminho)
            )
            return nome

    return "Helvetica"


def preparar_texto(texto):
    """
    Converte algumas marcações simples do Gemini
    para uma apresentação mais adequada no PDF.
    """

    texto = texto.replace("\r\n", "\n")
    texto = texto.replace("\r", "\n")

    return texto


def separar_resultado(texto):
    """
    Divide o resultado do Gemini em três partes:

    ATIVIDADE
    GABARITO
    ORIENTAÇÕES AO PROFESSOR
    """

    texto = preparar_texto(texto)

    marcador_gabarito = "GABARITO"
    marcador_orientacoes = "ORIENTAÇÕES AO PROFESSOR"

    if marcador_gabarito in texto:
        parte_atividade, restante = texto.split(
            marcador_gabarito,
            1
        )
    else:
        parte_atividade = texto
        restante = ""

    if marcador_orientacoes in restante:
        parte_gabarito, parte_orientacoes = restante.split(
            marcador_orientacoes,
            1
        )
    else:
        parte_gabarito = restante
        parte_orientacoes = ""

    return (
        parte_atividade.strip(),
        parte_gabarito.strip(),
        parte_orientacoes.strip()
    )


def criar_estilos(fonte):
    """
    Cria os estilos utilizados nos PDFs.
    """

    estilos = getSampleStyleSheet()

    estilos.add(
        ParagraphStyle(
            name="TituloAdaptaIA",
            parent=estilos["Title"],
            fontName=fonte,
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=20
        )
    )

    estilos.add(
        ParagraphStyle(
            name="CabecalhoAdaptaIA",
            parent=estilos["Heading2"],
            fontName=fonte,
            fontSize=12,
            leading=16,
            spaceBefore=10,
            spaceAfter=8
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TextoAdaptaIA",
            parent=estilos["BodyText"],
            fontName=fonte,
            fontSize=10.5,
            leading=15,
            spaceAfter=8
        )
    )

    estilos.add(
        ParagraphStyle(
            name="QuestaoAdaptaIA",
            parent=estilos["BodyText"],
            fontName=fonte,
            fontSize=10.5,
            leading=15,
            spaceAfter=10
        )
    )

    return estilos


def criar_pdf_atividade(
    atividade,
    resultado,
    pasta_destino
):
    """
    Cria o PDF destinado ao estudante.
    """

    pasta_destino = Path(pasta_destino)
    pasta_destino.mkdir(
        parents=True,
        exist_ok=True
    )

    caminho_pdf = (
        pasta_destino /
        "Atividade_Adaptada.pdf"
    )

    fonte = configurar_fontes()
    estilos = criar_estilos(fonte)

    parte_atividade, _, _ = separar_resultado(
        resultado
    )

    documento = SimpleDocTemplate(
        str(caminho_pdf),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    elementos = []

    elementos.append(
        Paragraph(
            "ADAPTAIA",
            estilos["TituloAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            "Atividade Adaptada",
            estilos["CabecalhoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Aluno:</b> "
            f"{atividade.aluno_nome or '________________________________'}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Ano:</b> {atividade.ano}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Disciplina:</b> {atividade.disciplina}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Conteúdo:</b> {atividade.conteudo}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "ATIVIDADE",
            estilos["CabecalhoAdaptaIA"]
        )
    )

    adicionar_texto_formatado(
        elementos,
        parte_atividade,
        estilos
    )

    documento.build(elementos)

    return caminho_pdf


def criar_pdf_gabarito(
    atividade,
    resultado,
    pasta_destino
):
    """
    Cria o PDF destinado ao professor.
    """

    pasta_destino = Path(pasta_destino)
    pasta_destino.mkdir(
        parents=True,
        exist_ok=True
    )

    caminho_pdf = (
        pasta_destino /
        "Gabarito_Professor.pdf"
    )

    fonte = configurar_fontes()
    estilos = criar_estilos(fonte)

    _, parte_gabarito, parte_orientacoes = (
        separar_resultado(resultado)
    )

    documento = SimpleDocTemplate(
        str(caminho_pdf),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    elementos = []

    elementos.append(
        Paragraph(
            "ADAPTAIA",
            estilos["TituloAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            "Gabarito e Orientações ao Professor",
            estilos["CabecalhoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Aluno:</b> "
            f"{atividade.aluno_nome or 'Não informado'}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Disciplina:</b> {atividade.disciplina}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Conteúdo:</b> {atividade.conteudo}",
            estilos["TextoAdaptaIA"]
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "GABARITO",
            estilos["CabecalhoAdaptaIA"]
        )
    )

    adicionar_texto_formatado(
        elementos,
        parte_gabarito,
        estilos
    )

    elementos.append(PageBreak())

    elementos.append(
        Paragraph(
            "ORIENTAÇÕES AO PROFESSOR",
            estilos["CabecalhoAdaptaIA"]
        )
    )

    adicionar_texto_formatado(
        elementos,
        parte_orientacoes,
        estilos
    )

    documento.build(elementos)

    return caminho_pdf


def adicionar_texto_formatado(
    elementos,
    texto,
    estilos
):
    """
    Adiciona o texto ao documento preservando
    linhas e separações básicas.
    """

    linhas = texto.split("\n")

    bloco = []

    for linha in linhas:

        linha = linha.rstrip()

        if not linha:
            if bloco:
                elementos.append(
                    Paragraph(
                        "<br/>".join(bloco),
                        estilos["TextoAdaptaIA"]
                    )
                )

                bloco = []

            elementos.append(
                Spacer(1, 5)
            )

            continue

        linha_html = (
            linha
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        linha_html = linha_html.replace(
            "**",
            "<b>",
            1
        )

        if "<b>" in linha_html:
            linha_html = linha_html.replace(
                "**",
                "</b>",
                1
            )

        bloco.append(linha_html)

    if bloco:
        elementos.append(
            Paragraph(
                "<br/>".join(bloco),
                estilos["TextoAdaptaIA"]
            )
        )