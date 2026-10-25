import customtkinter as ctk
from tkinter import filedialog, messagebox


from documentos.leitor import ler_documento
from modelos.atividade import Atividade
from alunos.repositorio import listar_alunos, buscar_necessidades
from pdf.gerador import criar_pdf_atividade, criar_pdf_gabarito
from impressao.impressora import imprimir_pdf


# ============================================================
# TELA INICIAL
# ============================================================

class TelaInicial(ctk.CTkFrame):

    def __init__(self, master, iniciar_criacao):
        super().__init__(master)

        self.iniciar_criacao = iniciar_criacao

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=40,
            pady=40
        )

        container.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            container,
            text="AdaptaIA",
            font=ctk.CTkFont(
                size=38,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(80, 10)
        )

        subtitulo = ctk.CTkLabel(
            container,
            text="Inteligência Artificial para uma educação mais inclusiva.",
            font=ctk.CTkFont(size=18),
            wraplength=700
        )

        subtitulo.grid(
            row=1,
            column=0,
            pady=10
        )

        descricao = ctk.CTkLabel(
            container,
            text=(
                "Crie atividades adaptadas para estudantes "
                "do Ensino Médio, considerando objetivos "
                "pedagógicos e necessidades educacionais "
                "confirmadas pelo professor."
            ),
            font=ctk.CTkFont(size=15),
            wraplength=650,
            justify="center"
        )

        descricao.grid(
            row=2,
            column=0,
            pady=(10, 30)
        )

        botao = ctk.CTkButton(
            container,
            text="Criar atividade adaptada",
            width=260,
            height=50,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            command=self.iniciar_criacao
        )

        botao.grid(
            row=3,
            column=0,
            pady=20
        )


# ============================================================
# TELA DE CRIAÇÃO
# ============================================================

class TelaCriacao(ctk.CTkFrame):

    def __init__(
        self,
        master,
        voltar_inicio,
        abrir_revisao
    ):
        super().__init__(master)

        self.voltar_inicio = voltar_inicio
        self.abrir_revisao = abrir_revisao

        # Dados dos alunos
        self.alunos = []
        self.aluno_selecionado_id = None
        self.aluno_necessidades = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Criar atividade adaptada",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        formulario = ctk.CTkScrollableFrame(
            self
        )

        formulario.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )

        formulario.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # ALUNO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Aluno:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.aluno = ctk.CTkComboBox(
            formulario,
            values=["Nenhum aluno"],
            command=self.selecionar_aluno
        )

        self.aluno.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 5)
        )

        self.aluno.set(
            "Nenhum aluno"
        )

        self.label_turma = ctk.CTkLabel(
            formulario,
            text="Nenhum aluno selecionado.",
            anchor="w"
        )

        self.label_turma.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.label_necessidades = ctk.CTkLabel(
            formulario,
            text="Necessidades cadastradas: nenhuma.",
            anchor="w",
            justify="left",
            wraplength=800
        )

        self.label_necessidades.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(0, 15)
        )

        self.carregar_alunos()

        # ====================================================
        # ANO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Ano do Ensino Médio:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.ano = ctk.CTkComboBox(
            formulario,
            values=[
                "1º ano do Ensino Médio",
                "2º ano do Ensino Médio",
                "3º ano do Ensino Médio"
            ]
        )

        self.ano.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.ano.set(
            "1º ano do Ensino Médio"
        )

        # ====================================================
        # DISCIPLINA
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Disciplina:"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.disciplina = ctk.CTkComboBox(
            formulario,
            values=[
                "Português",
                "Matemática",
                "Biologia",
                "Química",
                "Física",
                "História",
                "Geografia",
                "Filosofia",
                "Sociologia",
                "Inglês",
                "Outras"
            ]
        )

        self.disciplina.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.disciplina.set(
            "Português"
        )

        # ====================================================
        # CONTEÚDO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Conteúdo:"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.conteudo = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: Primeira Lei de Mendel"
        )

        self.conteudo.grid(
            row=9,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ====================================================
        # OBJETIVO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Objetivo pedagógico:"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.objetivo = ctk.CTkTextbox(
            formulario,
            height=100
        )

        self.objetivo.grid(
            row=11,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ====================================================
        # QUANTIDADE
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Quantidade de questões (3 a 15):"
        ).grid(
            row=12,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.quantidade = ctk.CTkEntry(
            formulario
        )

        self.quantidade.grid(
            row=13,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.quantidade.insert(
            0,
            "5"
        )

        # ====================================================
        # TIPO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Tipo de atividade:"
        ).grid(
            row=14,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.tipo = ctk.CTkComboBox(
            formulario,
            values=[
                "Múltipla escolha",
                "Discursiva",
                "Mista"
            ]
        )

        self.tipo.grid(
            row=15,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.tipo.set(
            "Mista"
        )

        # ====================================================
        # OBSERVAÇÕES
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Observações adicionais:"
        ).grid(
            row=16,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.observacoes = ctk.CTkTextbox(
            formulario,
            height=100
        )

        self.observacoes.grid(
            row=17,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ====================================================
        # ATIVIDADE ORIGINAL
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Atividade original (opcional):"
        ).grid(
            row=18,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        self.atividade_original = ctk.CTkTextbox(
            formulario,
            height=120
        )

        self.atividade_original.grid(
            row=19,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ====================================================
        # DOCUMENTO
        # ====================================================

        ctk.CTkLabel(
            formulario,
            text="Documento / laudo pedagógico:"
        ).grid(
            row=20,
            column=0,
            sticky="w",
            pady=(10, 5)
        )

        linha_documento = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )

        linha_documento.grid(
            row=21,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        linha_documento.grid_columnconfigure(
            0,
            weight=1
        )

        self.caminho_documento = ctk.CTkEntry(
            linha_documento,
            placeholder_text="Nenhum documento selecionado"
        )

        self.caminho_documento.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        ctk.CTkButton(
            linha_documento,
            text="Selecionar PDF",
            width=150,
            command=self.selecionar_documento
        ).grid(
            row=0,
            column=1
        )

        # ====================================================
        # BOTÕES
        # ====================================================

        botoes = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )

        botoes.grid(
            row=22,
            column=0,
            pady=25
        )

        ctk.CTkButton(
            botoes,
            text="Voltar",
            width=140,
            command=self.voltar_inicio
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ctk.CTkButton(
            botoes,
            text="Continuar",
            width=180,
            command=self.continuar
        ).grid(
            row=0,
            column=1,
            padx=10
        )

    # ========================================================
    # CARREGAR ALUNOS
    # ========================================================

    def carregar_alunos(self):

        try:

            self.alunos = listar_alunos()

            nomes = [
                "Nenhum aluno"
            ]

            for aluno in self.alunos:

                nomes.append(
                    f"{aluno['nome']} - {aluno['turma']}"
                )

            self.aluno.configure(
                values=nomes
            )

        except Exception as erro:

            print(
                "Erro ao carregar alunos:",
                erro
            )

    # ========================================================
    # SELECIONAR ALUNO
    # ========================================================

    def selecionar_aluno(self, escolha):

        if escolha == "Nenhum aluno":

            self.aluno_selecionado_id = None
            self.aluno_necessidades = []

            self.label_turma.configure(
                text="Nenhum aluno selecionado."
            )

            self.label_necessidades.configure(
                text="Necessidades cadastradas: nenhuma."
            )

            return

        aluno_encontrado = None

        for aluno in self.alunos:

            nome_exibicao = (
                f"{aluno['nome']} - {aluno['turma']}"
            )

            if nome_exibicao == escolha:

                aluno_encontrado = aluno
                break

        if aluno_encontrado is None:
            return

        self.aluno_selecionado_id = (
            aluno_encontrado["id"]
        )

        self.label_turma.configure(
            text=(
                f"Turma: {aluno_encontrado['turma']}"
            )
        )

        necessidades = buscar_necessidades(
            self.aluno_selecionado_id
        )

        self.aluno_necessidades = [
            necessidade["descricao"]
            for necessidade in necessidades
        ]

        if self.aluno_necessidades:

            texto = (
                "Necessidades cadastradas:\n"
                + "\n".join(
                    f"✓ {necessidade}"
                    for necessidade in self.aluno_necessidades
                )
            )

        else:

            texto = (
                "Necessidades cadastradas: nenhuma."
            )

        self.label_necessidades.configure(
            text=texto
        )

    # ========================================================
    # SELECIONAR DOCUMENTO
    # ========================================================

    def selecionar_documento(self):

        caminho = filedialog.askopenfilename(
            title="Selecionar documento",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if caminho:

            self.caminho_documento.delete(
                0,
                "end"
            )

            self.caminho_documento.insert(
                0,
                caminho
            )

    # ========================================================
    # CONTINUAR
    # ========================================================

    def continuar(self):

        try:

            quantidade = int(
                self.quantidade.get()
            )

        except ValueError:

            messagebox.showerror(
                "Quantidade inválida",
                "Informe um número inteiro entre 3 e 15."
            )

            return

        if quantidade < 3 or quantidade > 15:

            messagebox.showerror(
                "Quantidade inválida",
                "A quantidade deve estar entre 3 e 15."
            )

            return

        if not self.conteudo.get().strip():

            messagebox.showerror(
                "Conteúdo obrigatório",
                "Informe o conteúdo da atividade."
            )

            return

        aluno_nome = ""

        for aluno in self.alunos:

            if aluno["id"] == self.aluno_selecionado_id:

                aluno_nome = aluno["nome"]

                break

        dados = {

            "ano": self.ano.get(),

            "disciplina": self.disciplina.get(),

            "conteudo": self.conteudo.get().strip(),

            "objetivo": self.objetivo.get(
                "1.0",
                "end"
            ).strip(),

            "quantidade": quantidade,

            "tipo": self.tipo.get(),

            "observacoes": self.observacoes.get(
                "1.0",
                "end"
            ).strip(),

            "atividade_original": self.atividade_original.get(
                "1.0",
                "end"
            ).strip(),

            "caminho_documento": self.caminho_documento.get(),

            "aluno_id": self.aluno_selecionado_id,

            "aluno_nome": aluno_nome,

            "necessidades_aluno": (
                self.aluno_necessidades.copy()
            )
        }

        # ====================================================
        # LEITURA DO DOCUMENTO
        # ====================================================

        texto_documento = ""

        caminho = (
            self.caminho_documento.get().strip()
        )

        if caminho:

            resultado = ler_documento(
                caminho
            )

            if resultado["sucesso"]:

                texto_documento = (
                    resultado["texto"]
                )

            else:

                messagebox.showwarning(
                    "Documento",
                    resultado["mensagem"]
                )

        # ====================================================
        # ABRIR REVISÃO
        # ====================================================

        self.abrir_revisao(
            dados,
            texto_documento
        )


# ============================================================
# TELA DE REVISÃO
# ============================================================

class TelaRevisao(ctk.CTkFrame):

    def __init__(
        self,
        master,
        dados,
        texto_documento,
        voltar_criacao,
        abrir_necessidades
    ):
        super().__init__(master)

        self.dados = dados
        self.texto_documento = texto_documento

        self.voltar_criacao = voltar_criacao
        self.abrir_necessidades = abrir_necessidades

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        titulo = ctk.CTkLabel(
            self,
            text="Revisão do documento",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            self,
            text=(
                "Revise as informações extraídas do documento. "
                "Você pode corrigir ou complementar o texto "
                "antes de continuar."
            ),
            wraplength=800
        ).grid(
            row=1,
            column=0,
            padx=30,
            pady=10
        )

        self.texto = ctk.CTkTextbox(
            self
        )

        self.texto.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=15
        )

        if texto_documento:

            self.texto.insert(
                "1.0",
                texto_documento
            )

        else:

            self.texto.insert(
                "1.0",
                "Nenhum texto foi extraído do documento."
            )

        botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botoes.grid(
            row=3,
            column=0,
            pady=20
        )

        ctk.CTkButton(
            botoes,
            text="Voltar",
            width=140,
            command=self.voltar_criacao
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ctk.CTkButton(
            botoes,
            text="Continuar",
            width=180,
            command=self.continuar
        ).grid(
            row=0,
            column=1,
            padx=10
        )

    def continuar(self):

        texto_atualizado = self.texto.get(
            "1.0",
            "end"
        ).strip()

        self.abrir_necessidades(
            self.dados,
            texto_atualizado
        )


# ============================================================
# TELA DE NECESSIDADES PEDAGÓGICAS
# ============================================================

class TelaNecessidades(ctk.CTkFrame):

    def __init__(
        self,
        master,
        dados,
        texto_documento,
        voltar_revisao,
        gerar_resultado
    ):
        super().__init__(master)

        self.dados = dados
        self.texto_documento = texto_documento

        self.voltar_revisao = voltar_revisao
        self.gerar_resultado = gerar_resultado

        self.opcoes = [
            "Instruções curtas e objetivas",
            "Utilizar apoio visual",
            "Dividir exercícios em etapas",
            "Facilitar a interpretação dos enunciados",
            "Destacar informações importantes",
            "Reduzir a quantidade de informações por questão",
            "Organizar informações em tópicos"
        ]

        self.checkboxes = []

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self,
            text="Necessidades pedagógicas",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        area = ctk.CTkScrollableFrame(
            self
        )

        area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )

        area.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            area,
            text=(
                "Selecione somente as necessidades pedagógicas "
                "confirmadas pelo professor."
            ),
            wraplength=800
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(10, 20)
        )

        for indice, opcao in enumerate(
            self.opcoes,
            start=1
        ):

            checkbox = ctk.CTkCheckBox(
                area,
                text=opcao
            )

            checkbox.grid(
                row=indice,
                column=0,
                sticky="w",
                pady=7
            )

            self.checkboxes.append(
                checkbox
            )

            if opcao in self.dados.get(
                "necessidades_aluno",
                []
            ):

                checkbox.select()

        ctk.CTkLabel(
            area,
            text="Observações do professor:"
        ).grid(
            row=len(self.opcoes) + 1,
            column=0,
            sticky="w",
            pady=(25, 5)
        )

        self.observacoes = ctk.CTkTextbox(
            area,
            height=120
        )

        self.observacoes.grid(
            row=len(self.opcoes) + 2,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botoes.grid(
            row=2,
            column=0,
            pady=20
        )

        ctk.CTkButton(
            botoes,
            text="Voltar",
            width=140,
            command=self.voltar_revisao
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ctk.CTkButton(
            botoes,
            text="Gerar atividade com IA",
            width=220,
            command=self.confirmar
        ).grid(
            row=0,
            column=1,
            padx=10
        )

    def confirmar(self):

        necessidades = []

        for checkbox in self.checkboxes:

            if checkbox.get():

                necessidades.append(
                    checkbox.cget("text")
                )

        necessidades = list(
            dict.fromkeys(
                necessidades
            )
        )

        observacoes = self.observacoes.get(
            "1.0",
            "end"
        ).strip()

        atividade = Atividade(

            ano=self.dados["ano"],

            disciplina=self.dados["disciplina"],

            conteudo=self.dados["conteudo"],

            objetivo=self.dados["objetivo"],

            quantidade=self.dados["quantidade"],

            tipo=self.dados["tipo"],

            observacoes=(
                self.dados["observacoes"]
                + (
                    "\n\n" + observacoes
                    if observacoes
                    else ""
                )
            ).strip(),

            atividade_original=self.dados[
                "atividade_original"
            ],

            texto_documento=self.texto_documento,

            necessidades_pedagogicas=necessidades,

            aluno_id=self.dados.get(
                "aluno_id"
            ),

            aluno_nome=self.dados.get(
                "aluno_nome",
                ""
            )
        )

        self.gerar_resultado(
            atividade
        )


# ============================================================
# TELA DE RESULTADO
# ============================================================

class TelaResultado(ctk.CTkFrame):

    def __init__(
        self,
        master,
        atividade,
        resultado,
        voltar_inicio,
        gerar_nova_versao
    ):
        super().__init__(master)

        self.atividade = atividade
        self.resultado = resultado

        self.voltar_inicio = voltar_inicio
        self.gerar_nova_versao = gerar_nova_versao

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self,
            text="Atividade gerada pela IA",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        self.texto_resultado = ctk.CTkTextbox(
            self
        )

        self.texto_resultado.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=15
        )

        self.texto_resultado.insert(
            "1.0",
            resultado
        )

        botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botoes.grid(
            row=2,
            column=0,
            pady=20
        )

        # ====================================================
        # COPIAR
        # ====================================================

        ctk.CTkButton(
            botoes,
            text="Copiar resultado",
            width=160,
            command=self.copiar
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        # ====================================================
        # PDF DA ATIVIDADE
        # ====================================================

        ctk.CTkButton(
            botoes,
            text="📄 Salvar atividade em PDF",
            width=210,
            command=self.salvar_atividade_pdf
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        # ====================================================
        # PDF DO GABARITO
        # ====================================================

        ctk.CTkButton(
            botoes,
            text="📄 Salvar gabarito em PDF",
            width=210,
            command=self.salvar_gabarito_pdf
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        # ====================================================
        # NOVA VERSÃO
        # ====================================================

        ctk.CTkButton(
            botoes,
            text="Gerar nova versão",
            width=180,
            command=self.nova_versao
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=10
        )

        # ====================================================
        # VOLTAR
        # ====================================================

        ctk.CTkButton(
            botoes,
            text="Voltar ao início",
            width=160,
            command=self.voltar_inicio
        ).grid(
            row=1,
            column=1,
            padx=8,
            pady=10
        )

    # ========================================================
    # COPIAR
    # ========================================================

    def copiar(self):

        texto = self.texto_resultado.get(
            "1.0",
            "end"
        ).strip()

        self.clipboard_clear()

        self.clipboard_append(
            texto
        )

        messagebox.showinfo(
            "Copiado",
            "O resultado foi copiado para a área de transferência."
        )

    # ========================================================
    # SALVAR ATIVIDADE EM PDF
    # ========================================================

    def salvar_atividade_pdf(self):

        try:

            # Pega o texto atual da tela.
            # Assim, se o professor editar a atividade,
            # o PDF recebe a versão editada.
            resultado_atual = self.texto_resultado.get(
                "1.0",
                "end"
            ).strip()

            pasta = filedialog.askdirectory(
                title="Escolha onde salvar a atividade"
            )

            if not pasta:
                return

            caminho = criar_pdf_atividade(
                self.atividade,
                resultado_atual,
                pasta
            )

            messagebox.showinfo(
                "PDF criado",
                (
                    "A atividade foi salva com sucesso!\n\n"
                    f"Arquivo:\n{caminho}"
                )
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao criar PDF",
                (
                    "Não foi possível criar o PDF da atividade.\n\n"
                    f"Detalhes:\n{erro}"
                )
            )

    # ========================================================
    # SALVAR GABARITO EM PDF
    # ========================================================

    def salvar_gabarito_pdf(self):

        try:

            resultado_atual = self.texto_resultado.get(
                "1.0",
                "end"
            ).strip()

            pasta = filedialog.askdirectory(
                title="Escolha onde salvar o gabarito"
            )

            if not pasta:
                return

            caminho = criar_pdf_gabarito(
                self.atividade,
                resultado_atual,
                pasta
            )

            messagebox.showinfo(
                "PDF criado",
                (
                    "O gabarito foi salvo com sucesso!\n\n"
                    f"Arquivo:\n{caminho}"
                )
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao criar PDF",
                (
                    "Não foi possível criar o PDF do gabarito.\n\n"
                    f"Detalhes:\n{erro}"
                )
            )

    # ========================================================
    # NOVA VERSÃO
    # ========================================================

    def nova_versao(self):

        resposta = messagebox.askyesno(
            "Gerar nova versão",
            (
                "Uma nova atividade será gerada usando "
                "as mesmas informações e necessidades pedagógicas.\n\n"
                "Deseja continuar?"
            )
        )

        if resposta:

            self.gerar_nova_versao(
                self.atividade
            )