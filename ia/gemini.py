from google import genai

from config.settings import GEMINI_MODEL
from documentos.chave_gemini import obter_chave
from modelos.atividade import Atividade


def criar_cliente():
    """
    Cria o cliente responsável pela comunicação com o Gemini.
    """

    chave = obter_chave()

    if not chave:
        raise ValueError(
            "Nenhuma chave da API do Gemini foi configurada.\n\n"
            "Abra a configuração da Inteligência Artificial "
            "e informe sua chave da API do Gemini."
        )

    return genai.Client(api_key=chave)


def montar_prompt(atividade: Atividade) -> str:
    """
    Monta o prompt que será enviado ao Gemini.
    """

    necessidades = "\n".join(
        f"- {necessidade}"
        for necessidade in atividade.necessidades_pedagogicas
    )

    if not necessidades:
        necessidades = (
            "Nenhuma necessidade pedagógica específica "
            "foi informada."
        )

    prompt = f"""
Você é uma inteligência artificial especializada
em adaptação pedagógica inclusiva para estudantes
do Ensino Médio.

Sua tarefa é criar uma atividade adaptada para o
professor, respeitando rigorosamente as informações
fornecidas.

==================================================
DADOS FORNECIDOS PELO PROFESSOR
==================================================

ANO:
{atividade.ano}

DISCIPLINA:
{atividade.disciplina}

CONTEÚDO:
{atividade.conteudo}

OBJETIVO PEDAGÓGICO:
{atividade.objetivo or "Não informado."}

QUANTIDADE DE QUESTÕES:
{atividade.quantidade}

TIPO DE ATIVIDADE:
{atividade.tipo}

==================================================
NECESSIDADES PEDAGÓGICAS CONFIRMADAS
==================================================

{necessidades}

==================================================
OBSERVAÇÕES DO PROFESSOR
==================================================

{atividade.observacoes or "Nenhuma observação foi informada."}

==================================================
ATIVIDADE ORIGINAL
==================================================

{atividade.atividade_original or "Nenhuma atividade original foi fornecida."}

==================================================
REGRAS OBRIGATÓRIAS
==================================================

1. O ANO informado pelo professor é obrigatório e deve
   ser mantido exatamente como foi informado.

2. A DISCIPLINA informada pelo professor é obrigatória
   e deve ser mantida exatamente como foi informada.

3. O CONTEÚDO informado pelo professor deve ser mantido.
   Não substitua o conteúdo por outro assunto.

4. O OBJETIVO PEDAGÓGICO deve ser preservado.
   A adaptação deve facilitar o acesso ao conteúdo,
   mas não deve eliminar o objetivo de aprendizagem.

5. Crie EXATAMENTE {atividade.quantidade} questões.

6. O tipo solicitado pelo professor é:
   {atividade.tipo}

7. Nunca altere a quantidade de questões solicitada.

8. Nunca troque o ano escolar por outro ano.

9. Nunca troque a disciplina por outra disciplina.

10. Nunca invente informações pessoais sobre o estudante.

11. Nunca invente diagnósticos ou condições de saúde.

12. Não faça uma adaptação baseada apenas em um diagnóstico.
    Utilize principalmente as necessidades pedagógicas
    confirmadas pelo professor.

13. Não infantilize a atividade.

14. Utilize linguagem adequada ao Ensino Médio.

15. Caso o estudante tenha dificuldade com textos longos,
    utilize enunciados mais curtos e objetivos.

16. Caso tenha sido solicitado apoio visual, organize
    informações de maneira visualmente clara.
    Quando apropriado, utilize tabelas, esquemas,
    tópicos ou representações textuais simples.

17. Caso tenha sido solicitado dividir exercícios em etapas,
    apresente as etapas de forma clara e organizada.

18. Caso tenha sido solicitada facilidade na interpretação,
    escreva comandos claros e objetivos.

19. Caso tenha sido solicitado destaque de informações,
    organize as informações principais de maneira evidente.

20. Preserve a complexidade adequada ao Ensino Médio.

21. Não reduza o conteúdo a uma atividade infantil.

22. Se uma informação importante não tiver sido fornecida,
    não invente. Trabalhe apenas com as informações disponíveis.

23. A resposta deve conter separadamente:
    - atividade
    - gabarito
    - orientações ao professor

==================================================
VERIFICAÇÃO OBRIGATÓRIA ANTES DA RESPOSTA
==================================================

Antes de responder, confira:

ANO:
Deve ser exatamente:
{atividade.ano}

DISCIPLINA:
Deve ser exatamente:
{atividade.disciplina}

CONTEÚDO:
Deve corresponder a:
{atividade.conteudo}

QUANTIDADE:
Deve ser exatamente:
{atividade.quantidade} questões.

TIPO:
Deve respeitar:
{atividade.tipo}

Se qualquer um desses dados estiver diferente,
corrija antes de apresentar a resposta.

==================================================
FORMATO DA RESPOSTA
==================================================

ATIVIDADE

Título:
Crie um título relacionado ao conteúdo.

Disciplina:
Repita exatamente a disciplina informada.

Ano:
Repita exatamente o ano informado.

Conteúdo:
Repita exatamente o conteúdo informado.

Objetivo:
Repita ou preserve o objetivo pedagógico informado.

INSTRUÇÕES AO ESTUDANTE

Apresente instruções claras, curtas e objetivas.

QUESTÕES

Crie exatamente {atividade.quantidade} questões.

Respeite o tipo:
{atividade.tipo}

Para múltipla escolha:
- apresente alternativas;
- identifique as alternativas com A, B, C e D;
- deixe clara apenas uma resposta correta.

Para questões discursivas:
- apresente espaço adequado para resposta.

Para atividade mista:
- combine questões de múltipla escolha e discursivas.

GABARITO

Apresente o número de cada questão
e sua resposta correta.

ORIENTAÇÕES AO PROFESSOR

Adaptações utilizadas:
Explique quais adaptações foram aplicadas.

Motivo das adaptações:
Explique brevemente por que essas adaptações
foram utilizadas.

Observações:
Apresente observações importantes para o professor.

==================================================

Crie uma atividade clara, acessível, adequada ao
Ensino Médio e coerente com os dados fornecidos.

NÃO altere o ano.
NÃO altere a disciplina.
NÃO altere o conteúdo.
NÃO altere o objetivo.
NÃO altere a quantidade de questões.
NÃO altere o tipo de atividade.
"""

    return prompt.strip()


def gerar_atividade(atividade: Atividade) -> str:
    """
    Envia a atividade para o Gemini e retorna o resultado.
    """

    cliente = criar_cliente()

    prompt = montar_prompt(atividade)

    resposta = cliente.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not resposta.text:
        raise ValueError(
            "O Gemini não retornou nenhum conteúdo."
        )

    return resposta.text.strip()