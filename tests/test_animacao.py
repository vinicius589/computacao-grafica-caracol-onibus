"""Testa a sequencia de chegada, embarque e partida."""

from animacao import SequenciaAnimacao


def avancar_ate(animacao, etapa, limite=2000, passo=0.05):
    """Avanca a animacao ate a etapa informada."""
    for _ in range(limite):
        if animacao.etapa == etapa:
            return
        animacao.atualizar(passo)
    raise AssertionError(f"A animacao nao chegou a etapa: {etapa}")


def test_onibus_chega_primeiro_e_espera_o_caracol():
    animacao = SequenciaAnimacao()
    animacao.atualizar(2.5)

    assert animacao.etapa == "aproximacao"
    assert animacao.z_onibus == 1.2
    assert animacao.x_caracol > 0.25
    assert animacao.onibus_esta_se_movendo() is False


def test_onibus_e_caracol_terminam_a_aproximacao():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "abrir_porta")

    assert animacao.x_caracol == 0.25
    assert animacao.z_onibus == 1.2
    assert animacao.porta == 0.0
    assert animacao.embarcado is False


def test_porta_abre_antes_de_o_caracol_entrar():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")

    assert animacao.porta == 1.0
    assert animacao.embarcado is False
    assert animacao.x_caracol == 0.25


def test_caracol_avanca_pela_porta_durante_o_embarque():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")
    animacao.atualizar(1.1)

    assert animacao.etapa == "embarque"
    assert -2.3 < animacao.x_caracol < 0.25
    assert animacao.y_caracol > animacao.CARACOL_Y_CHAO
    assert animacao.porta == 1.0
    assert animacao.embarcado is False


def test_caracol_fica_dentro_ao_terminar_o_embarque():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "embarque")
    animacao.atualizar(2.2)

    assert animacao.etapa == "espera_embarcado"
    assert animacao.embarcado is True
    assert animacao.x_caracol == -2.3
    assert animacao.y_caracol == 0.92
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
    assert animacao.z_onibus == 1.2
    assert animacao.onibus_esta_se_movendo() is True


def test_caracol_permanece_embarcado_durante_a_partida():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "partida")
    animacao.atualizar(1.0)

    assert animacao.embarcado is True
    assert animacao.z_onibus < 1.2
    assert animacao.etapa == "partida"


def test_animacao_reinicia_e_o_caracol_desembarca_para_o_proximo_ciclo():
    animacao = SequenciaAnimacao()
    avancar_ate(animacao, "reiniciar")
    animacao.atualizar(1.0)

    assert animacao.etapa == "aproximacao"
    assert animacao.embarcado is False
    assert animacao.x_caracol == 3.6
    assert animacao.z_onibus == 6.0
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

    assert rapido.x_caracol == lento.x_caracol == 0.25
    assert rapido.z_onibus == lento.z_onibus == 1.2


def test_um_quadro_longo_nao_pula_o_embarque():
    animacao = SequenciaAnimacao()
    animacao.atualizar(8.0)

    assert animacao.etapa == "partida"
    assert animacao.embarcado is True
    assert animacao.porta == 0.0
    assert animacao.z_onibus < 1.2


def test_rodas_giram_so_quando_o_onibus_anda():
    animacao = SequenciaAnimacao()

    assert animacao.onibus_esta_se_movendo() is True

    animacao.atualizar(2.5)
    assert animacao.onibus_esta_se_movendo() is False

    avancar_ate(animacao, "partida")
    assert animacao.onibus_esta_se_movendo() is True
