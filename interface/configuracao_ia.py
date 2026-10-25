import customtkinter as ctk
from tkinter import messagebox
import webbrowser

from documentos.chave_gemini import (

    salvar_chave,
    obter_chave,
    existe_chave,
    remover_chave
)

from config.settings import GEMINI_MODEL


class TelaConfiguracaoIA(ctk.CTkFrame):

    def __init__(
        self,
        master,
        voltar
    ):

        super().__init__(
            master
        )

        self.voltar = voltar

        self.chave_visivel = False

        self.criar_interface()

        self.carregar_status()

    # ========================================================
    # INTERFACE PRINCIPAL
    # ========================================================

    def criar_interface(self):

        container = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=40
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = ctk.CTkLabel(
            container,
            text="⚙️ Configurar Inteligência Artificial",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 10)
        )

        # ====================================================
        # EXPLICAÇÃO
        # ====================================================

        explicacao = ctk.CTkLabel(
            container,
            text=(
                "O AdaptaIA utiliza o Google Gemini para gerar "
                "atividades adaptadas.\n\n"
                "Cada professor pode configurar sua própria "
                "chave da API do Gemini."
            ),
            font=ctk.CTkFont(
                size=15
            ),
            justify="center",
            wraplength=700
        )

        explicacao.pack(
            pady=(5, 15)
        )

        # ====================================================
        # BOTÃO DO TUTORIAL
        # ====================================================

        botao_tutorial = ctk.CTkButton(
            container,
            text="📖 Como conseguir minha chave?",
            width=260,
            height=42,
            command=self.mostrar_tutorial
        )

        botao_tutorial.pack(
            pady=(5, 20)
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.status.pack(
            pady=(0, 15)
        )

        # ====================================================
        # LABEL
        # ====================================================

        label_chave = ctk.CTkLabel(
            container,
            text="Chave da API do Gemini:",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        label_chave.pack(
            anchor="w",
            padx=100
        )

        # ====================================================
        # CAMPO DA CHAVE
        # ====================================================

        linha_chave = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        linha_chave.pack(
            fill="x",
            padx=100,
            pady=(8, 15)
        )

        self.campo_chave = ctk.CTkEntry(
            linha_chave,
            height=42,
            placeholder_text="Cole aqui sua chave da API",
            show="*"
        )

        self.campo_chave.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.botao_mostrar = ctk.CTkButton(
            linha_chave,
            text="Mostrar",
            width=100,
            height=42,
            command=self.alternar_visibilidade
        )

        self.botao_mostrar.pack(
            side="left",
            padx=(10, 0)
        )

        # ====================================================
        # LINK PARA O AI STUDIO
        # ====================================================

        botao_site = ctk.CTkButton(
            container,
            text="🌐 Abrir Google AI Studio",
            width=250,
            height=40,
            command=self.abrir_google_ai_studio
        )

        botao_site.pack(
            pady=(0, 20)
        )

        # ====================================================
        # BOTÕES PRINCIPAIS
        # ====================================================

        botoes = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        botoes.pack(
            pady=5
        )

        self.botao_testar = ctk.CTkButton(
            botoes,
            text="🔎 Testar conexão",
            width=180,
            height=42,
            command=self.testar_conexao
        )

        self.botao_testar.grid(
            row=0,
            column=0,
            padx=8,
            pady=8
        )

        self.botao_salvar = ctk.CTkButton(
            botoes,
            text="💾 Salvar chave",
            width=180,
            height=42,
            command=self.salvar
        )

        self.botao_salvar.grid(
            row=0,
            column=1,
            padx=8,
            pady=8
        )

        self.botao_remover = ctk.CTkButton(
            botoes,
            text="🗑 Remover chave",
            width=180,
            height=42,
            command=self.remover
        )

        self.botao_remover.grid(
            row=0,
            column=2,
            padx=8,
            pady=8
        )

        # ====================================================
        # AVISO
        # ====================================================

        aviso = ctk.CTkLabel(
            container,
            text=(
                "⚠️ Nunca compartilhe sua chave da API.\n"
                "Não publique sua chave no GitHub ou em código público."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            justify="center"
        )

        aviso.pack(
            pady=(15, 15)
        )

        # ====================================================
        # VOLTAR
        # ====================================================

        botao_voltar = ctk.CTkButton(
            container,
            text="← Voltar ao início",
            width=200,
            height=40,
            command=self.voltar
        )

        botao_voltar.pack(
            pady=(5, 25)
        )

    # ========================================================
    # STATUS
    # ========================================================

    def carregar_status(self):

        if existe_chave():

            self.status.configure(
                text="✓ Uma chave do Gemini já está configurada."
            )

        else:

            self.status.configure(
                text="⚠ Nenhuma chave do Gemini configurada."
            )

    # ========================================================
    # ABRIR GOOGLE AI STUDIO
    # ========================================================

    def abrir_google_ai_studio(self):

        webbrowser.open(
            "https://aistudio.google.com/app/apikey"
        )

    # ========================================================
    # MOSTRAR / OCULTAR CHAVE
    # ========================================================

    def alternar_visibilidade(self):

        self.chave_visivel = not self.chave_visivel

        if self.chave_visivel:

            self.campo_chave.configure(
                show=""
            )

            self.botao_mostrar.configure(
                text="Ocultar"
            )

        else:

            self.campo_chave.configure(
                show="*"
            )

            self.botao_mostrar.configure(
                text="Mostrar"
            )

    # ========================================================
    # TUTORIAL
    # ========================================================

    def mostrar_tutorial(self):

        janela = ctk.CTkToplevel(
            self
        )

        janela.title(
            "Como conseguir sua chave do Gemini"
        )

        janela.geometry(
            "750x650"
        )

        janela.minsize(
            650,
            550
        )

        janela.grab_set()

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = ctk.CTkLabel(
            janela,
            text="📖 Como conseguir sua chave do Gemini",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(25, 15)
        )

        # ====================================================
        # TEXTO
        # ====================================================

        texto = ctk.CTkTextbox(
            janela,
            width=650,
            height=430,
            wrap="word"
        )

        texto.pack(
            padx=40,
            pady=10,
            fill="both",
            expand=True
        )

        tutorial = """
PASSO 1 — Acesse o Google AI Studio

Clique no botão abaixo para abrir a página oficial
do Google AI Studio.

O Google AI Studio é o local utilizado para criar
e gerenciar as chaves da API Gemini.


PASSO 2 — Entre com sua conta Google

Faça login utilizando sua conta Google.


PASSO 3 — Crie sua chave

Na página de chaves da API, procure a opção para
criar uma nova chave.

Dependendo da sua conta, o Google pode criar
automaticamente um projeto e uma chave para você.


PASSO 4 — Copie sua chave

Depois que a chave for criada, copie o código da chave.


PASSO 5 — Volte para o AdaptaIA

Cole a chave no campo:

"Chave da API do Gemini"


PASSO 6 — Teste a conexão

Clique em:

"🔎 Testar conexão"

Se a chave estiver correta, o AdaptaIA informará
que a conexão foi realizada com sucesso.


PASSO 7 — Salve a chave

Clique em:

"💾 Salvar chave"

Depois disso, o AdaptaIA poderá utilizar sua chave
para gerar atividades adaptadas.


IMPORTANTE SOBRE SEGURANÇA

Sua chave da API é pessoal.

Não envie sua chave para outras pessoas.

Não publique sua chave no GitHub.

Não coloque sua chave diretamente em códigos públicos.


SOBRE CUSTOS

A utilização da API depende das condições da sua
conta, projeto, modelo e nível de uso.

Caso você configure faturamento ou utilize recursos
pagos, o uso pode gerar custos na conta associada
ao projeto.

Consulte o Google AI Studio e o Google Cloud para
acompanhar o uso e as condições de faturamento.
"""

        texto.insert(
            "1.0",
            tutorial
        )

        texto.configure(
            state="disabled"
        )

        # ====================================================
        # BOTÃO GOOGLE AI STUDIO
        # ====================================================

        botao_site = ctk.CTkButton(
            janela,
            text="🌐 Abrir Google AI Studio",
            width=260,
            height=42,
            command=self.abrir_google_ai_studio
        )

        botao_site.pack(
            pady=10
        )

        # ====================================================
        # FECHAR
        # ====================================================

        botao_fechar = ctk.CTkButton(
            janela,
            text="Fechar",
            width=180,
            height=38,
            command=janela.destroy
        )

        botao_fechar.pack(
            pady=(0, 20)
        )

    # ========================================================
    # SALVAR
    # ========================================================

    def salvar(self):

        chave = self.campo_chave.get().strip()

        if not chave:

            messagebox.showwarning(
                "Chave não informada",
                "Digite sua chave da API do Gemini."
            )

            return

        try:

            salvar_chave(
                chave
            )

            self.status.configure(
                text="✓ Chave salva com sucesso."
            )

            self.campo_chave.delete(
                0,
                "end"
            )

            messagebox.showinfo(
                "Chave salva",
                (
                    "A chave da API do Gemini foi salva "
                    "com sucesso.\n\n"
                    "Agora você pode voltar ao início "
                    "e criar uma atividade."
                )
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar a chave.\n\n{erro}"
            )

    # ========================================================
    # TESTAR CONEXÃO
    # ========================================================

    def testar_conexao(self):

        chave = self.campo_chave.get().strip()

        if not chave:

            chave = obter_chave()

        if not chave:

            messagebox.showwarning(
                "Chave não encontrada",
                (
                    "Informe uma chave da API do Gemini "
                    "antes de testar."
                )
            )

            return

        try:

            self.botao_testar.configure(
                state="disabled",
                text="Testando..."
            )

            self.update()

            from google import genai

            cliente = genai.Client(
                api_key=chave
            )

            cliente.models.get(
                model=GEMINI_MODEL
            )

            self.status.configure(
                text="✓ Conexão com o Gemini realizada com sucesso."
            )

            messagebox.showinfo(
                "Conexão funcionando",
                (
                    "A chave do Gemini está funcionando "
                    "corretamente."
                )
            )

        except Exception as erro:

            self.status.configure(
                text="✗ Não foi possível validar a chave."
            )

            messagebox.showerror(
                "Erro na conexão",
                (
                    "Não foi possível conectar ao Gemini.\n\n"
                    "Verifique se a chave está correta e se "
                    "há conexão com a internet.\n\n"
                    f"Detalhes:\n{erro}"
                )
            )

        finally:

            self.botao_testar.configure(
                state="normal",
                text="🔎 Testar conexão"
            )

    # ========================================================
    # REMOVER CHAVE
    # ========================================================

    def remover(self):

        if not existe_chave():

            messagebox.showinfo(
                "Nenhuma chave",
                "Não existe uma chave configurada."
            )

            return

        confirmar = messagebox.askyesno(
            "Remover chave",
            (
                "Tem certeza que deseja remover a chave "
                "da API do Gemini deste computador?"
            )
        )

        if not confirmar:

            return

        try:

            remover_chave()

            self.campo_chave.delete(
                0,
                "end"
            )

            self.status.configure(
                text="⚠ Nenhuma chave do Gemini configurada."
            )

            messagebox.showinfo(
                "Chave removida",
                "A chave da API foi removida com sucesso."
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível remover a chave.\n\n{erro}"
            )