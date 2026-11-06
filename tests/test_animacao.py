"""Testa a chegada, a subida pela rampa e a partida do onibus."""

from animacao import SequenciaAnimacao


def avancar_ate(animacao, etapa, limite=2000, passo=0.05):
    """Avanca a sequencia ate a etapa indicada."""
    for _ in range(limite):
        if animacao.etapa == etapa:
            return
        animacao.atualizar(passo)

    raise AssertionError(f"A animacao nao chegou a etapa: {etapa}")


def test_onibus_chega_e_espera_o_caracol():
    animacao = SequenciaAnimacao()
    animacao.atualizar(2.5)

    assert animacao.etapa == "aproximacao"
    assert animacao.z_onibus == animacao.ONIBUS_Z_PARADA
    assert animacao.x_caracol > animacao.CARACOL_X_PARADA
    assert animacao.onibus_esta_se_movendo() is False


def test_porta_abre_antes_do_embarque():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")

    assert animacao.porta == 1.0
    assert animacao.embarcado is False
    assert animacao.x_caracol == animacao.CARACOL_X_PARADA


def test_caracol_chega_ate_a_rampa_sem_subir_antes_da_hora():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")
    animacao.atualizar(0.9)

    assert animacao.etapa == "embarque"
    assert animacao.CARACOL_X_RAMPA < animacao.x_caracol < animacao.CARACOL_X_PARADA
    assert animacao.y_caracol == animacao.CARACOL_Y_CHAO
    assert animacao.porta == 1.0


def test_caracol_sobe_pela_rampa_e_entra_na_cabine():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")
    animacao.atualizar(2.4)

    assert animacao.etapa == "embarque"
    assert animacao.ONIBUS_X < animacao.x_caracol < animacao.CARACOL_X_RAMPA
    assert animacao.CARACOL_Y_CHAO < animacao.y_caracol < animacao.CARACOL_Y_INTERIOR
    assert animacao.porta == 1.0


def test_caracol_termina_dentro_antes_de_ser_considerado_embarcado():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "espera_embarcado")

    assert animacao.embarcado is True
    assert animacao.x_caracol == animacao.ONIBUS_X
    assert animacao.y_caracol == animacao.CARACOL_Y_INTERIOR
    assert animacao.angulo_caracol == animacao.CARACOL_ANGULO_DENTRO
    assert animacao.porta == 1.0


def test_porta_so_fecha_depois_que_o_caracol_embarca():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "fechar_porta")

    assert animacao.embarcado is True
    assert animacao.porta == 1.0

    animacao.atualizar(0.4)
    assert animacao.etapa == "fechar_porta"
    assert animacao.porta == 0.5


def test_onibus_so_parte_depois_de_fechar_a_porta():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "partida")

    assert animacao.embarcado is True
    assert animacao.porta == 0.0
    assert animacao.z_onibus == animacao.ONIBUS_Z_PARADA
    assert animacao.onibus_esta_se_movendo() is True


def test_caracol_permanece_embarcado_durante_a_partida():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "partida")
    animacao.atualizar(1.0)

    assert animacao.embarcado is True
    assert animacao.z_onibus < animacao.ONIBUS_Z_PARADA
    assert animacao.etapa == "partida"


def test_animacao_reinicia_no_final():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "reiniciar")
    animacao.atualizar(1.0)

    assert animacao.etapa == "aproximacao"
    assert animacao.embarcado is False
    assert animacao.x_caracol == animacao.CARACOL_X_INICIAL
    assert animacao.y_caracol == animacao.CARACOL_Y_CHAO
    assert animacao.z_onibus == animacao.ONIBUS_Z_INICIAL
    assert animacao.porta == 0.0


def test_delta_tempo_zero_nao_muda_a_cena():
    animacao = SequenciaAnimacao()
    estado = (
        animacao.etapa,
        animacao.x_caracol,
        animacao.y_caracol,
        animacao.z_onibus,
        animacao.porta
    )

    animacao.atualizar(0)

    assert estado == (
        animacao.etapa,
        animacao.x_caracol,
        animacao.y_caracol,
        animacao.z_onibus,
        animacao.porta
    )


def test_passos_de_tempo_diferentes_chegam_ao_mesmo_ponto():
    rapido = SequenciaAnimacao()
    lento = SequenciaAnimacao()

    avancar_ate(rapido, "abrir_porta", passo=0.01)
    avancar_ate(lento, "abrir_porta", passo=0.10)

    assert rapido.x_caracol == lento.x_caracol == rapido.CARACOL_X_PARADA
    assert rapido.z_onibus == lento.z_onibus == rapido.ONIBUS_Z_PARADA


def test_quadro_longo_respeita_a_ordem_do_embarque():
    animacao = SequenciaAnimacao()
    animacao.atualizar(9.0)

    assert animacao.etapa == "partida"
    assert animacao.embarcado is True
    assert animacao.porta == 0.0
    assert animacao.z_onibus < animacao.ONIBUS_Z_PARADA


def test_rodas_giram_so_quando_o_onibus_anda():
    animacao = SequenciaAnimacao()

    assert animacao.onibus_esta_se_movendo() is True

    animacao.atualizar(2.5)
    assert animacao.onibus_esta_se_movendo() is False

    avancar_ate(animacao, "partida")
    assert animacao.onibus_esta_se_movendo() is True
