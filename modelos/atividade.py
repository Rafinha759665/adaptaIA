from dataclasses import dataclass, field


@dataclass
class Questao:

    numero: int

    enunciado: str

    tipo: str

    alternativas: list[str] = field(
        default_factory=list
    )

    resposta: str = ""


@dataclass
class Atividade:

    ano: str

    disciplina: str

    conteudo: str

    objetivo: str

    quantidade: int

    tipo: str

    observacoes: str = ""

    atividade_original: str = ""

    texto_documento: str = ""

    necessidades_pedagogicas: list[str] = field(
        default_factory=list
    )

    questoes: list[Questao] = field(
        default_factory=list
    )

    aluno_id: int | None = None

    aluno_nome: str = ""