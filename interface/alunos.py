import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from alunos.repositorio import (
    cadastrar_aluno,
    listar_alunos,
    buscar_aluno,
    buscar_necessidades,
    buscar_documentos,
    atualizar_aluno,
    adicionar_documento,
    excluir_aluno
)


# ============================================================
# TELA DE GERENCIAMENTO
# ============================================================

class TelaAlunos(ctk.CTkFrame):

    def __init__(
        self,
        master,
        voltar_inicio
    ):

        super().__init__(master)

        self.voltar_inicio = voltar_inicio

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Gerenciar alunos",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(25, 10)
        )

        # ----------------------------------------------------
        # BOTÕES SUPERIORES
        # ----------------------------------------------------

        barra = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        barra.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=30,
            pady=10
        )

        ctk.CTkButton(
            barra,
            text="+ Novo aluno",
            width=160,
            command=self.novo_aluno
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            barra,
            text="Voltar ao início",
            width=160,
            command=self.voltar_inicio
        ).pack(
            side="right",
            padx=5
        )

        # ----------------------------------------------------
        # LISTA
        # ----------------------------------------------------

        self.lista = ctk.CTkScrollableFrame(
            self
        )

        self.lista.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )

        self.lista.grid_columnconfigure(
            0,
            weight=1
        )

        self.carregar_alunos()

    # ========================================================
    # CARREGAR ALUNOS
    # ========================================================

    def carregar_alunos(self):

        for widget in self.lista.winfo_children():

            widget.destroy()

        alunos = listar_alunos()

        if not alunos:

            ctk.CTkLabel(
                self.lista,
                text=(
                    "Nenhum aluno cadastrado ainda.\n\n"
                    "Clique em '+ Novo aluno' para cadastrar."
                ),
                font=ctk.CTkFont(
                    size=16
                )
            ).grid(
                row=0,
                column=0,
                pady=80
            )

            return

        for indice, aluno in enumerate(
            alunos
        ):

            card = ctk.CTkFrame(
                self.lista
            )

            card.grid(
                row=indice,
                column=0,
                sticky="ew",
                pady=8
            )

            card.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                card,
                text=aluno["nome"],
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=15,
                pady=(12, 2)
            )

            ctk.CTkLabel(
                card,
                text=aluno["turma"]
            ).grid(
                row=1,
                column=0,
                sticky="w",
                padx=15,
                pady=(0, 12)
            )

            ctk.CTkButton(
                card,
                text="Abrir",
                width=100,
                command=lambda id_aluno=aluno["id"]:
                    self.abrir_aluno(id_aluno)
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                padx=15,
                pady=10
            )

    # ========================================================
    # NOVO ALUNO
    # ========================================================

    def novo_aluno(self):

        TelaFormularioAluno(
            self,
            titulo="Cadastrar aluno",
            salvar_callback=self.salvar_novo_aluno
        )

    # ========================================================
    # SALVAR NOVO
    # ========================================================

    def salvar_novo_aluno(
        self,
        dados
    ):

        try:

            cadastrar_aluno(
                nome=dados["nome"],
                turma=dados["turma"],
                necessidades=dados["necessidades"],
                observacoes=dados["observacoes"],
                caminho_documento=dados["documento"]
            )

            messagebox.showinfo(
                "Aluno cadastrado",
                "O aluno foi cadastrado com sucesso."
            )

            self.carregar_alunos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível cadastrar o aluno.\n\n{erro}"
            )

    # ========================================================
    # ABRIR ALUNO
    # ========================================================

    def abrir_aluno(
        self,
        aluno_id
    ):

        TelaDetalhesAluno(
            self,
            aluno_id,
            atualizar_lista=self.carregar_alunos
        )


# ============================================================
# FORMULÁRIO DE ALUNO
# ============================================================

class TelaFormularioAluno(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        titulo,
        salvar_callback,
        aluno_id=None
    ):

        super().__init__(master)

        self.title(
            titulo
        )

        self.geometry(
            "700x700"
        )

        self.minsize(
            600,
            600
        )

        self.salvar_callback = salvar_callback
        self.aluno_id = aluno_id

        self.documento = ""

        # ----------------------------------------------------
        # CAMPOS
        # ----------------------------------------------------

        container = ctk.CTkScrollableFrame(
            self
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            container,
            text="Nome do aluno:"
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.nome = ctk.CTkEntry(
            container,
            placeholder_text="Ex.: João da Silva"
        )

        self.nome.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            container,
            text="Turma:"
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.turma = ctk.CTkEntry(
            container,
            placeholder_text="Ex.: 3º ano do Ensino Médio"
        )

        self.turma.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            container,
            text="Necessidades pedagógicas:"
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.checkboxes = []

        opcoes = [
            "Instruções curtas e objetivas",
            "Utilizar apoio visual",
            "Dividir exercícios em etapas",
            "Facilitar a interpretação dos enunciados",
            "Destacar informações importantes",
            "Reduzir a quantidade de informações por questão",
            "Organizar informações em tópicos"
        ]

        for opcao in opcoes:

            checkbox = ctk.CTkCheckBox(
                container,
                text=opcao
            )

            checkbox.pack(
                anchor="w",
                pady=5
            )

            self.checkboxes.append(
                checkbox
            )

        ctk.CTkLabel(
            container,
            text="Observações pedagógicas:"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.observacoes = ctk.CTkTextbox(
            container,
            height=120
        )

        self.observacoes.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            container,
            text="Laudo / documento pedagógico:"
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        linha_documento = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        linha_documento.pack(
            fill="x",
            pady=(0, 20)
        )

        linha_documento.grid_columnconfigure(
            0,
            weight=1
        )

        self.caminho_label = ctk.CTkLabel(
            linha_documento,
            text="Nenhum documento selecionado",
            anchor="w"
        )

        self.caminho_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        ctk.CTkButton(
            linha_documento,
            text="Selecionar",
            width=130,
            command=self.selecionar_documento
        ).grid(
            row=0,
            column=1
        )

        ctk.CTkButton(
            container,
            text="Salvar aluno",
            height=45,
            command=self.salvar
        ).pack(
            fill="x",
            pady=10
        )

    # ========================================================
    # SELECIONAR DOCUMENTO
    # ========================================================

    def selecionar_documento(self):

        caminho = filedialog.askopenfilename(
            title="Selecionar laudo ou documento",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if caminho:

            self.documento = caminho

            self.caminho_label.configure(
                text=caminho
            )

    # ========================================================
    # SALVAR
    # ========================================================

    def salvar(self):

        nome = self.nome.get().strip()

        turma = self.turma.get().strip()

        observacoes = self.observacoes.get(
            "1.0",
            "end"
        ).strip()

        if not nome:

            messagebox.showwarning(
                "Campo obrigatório",
                "Informe o nome do aluno."
            )

            return

        if not turma:

            messagebox.showwarning(
                "Campo obrigatório",
                "Informe a turma do aluno."
            )

            return

        necessidades = []

        for checkbox in self.checkboxes:

            if checkbox.get():

                necessidades.append(
                    checkbox.cget("text")
                )

        dados = {
            "nome": nome,
            "turma": turma,
            "necessidades": necessidades,
            "observacoes": observacoes,
            "documento": self.documento
        }

        self.salvar_callback(
            dados
        )

        self.destroy()


# ============================================================
# DETALHES DO ALUNO
# ============================================================

class TelaDetalhesAluno(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        aluno_id,
        atualizar_lista
    ):

        super().__init__(master)

        self.title(
            "Dados do aluno"
        )

        self.geometry(
            "750x700"
        )

        self.aluno_id = aluno_id
        self.atualizar_lista = atualizar_lista

        aluno = buscar_aluno(
            aluno_id
        )

        if not aluno:

            messagebox.showerror(
                "Erro",
                "Aluno não encontrado."
            )

            self.destroy()

            return

        self.aluno = aluno

        container = ctk.CTkScrollableFrame(
            self
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ----------------------------------------------------
        # DADOS
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text=aluno["nome"],
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        ctk.CTkLabel(
            container,
            text=f"Turma: {aluno['turma']}"
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # NECESSIDADES
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Necessidades pedagógicas",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(10, 10)
        )

        necessidades = buscar_necessidades(
            aluno_id
        )

        if necessidades:

            for necessidade in necessidades:

                ctk.CTkLabel(
                    container,
                    text=f"• {necessidade['descricao']}"
                ).pack(
                    anchor="w",
                    pady=3
                )

        else:

            ctk.CTkLabel(
                container,
                text="Nenhuma necessidade cadastrada."
            ).pack(
                anchor="w"
            )

        # ----------------------------------------------------
        # OBSERVAÇÕES
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Observações",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(25, 10)
        )

        ctk.CTkLabel(
            container,
            text=aluno["observacoes"] or "Nenhuma observação.",
            wraplength=650,
            justify="left"
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # DOCUMENTOS
        # ----------------------------------------------------

        ctk.CTkLabel(
            container,
            text="Documentos",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(25, 10)
        )

        documentos = buscar_documentos(
            aluno_id
        )

        if documentos:

            for documento in documentos:

                ctk.CTkLabel(
                    container,
                    text=f"📄 {documento['nome_arquivo']}",
                    wraplength=650
                ).pack(
                    anchor="w",
                    pady=3
                )

        else:

            ctk.CTkLabel(
                container,
                text="Nenhum documento cadastrado."
            ).pack(
                anchor="w"
            )

        # ----------------------------------------------------
        # BOTÃO ADICIONAR DOCUMENTO
        # ----------------------------------------------------

        ctk.CTkButton(
            container,
            text="Adicionar documento",
            command=self.adicionar_documento
        ).pack(
            fill="x",
            pady=(15, 5)
        )

        # ----------------------------------------------------
        # EDITAR
        # ----------------------------------------------------

        ctk.CTkButton(
            container,
            text="Editar aluno",
            command=self.editar
        ).pack(
            fill="x",
            pady=5
        )

        # ----------------------------------------------------
        # EXCLUIR
        # ----------------------------------------------------

        ctk.CTkButton(
            container,
            text="Excluir aluno",
            command=self.excluir,
            fg_color="#8B0000",
            hover_color="#A52A2A"
        ).pack(
            fill="x",
            pady=5
        )

    # ========================================================
    # ADICIONAR DOCUMENTO
    # ========================================================

    def adicionar_documento(self):

        caminho = filedialog.askopenfilename(
            title="Adicionar documento",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:

            return

        try:

            adicionar_documento(
                self.aluno_id,
                caminho
            )

            messagebox.showinfo(
                "Documento",
                "Documento adicionado com sucesso."
            )

            self.destroy()

            TelaDetalhesAluno(
                self.master,
                self.aluno_id,
                self.atualizar_lista
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível adicionar o documento.\n\n{erro}"
            )

    # ========================================================
    # EDITAR
    # ========================================================

    def editar(self):

        TelaEditarAluno(
            self,
            self.aluno_id,
            self.atualizar_lista
        )

    # ========================================================
    # EXCLUIR
    # ========================================================

    def excluir(self):

        resposta = messagebox.askyesno(
            "Excluir aluno",
            (
                "Tem certeza que deseja excluir este aluno?\n\n"
                "Os documentos armazenados para este aluno "
                "também serão removidos."
            )
        )

        if not resposta:

            return

        try:

            excluir_aluno(
                self.aluno_id
            )

            messagebox.showinfo(
                "Aluno excluído",
                "O aluno foi excluído com sucesso."
            )

            self.atualizar_lista()

            self.destroy()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível excluir o aluno.\n\n{erro}"
            )


# ============================================================
# EDIÇÃO DO ALUNO
# ============================================================

class TelaEditarAluno(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        aluno_id,
        atualizar_lista
    ):

        super().__init__(master)

        self.title(
            "Editar aluno"
        )

        self.geometry(
            "700x650"
        )

        self.aluno_id = aluno_id
        self.atualizar_lista = atualizar_lista

        aluno = buscar_aluno(
            aluno_id
        )

        necessidades = buscar_necessidades(
            aluno_id
        )

        necessidades_texto = [
            item["descricao"]
            for item in necessidades
        ]

        container = ctk.CTkScrollableFrame(
            self
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # NOME

        ctk.CTkLabel(
            container,
            text="Nome do aluno:"
        ).pack(
            anchor="w",
            pady=5
        )

        self.nome = ctk.CTkEntry(
            container
        )

        self.nome.pack(
            fill="x",
            pady=(0, 15)
        )

        self.nome.insert(
            0,
            aluno["nome"]
        )

        # TURMA

        ctk.CTkLabel(
            container,
            text="Turma:"
        ).pack(
            anchor="w",
            pady=5
        )

        self.turma = ctk.CTkEntry(
            container
        )

        self.turma.pack(
            fill="x",
            pady=(0, 15)
        )

        self.turma.insert(
            0,
            aluno["turma"]
        )

        # NECESSIDADES

        ctk.CTkLabel(
            container,
            text="Necessidades pedagógicas:"
        ).pack(
            anchor="w",
            pady=5
        )

        self.checkboxes = []

        opcoes = [
            "Instruções curtas e objetivas",
            "Utilizar apoio visual",
            "Dividir exercícios em etapas",
            "Facilitar a interpretação dos enunciados",
            "Destacar informações importantes",
            "Reduzir a quantidade de informações por questão",
            "Organizar informações em tópicos"
        ]

        for opcao in opcoes:

            checkbox = ctk.CTkCheckBox(
                container,
                text=opcao
            )

            checkbox.pack(
                anchor="w",
                pady=4
            )

            if opcao in necessidades_texto:

                checkbox.select()

            self.checkboxes.append(
                checkbox
            )

        # OBSERVAÇÕES

        ctk.CTkLabel(
            container,
            text="Observações:"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.observacoes = ctk.CTkTextbox(
            container,
            height=120
        )

        self.observacoes.pack(
            fill="x"
        )

        self.observacoes.insert(
            "1.0",
            aluno["observacoes"] or ""
        )

        # SALVAR

        ctk.CTkButton(
            container,
            text="Salvar alterações",
            height=45,
            command=self.salvar
        ).pack(
            fill="x",
            pady=20
        )

    def salvar(self):

        nome = self.nome.get().strip()

        turma = self.turma.get().strip()

        observacoes = self.observacoes.get(
            "1.0",
            "end"
        ).strip()

        if not nome or not turma:

            messagebox.showwarning(
                "Campos obrigatórios",
                "Nome e turma são obrigatórios."
            )

            return

        necessidades = []

        for checkbox in self.checkboxes:

            if checkbox.get():

                necessidades.append(
                    checkbox.cget("text")
                )

        try:

            atualizar_aluno(
                aluno_id=self.aluno_id,
                nome=nome,
                turma=turma,
                necessidades=necessidades,
                observacoes=observacoes
            )

            messagebox.showinfo(
                "Aluno atualizado",
                "Os dados do aluno foram atualizados."
            )

            self.atualizar_lista()

            self.destroy()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível atualizar o aluno.\n\n{erro}"
            )