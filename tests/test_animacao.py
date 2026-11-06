"""Testes da sequencia do caracol e do onibus usando apenas Python."""

import unittest

from animacao import SequenciaAnimacao


def avancar_ate(animacao, etapa, limite=2000, passo=0.05):
    """Avanca a animacao ate chegar na etapa pedida."""
    for _ in range(limite):
        if animacao.etapa == etapa:
            return
        animacao.atualizar(passo)

    raise AssertionError(f"A animacao nao chegou a etapa: {etapa}")


class TestarAnimacao(unittest.TestCase):
    """Confere a ordem dos movimentos sem abrir a janela 3D."""

    def test_onibus_chega_e_espera_o_caracol(self):
        animacao = SequenciaAnimacao()
        animacao.atualizar(2.5)

        self.assertEqual(animacao.etapa, "aproximacao")
        self.assertEqual(animacao.z_onibus, animacao.ONIBUS_Z_PARADA)
        self.assertGreater(animacao.x_caracol, animacao.CARACOL_X_PARADA)
        self.assertFalse(animacao.onibus_esta_se_movendo())

    def test_porta_abre_antes_do_embarque(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "embarque")

        self.assertEqual(animacao.porta, 1.0)
        self.assertFalse(animacao.embarcado)
        self.assertEqual(animacao.x_caracol, animacao.CARACOL_X_PARADA)

    def test_caracol_chega_ate_a_rampa_sem_subir_antes_da_hora(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "embarque")
        animacao.atualizar(0.9)

        self.assertEqual(animacao.etapa, "embarque")
        self.assertGreater(animacao.x_caracol, animacao.CARACOL_X_RAMPA)
        self.assertLess(animacao.x_caracol, animacao.CARACOL_X_PARADA)
        self.assertEqual(animacao.y_caracol, animacao.CARACOL_Y_CHAO)
        self.assertEqual(animacao.porta, 1.0)

    def test_caracol_sobe_pela_rampa_e_entra_na_cabine(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "embarque")
        animacao.atualizar(2.4)

        self.assertEqual(animacao.etapa, "embarque")
        self.assertGreater(animacao.x_caracol, animacao.ONIBUS_X)
        self.assertLess(animacao.x_caracol, animacao.CARACOL_X_RAMPA)
        self.assertGreater(animacao.y_caracol, animacao.CARACOL_Y_CHAO)
        self.assertLess(animacao.y_caracol, animacao.CARACOL_Y_INTERIOR)
        self.assertEqual(animacao.porta, 1.0)

    def test_caracol_termina_dentro_antes_de_ser_embarcado(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "espera_embarcado")

        self.assertTrue(animacao.embarcado)
        self.assertEqual(animacao.x_caracol, animacao.CARACOL_X_INTERIOR)
        self.assertEqual(animacao.y_caracol, animacao.CARACOL_Y_INTERIOR)
        self.assertEqual(animacao.angulo_caracol, animacao.CARACOL_ANGULO_DENTRO)
        self.assertEqual(animacao.porta, 1.0)

    def test_porta_so_fecha_depois_que_o_caracol_embarca(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "fechar_porta")

        self.assertTrue(animacao.embarcado)
        self.assertEqual(animacao.porta, 1.0)

        animacao.atualizar(0.4)
        self.assertEqual(animacao.etapa, "fechar_porta")
        self.assertAlmostEqual(animacao.porta, 0.5)

    def test_onibus_so_parte_depois_de_fechar_a_porta(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "partida")

        self.assertTrue(animacao.embarcado)
        self.assertEqual(animacao.porta, 0.0)
        self.assertEqual(animacao.z_onibus, animacao.ONIBUS_Z_PARADA)
        self.assertTrue(animacao.onibus_esta_se_movendo())

    def test_caracol_permanece_embarcado_durante_a_partida(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "partida")
        animacao.atualizar(1.0)

        self.assertTrue(animacao.embarcado)
        self.assertLess(animacao.z_onibus, animacao.ONIBUS_Z_PARADA)
        self.assertEqual(animacao.etapa, "partida")

    def test_animacao_reinicia_no_final(self):
        animacao = SequenciaAnimacao()
        avancar_ate(animacao, "reiniciar")
        animacao.atualizar(1.0)

        self.assertEqual(animacao.etapa, "aproximacao")
        self.assertFalse(animacao.embarcado)
        self.assertEqual(animacao.x_caracol, animacao.CARACOL_X_INICIAL)
        self.assertEqual(animacao.y_caracol, animacao.CARACOL_Y_CHAO)
        self.assertEqual(animacao.z_onibus, animacao.ONIBUS_Z_INICIAL)
        self.assertEqual(animacao.porta, 0.0)

    def test_delta_tempo_zero_nao_muda_a_cena(self):
        animacao = SequenciaAnimacao()
        estado = (
            animacao.etapa,
            animacao.x_caracol,
            animacao.y_caracol,
            animacao.z_onibus,
            animacao.porta
        )

        animacao.atualizar(0)

        estado_atual = (
            animacao.etapa,
            animacao.x_caracol,
            animacao.y_caracol,
            animacao.z_onibus,
            animacao.porta
        )
        self.assertEqual(estado, estado_atual)

    def test_passos_de_tempo_diferentes_chegam_ao_mesmo_ponto(self):
        rapido = SequenciaAnimacao()
        lento = SequenciaAnimacao()

        avancar_ate(rapido, "abrir_porta", passo=0.01)
        avancar_ate(lento, "abrir_porta", passo=0.10)

        self.assertEqual(rapido.x_caracol, lento.x_caracol)
        self.assertEqual(rapido.z_onibus, lento.z_onibus)

    def test_quadro_longo_respeita_a_ordem_do_embarque(self):
        animacao = SequenciaAnimacao()
        animacao.atualizar(9.0)

        self.assertEqual(animacao.etapa, "partida")
        self.assertTrue(animacao.embarcado)
        self.assertEqual(animacao.porta, 0.0)
        self.assertLess(animacao.z_onibus, animacao.ONIBUS_Z_PARADA)

    def test_rodas_giram_so_quando_o_onibus_anda(self):
        animacao = SequenciaAnimacao()
        self.assertTrue(animacao.onibus_esta_se_movendo())

        animacao.atualizar(2.5)
        self.assertFalse(animacao.onibus_esta_se_movendo())

        avancar_ate(animacao, "partida")
        self.assertTrue(animacao.onibus_esta_se_movendo())


if __name__ == "__main__":
    unittest.main()
