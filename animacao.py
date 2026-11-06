"""Controla a chegada do onibus e o embarque do caracol."""


class SequenciaAnimacao:
    """Guarda as posicoes e a etapa atual da animacao."""

    # Posicoes do onibus.
    ONIBUS_X = -2.3
    CARACOL_X_INTERIOR = ONIBUS_X + 0.18
    ONIBUS_Z_INICIAL = 6.0
    ONIBUS_Z_PARADA = 1.2
    ONIBUS_Z_FINAL = -6.0

    # Posicoes do caracol.
    CARACOL_X_INICIAL = 3.6
    CARACOL_X_PARADA = 0.25
    CARACOL_X_RAMPA = -1.05
    CARACOL_Y_CHAO = 0.16
    CARACOL_Y_INTERIOR = 1.15
    CARACOL_ANGULO_FORA = 3.141592653589793
    CARACOL_ANGULO_DENTRO = 1.5707963267948966

    # Parte do embarque usada para chegar ate a rampa.
    PROGRESSO_ATE_RAMPA = 0.55

    # Duracao de cada parte da animacao, em segundos.
    DURACOES = {
        "aproximacao": 3.35,
        "abrir_porta": 0.8,
        "embarque": 3.0,
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

    def limitar_progresso(self, progresso):
        """Mantem o progresso entre zero e um."""
        return max(0.0, min(1.0, progresso))

    def suavizar(self, progresso):
        """Deixa o inicio e o fim do movimento mais suaves."""
        progresso = self.limitar_progresso(progresso)
        return progresso * progresso * (3 - 2 * progresso)

    def interpolar(self, inicio, fim, progresso):
        """Calcula uma posicao entre o inicio e o fim."""
        progresso = self.limitar_progresso(progresso)

        # Garante os valores exatos no inicio e no fim do movimento.
        if progresso == 0:
            return inicio
        if progresso == 1:
            return fim

        return inicio + (fim - inicio) * progresso

    def atualizar_posicoes(self):
        """Atualiza as posicoes de acordo com a etapa atual."""
        duracao = self.DURACOES[self.etapa]
        progresso = self.limitar_progresso(self.tempo_etapa / duracao)

        if self.etapa == "aproximacao":
            # O caracol caminha ate o ponto.
            self.x_caracol = self.interpolar(
                self.CARACOL_X_INICIAL,
                self.CARACOL_X_PARADA,
                self.suavizar(progresso)
            )

            # O onibus chega primeiro e espera o caracol.
            progresso_onibus = self.suavizar(self.tempo_etapa / 2.4)
            self.z_onibus = self.interpolar(
                self.ONIBUS_Z_INICIAL,
                self.ONIBUS_Z_PARADA,
                progresso_onibus
            )

        elif self.etapa == "abrir_porta":
            self.porta = progresso

        elif self.etapa == "embarque":
            # Primeiro, o caracol anda ate a entrada sem subir do chao.
            if progresso <= self.PROGRESSO_ATE_RAMPA:
                progresso_entrada = self.suavizar(
                    progresso / self.PROGRESSO_ATE_RAMPA
                )
                self.x_caracol = self.interpolar(
                    self.CARACOL_X_PARADA,
                    self.CARACOL_X_RAMPA,
                    progresso_entrada
                )
                self.y_caracol = self.CARACOL_Y_CHAO

            # Depois, sobe pela rampa e entra completamente na cabine.
            else:
                progresso_rampa = self.suavizar(
                    (progresso - self.PROGRESSO_ATE_RAMPA)
                    / (1.0 - self.PROGRESSO_ATE_RAMPA)
                )
                self.x_caracol = self.interpolar(
                    self.CARACOL_X_RAMPA,
                    self.CARACOL_X_INTERIOR,
                    progresso_rampa
                )
                self.y_caracol = self.interpolar(
                    self.CARACOL_Y_CHAO,
                    self.CARACOL_Y_INTERIOR,
                    progresso_rampa
                )

            # O caracol vira para a frente enquanto termina de embarcar.
            self.angulo_caracol = self.interpolar(
                self.CARACOL_ANGULO_FORA,
                self.CARACOL_ANGULO_DENTRO,
                self.suavizar(progresso)
            )

        elif self.etapa == "espera_embarcado":
            self.porta = 1.0

        elif self.etapa == "fechar_porta":
            self.porta = 1.0 - progresso

        elif self.etapa == "partida":
            # O caracol ja esta preso ao grupo do onibus.
            self.z_onibus = self.interpolar(
                self.ONIBUS_Z_PARADA,
                self.ONIBUS_Z_FINAL,
                self.suavizar(progresso)
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

        # Ao terminar o embarque, o caracol passa a ser passageiro.
        if self.etapa == "embarque":
            self.embarcado = True

        if self.etapa == "reiniciar":
            self.reiniciar()
            return

        self.etapa = proximas_etapas[self.etapa]
        self.tempo_etapa = 0.0
        self.atualizar_posicoes()

    def atualizar(self, delta_tempo):
        """Avanca a animacao pelo tempo, sem depender do FPS."""
        if delta_tempo <= 0:
            return

        tempo_restante = delta_tempo

        # Aproveita o tempo que sobrar quando uma etapa terminar.
        while tempo_restante > 0.000000001:
            duracao = self.DURACOES[self.etapa]
            falta = duracao - self.tempo_etapa
            passo = min(tempo_restante, falta)

            self.tempo_etapa += passo
            tempo_restante -= passo
            self.atualizar_posicoes()

            if self.tempo_etapa >= duracao - 0.000000001:
                self.avancar_etapa()

            if tempo_restante < 0.000000001:
                tempo_restante = 0.0

    def onibus_esta_se_movendo(self):
        """Informa quando as rodas devem girar."""
        return self.etapa == "partida" or (
            self.etapa == "aproximacao" and self.tempo_etapa < 2.4
        )
