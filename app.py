import customtkinter as ctk

from interface.telas import (
    TelaInicial,
    TelaCriacao,
    TelaRevisao,
    TelaNecessidades,
    TelaResultado
)

from interface.alunos import TelaAlunos

from interface.configuracao_ia import (
    TelaConfiguracaoIA
)

from banco.database import inicializar_banco

from historico.repositorio import salvar_atividade


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "AdaptaIA"
        )

        self.geometry(
            "1000x700"
        )

        self.minsize(
            800,
            600
        )

        inicializar_banco()

        self.mostrar_inicio()

    # ========================================================
    # LIMPAR TELA
    # ========================================================

    def limpar_tela(self):

        for widget in self.winfo_children():

            widget.destroy()

    # ========================================================
    # TELA INICIAL
    # ========================================================

    def mostrar_inicio(self):

        self.limpar_tela()

        tela = TelaInicial(
            self,
            self.mostrar_criacao
        )

        tela.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # CONFIGURAÇÃO DA IA
        # ----------------------------------------------------

        botao_configuracao = ctk.CTkButton(
            self,
            text="⚙️ Configurar Inteligência Artificial",
            width=260,
            height=40,
            command=self.mostrar_configuracao_ia
        )

        botao_configuracao.place(
            relx=0.5,
            rely=0.82,
            anchor="center"
        )

        # ----------------------------------------------------
        # ALUNOS
        # ----------------------------------------------------

        botao_alunos = ctk.CTkButton(
            self,
            text="👥 Gerenciar alunos",
            width=200,
            height=40,
            command=self.mostrar_alunos
        )

        botao_alunos.place(
            relx=0.5,
            rely=0.92,
            anchor="center"
        )

    # ========================================================
    # CONFIGURAÇÃO DA IA
    # ========================================================

    def mostrar_configuracao_ia(self):

        self.limpar_tela()

        tela = TelaConfiguracaoIA(
            self,
            self.mostrar_inicio
        )

        tela.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # ALUNOS
    # ========================================================

    def mostrar_alunos(self):

        self.limpar_tela()

        tela = TelaAlunos(
            self,
            self.mostrar_inicio
        )

        tela.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # CRIAÇÃO
    # ========================================================

    def mostrar_criacao(self):

        self.limpar_tela()

        tela = TelaCriacao(
            self,
            self.mostrar_inicio,
            self.mostrar_revisao
        )

        tela.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # REVISÃO
    # ========================================================

    def mostrar_revisao(
        self,
        dados,
        texto_documento
    ):

        self.limpar_tela()

        tela = TelaRevisao(
            self,
            dados,
            texto_documento,
            self.mostrar_criacao,
            self.mostrar_necessidades
        )

        tela.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # NECESSIDADES
    # ========================================================

    def mostrar_necessidades(
        self,
        dados,
        texto_documento
    ):

        self.limpar_tela()

        tela = TelaNecessidades(
            self,
            dados,
            texto_documento,
            self.mostrar_revisao_voltar,
            self.gerar_atividade
        )

        tela.pack(
            fill="both",
            expand=True
        )

    def mostrar_revisao_voltar(self):

        self.mostrar_criacao()

    # ========================================================
    # GERAR ATIVIDADE
    # ========================================================

    def gerar_atividade(
        self,
        atividade
    ):

        self.mostrar_carregando()

        self.update()

        try:

            from ia.gemini import (
                gerar_atividade
            )

            resultado = gerar_atividade(
                atividade
            )

            # Salva automaticamente no histórico
            salvar_atividade(
                atividade,
                resultado
            )

            self.mostrar_resultado(
                atividade,
                resultado
            )

        except Exception as erro:

            self.mostrar_erro(
                erro
            )

    # ========================================================
    # CARREGANDO
    # ========================================================

    def mostrar_carregando(self):

        self.limpar_tela()

        carregando = ctk.CTkFrame(
            self
        )

        carregando.pack(
            fill="both",
            expand=True
        )

        mensagem = ctk.CTkLabel(
            carregando,
            text=(
                "🤖 Gerando atividade...\n\n"
                "O AdaptaIA está consultando o Gemini.\n\n"
                "Isso pode levar alguns segundos."
            ),
            font=ctk.CTkFont(
                size=20
            ),
            justify="center"
        )

        mensagem.pack(
            expand=True
        )

    # ========================================================
    # RESULTADO
    # ========================================================

    def mostrar_resultado(
        self,
        atividade,
        resultado
    ):

        self.limpar_tela()

        tela = TelaResultado(
            self,
            atividade,
            resultado,
            self.mostrar_inicio,
            self.gerar_nova_versao
        )

        tela.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # NOVA VERSÃO
    # ========================================================

    def gerar_nova_versao(
        self,
        atividade
    ):

        self.mostrar_carregando()

        self.update()

        try:

            from ia.gemini import (
                gerar_atividade
            )

            resultado = gerar_atividade(
                atividade
            )

            # Também salva a nova versão
            salvar_atividade(
                atividade,
                resultado
            )

            self.mostrar_resultado(
                atividade,
                resultado
            )

        except Exception as erro:

            self.mostrar_erro(
                erro
            )

    # ========================================================
    # ERRO
    # ========================================================

    def mostrar_erro(
        self,
        erro
    ):

        self.limpar_tela()

        tela = ctk.CTkFrame(
            self
        )

        tela.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            tela,
            text="Não foi possível gerar a atividade",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(100, 20)
        )

        ctk.CTkLabel(
            tela,
            text=(
                "Ocorreu um erro ao conversar com o Gemini.\n\n"
                "Verifique a conexão com a internet e tente novamente."
            ),
            wraplength=700
        ).pack(
            pady=10
        )

        ctk.CTkLabel(
            tela,
            text=f"Detalhes técnicos:\n{erro}",
            wraplength=800
        ).pack(
            pady=20
        )

        ctk.CTkButton(
            tela,
            text="Voltar ao início",
            width=180,
            command=self.mostrar_inicio
        ).pack(
            pady=20
        )


if __name__ == "__main__":

    app = App()

    app.mainloop()