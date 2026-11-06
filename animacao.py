"""Controla a chegada do onibus e o embarque do caracol."""


class SequenciaAnimacao:
    """Guarda as posicoes e a etapa atual da animacao."""

    # Posicoes usadas na cena.
    ONIBUS_X = -2.3
    ONIBUS_Z_INICIAL = 6.0
    ONIBUS_Z_PARADA = 1.2
    ONIBUS_Z_FINAL = -6.0

    CARACOL_X_INICIAL = 3.6
    CARACOL_X_PARADA = 0.25
    CARACOL_Y_CHAO = -0.07
    CARACOL_Y_INTERIOR = 0.92
    CARACOL_ANGULO_FORA = 3.141592653589793
    CARACOL_ANGULO_DENTRO = 1.5707963267948966

    # Tempo de cada etapa, em segundos.
    DURACOES = {
        "aproximacao": 3.35,
        "abrir_porta": 0.8,
        "embarque": 2.2,
        "espera_embarcado": 0.8,
        "fechar_porta": 0.8,
        "partida": 3.0,
        "reiniciar": 1.0,
    }

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        """Coloca o onibus e o caracol nas posicoes iniciais."""
        self.etapa = "aproximacao"
        self.tempo_etapa = 0.0

        self.x_caracol = self.CARACOL_X_INICIAL
        self.y_caracol = self.CARACOL_Y_CHAO
        self.z_onibus = self.ONIBUS_Z_INICIAL

        self.porta = 0.0
        self.embarcado = False
        self.angulo_caracol = self.CARACOL_ANGULO_FORA

    def interpolar(self, inicio, fim, progresso):
        """Calcula um valor entre inicio e fim."""
        return inicio + (fim - inicio) * progresso

    def atualizar_posicoes(self):
        """Calcula as posicoes de acordo com a etapa atual."""
        duracao = self.DURACOES[self.etapa]
        progresso = min(self.tempo_etapa / duracao, 1.0)

        if self.etapa == "aproximacao":
            # O caracol caminha ate o ponto.
            self.x_caracol = self.interpolar(
                self.CARACOL_X_INICIAL,
                self.CARACOL_X_PARADA,
                progresso
            )

            # O onibus chega antes e espera o caracol.
            progresso_onibus = min(self.tempo_etapa / 2.4, 1.0)
            self.z_onibus = self.interpolar(
                self.ONIBUS_Z_INICIAL,
                self.ONIBUS_Z_PARADA,
                progresso_onibus
            )

        elif self.etapa == "abrir_porta":
            self.porta = progresso

        elif self.etapa == "embarque":
            # O caracol atravessa a porta e sobe para o piso do onibus.
            self.x_caracol = self.interpolar(
                self.CARACOL_X_PARADA,
                self.ONIBUS_X,
                progresso
            )
            self.y_caracol = self.interpolar(
                self.CARACOL_Y_CHAO,
                self.CARACOL_Y_INTERIOR,
                progresso
            )

            # Ao entrar, o caracol vira para a frente do onibus.
            self.angulo_caracol = self.interpolar(
                self.CARACOL_ANGULO_FORA,
                self.CARACOL_ANGULO_DENTRO,
                progresso
            )

        elif self.etapa == "espera_embarcado":
            self.porta = 1.0

        elif self.etapa == "fechar_porta":
            self.porta = 1.0 - progresso

        elif self.etapa == "partida":
            # O caracol ja esta dentro e acompanha o grupo do onibus.
            self.z_onibus = self.interpolar(
                self.ONIBUS_Z_PARADA,
                self.ONIBUS_Z_FINAL,
                progresso
            )

        elif self.etapa == "reiniciar":
            self.z_onibus = self.ONIBUS_Z_FINAL

    def avancar_etapa(self):
        """Passa para a proxima parte da sequencia."""
        proximas_etapas = {
            "aproximacao": "abrir_porta",
            "abrir_porta": "embarque",
            "embarque": "espera_embarcado",
            "espera_embarcado": "fechar_porta",
            "fechar_porta": "partida",
            "partida": "reiniciar",
        }

        if self.etapa == "embarque":
            # A partir daqui, o caracol fica preso ao grupo do onibus.
            self.embarcado = True

        if self.etapa == "reiniciar":
            self.reiniciar()
            return

        self.etapa = proximas_etapas[self.etapa]
        self.tempo_etapa = 0.0
        self.atualizar_posicoes()

    def atualizar(self, delta_tempo):
        """Avanca a animacao usando o tempo decorrido, sem depender do FPS."""
        if delta_tempo <= 0:
            return

        tempo_restante = delta_tempo

        # Se um quadro demorar mais, o tempo que sobrar continua na proxima etapa.
        while tempo_restante > 0:
            duracao = self.DURACOES[self.etapa]
            falta = duracao - self.tempo_etapa

            passo = min(tempo_restante, falta)
            self.tempo_etapa += passo
            tempo_restante -= passo

            self.atualizar_posicoes()

            if self.tempo_etapa >= duracao - 0.000000001:
                self.avancar_etapa()

    def onibus_esta_se_movendo(self):
        """Informa quando as rodas devem girar."""
        return self.etapa == "partida" or (
            self.etapa == "aproximacao" and self.tempo_etapa < 2.4
        )
