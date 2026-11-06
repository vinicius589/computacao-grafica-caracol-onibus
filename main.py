"""Cena 3D: o caracol entra no onibus e viaja com ele."""

import math
from pathlib import Path

import pygame

from py3d.core.base import Base
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.group import Group
from py3d.core_ext.texture import Texture
from py3d.light.ambient import AmbientLight
from py3d.light.directional import DirectionalLight
from py3d.material.phong import PhongMaterial
from py3d.geometry.box import BoxGeometry
from py3d.geometry.sphere import SphereGeometry
from py3d.geometry.ellipsoid import EllipsoidGeometry
from py3d.geometry.cylinder import CylinderGeometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.extras.movement_rig import MovementRig

from animacao import SequenciaAnimacao


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ASSETS = PASTA_PROJETO / "assets"

# O caracol fica visivel dentro da cabine, sem ultrapassar a carroceria.
ESCALA_CARACOL = 0.62

# Posicoes fixas do onibus na cena.
ONIBUS_X = SequenciaAnimacao.ONIBUS_X
POSICAO_CARACOL_Z = SequenciaAnimacao.ONIBUS_Z_PARADA


class TrabalhoComputacaoGrafica(Base):
    """Cria os objetos e atualiza a cena a cada quadro."""

    def __init__(self):
        super().__init__(screen_size=(1100, 720))

    def criar_material(self, cor, textura=None):
        """Cria um material com iluminacao Phong."""
        return PhongMaterial(
            texture=textura,
            number_of_light_sources=2,
            use_shadow=True,
            property_dict={"baseColor": cor}
        )

    def adicionar_peca(self, grupo, geometria, material, posicao):
        """Cria uma peca e coloca no grupo informado."""
        peca = Mesh(geometria, material)
        peca.set_position(posicao)
        grupo.add(peca)
        return peca

    def initialize(self):
        pygame.display.set_caption("Caracol embarcando no onibus")

        # Cria o renderizador, a cena e a camera.
        self.renderer = Renderer(clear_color=(0.34, 0.52, 0.68))
        self.scene = Scene()

        # A camera fica voltada para a lateral aberta do onibus e para o caracol.
        self.camera = Camera(angle_of_view=58, aspect_ratio=1100 / 720, near=0.1, far=100)
        self.camera.set_position([7.2, 5.6, 8.8])
        self.camera.look_at([-0.5, 1.0, 0.3])

        # O teclado movimenta a camera.
        self.camera_rig = MovementRig(units_per_second=4, degrees_per_second=65)
        self.camera_rig.add(self.camera)
        self.scene.add(self.camera_rig)

        # Iluminacao ambiente e direcional.
        luz_ambiente = AmbientLight(color=[0.38, 0.38, 0.42])
        luz_direcional = DirectionalLight(color=[0.95, 0.90, 0.82])
        luz_direcional.set_position([5, 10, 6])
        luz_direcional.set_direction([-0.45, -1.0, -0.55])
        self.scene.add(luz_ambiente)
        self.scene.add(luz_direcional)

        # Ativa o shadow mapping do framework.
        self.renderer.enable_shadows(luz_direcional, strength=0.58, resolution=(1024, 1024))
        self.renderer.shadow_object.camera.set_orthographic(
            left=-8, right=8, bottom=-8, top=8, near=0, far=28
        )

        # Materiais da cena.
        self.material_asfalto = self.criar_material(
            [0.78, 0.80, 0.82], Texture(str(PASTA_ASSETS / "asfalto.png"))
        )
        self.material_cinza = self.criar_material([0.22, 0.25, 0.29])
        self.material_branco = self.criar_material([0.92, 0.92, 0.88])
        self.material_amarelo = self.criar_material([0.95, 0.67, 0.12])
        self.material_azul = self.criar_material([0.08, 0.35, 0.72])
        self.material_vidro = self.criar_material([0.25, 0.72, 0.88])
        self.material_pneu = self.criar_material([0.035, 0.04, 0.05])
        self.material_metal = self.criar_material([0.52, 0.57, 0.62])
        self.material_verde = self.criar_material([0.18, 0.62, 0.43])
        self.material_casco = self.criar_material([0.72, 0.34, 0.13])
        self.material_antena = self.criar_material([0.90, 0.78, 0.30])
        self.material_luz = self.criar_material([1.0, 0.83, 0.28])

        # Monta o ambiente e os dois personagens.
        self.criar_ambiente()
        self.criar_onibus()
        self.criar_caracol()

        self.animacao = SequenciaAnimacao()
        self.pausado = False
        self.tempo_cena = 0.0
        self.angulo_antena = 0.0
        self.angulo_caracol = math.pi
        self.angulo_porta = 0.0

    def criar_ambiente(self):
        """Cria a rua e um ponto de onibus organizado fora do caminho do caracol."""
        # Asfalto de toda a cena.
        chao = self.adicionar_peca(
            self.scene, RectangleGeometry(width=24, height=22),
            self.material_asfalto, [0, 0, 0]
        )
        chao.rotate_x(-math.pi / 2)

        # Calcada e meio-fio ficam atras do percurso do caracol.
        self.adicionar_peca(
            self.scene, BoxGeometry(8.0, 0.14, 2.6), self.material_cinza,
            [2.8, 0.07, 4.0]
        )
        self.adicionar_peca(
            self.scene, BoxGeometry(8.0, 0.16, 0.18), self.material_branco,
            [2.8, 0.08, 2.68]
        )

        # Faixas da rua.
        for indice in range(6):
            self.adicionar_peca(
                self.scene, BoxGeometry(0.48, 0.025, 2.8), self.material_branco,
                [0.6 + indice * 0.58, 0.025, -2.5]
            )

        # Cobertura simples do ponto de onibus.
        for pos_x in [1.25, 4.35]:
            self.adicionar_peca(
                self.scene, CylinderGeometry(radius=0.055, height=2.35),
                self.material_metal, [pos_x, 1.25, 4.0]
            )

        self.adicionar_peca(
            self.scene, BoxGeometry(3.55, 0.14, 2.15), self.material_azul,
            [2.8, 2.48, 4.0]
        )

        # Banco: fica na calcada, longe do caminho de embarque.
        self.adicionar_peca(
            self.scene, BoxGeometry(1.6, 0.12, 0.42), self.material_amarelo,
            [2.75, 0.62, 4.15]
        )
        self.adicionar_peca(
            self.scene, BoxGeometry(1.6, 0.72, 0.12), self.material_metal,
            [2.75, 1.0, 4.34]
        )
        for pos_x in [2.15, 3.35]:
            self.adicionar_peca(
                self.scene, BoxGeometry(0.10, 0.42, 0.10), self.material_metal,
                [pos_x, 0.34, 4.15]
            )

        # Placa do ponto, afastada do caracol e da entrada do onibus.
        self.adicionar_peca(
            self.scene, CylinderGeometry(radius=0.055, height=2.0),
            self.material_metal, [5.15, 1.08, 4.0]
        )
        self.adicionar_peca(
            self.scene, BoxGeometry(0.82, 0.72, 0.12), self.material_azul,
            [5.15, 2.12, 4.0]
        )
        self.adicionar_peca(
            self.scene, BoxGeometry(0.26, 0.35, 0.04), self.material_branco,
            [5.15, 2.12, 3.93]
        )

        # Duas arvores pequenas deixam o ponto mais acolhedor sem esconder a cena.
        for pos_x in [0.0, 6.0]:
            self.adicionar_peca(
                self.scene, CylinderGeometry(radius=0.12, height=1.35),
                self.material_casco, [pos_x, 0.82, 4.85]
            )
            self.adicionar_peca(
                self.scene, SphereGeometry(radius=0.72), self.material_verde,
                [pos_x, 1.95, 4.85]
            )

    def criar_onibus(self):
        """Monta um onibus amarelo com janelas e duas portas articuladas."""
        self.onibus = Group()
        self.scene.add(self.onibus)

        # Chassi inferior e piso interno.
        self.adicionar_peca(
            self.onibus, BoxGeometry(2.0, 0.58, 3.8), self.material_amarelo,
            [0, 0.62, 0]
        )
        self.adicionar_peca(
            self.onibus, BoxGeometry(1.72, 0.08, 3.5), self.material_cinza,
            [0, 0.95, 0]
        )

        # Rampa inclinada que liga o chao ao piso do onibus.
        rampa = self.adicionar_peca(
            self.onibus, BoxGeometry(1.30, 0.12, 1.15), self.material_metal,
            [0.60, 0.48, -0.05]
        )
        rampa.rotate_z(-0.75)

        # Laterais inferiores: a entrada central permanece livre.
        for lado in [-1, 1]:
            for pos_z in [-1.30, 1.30]:
                self.adicionar_peca(
                    self.onibus, BoxGeometry(0.08, 0.52, 0.82),
                    self.material_amarelo, [lado * 0.99, 0.68, pos_z]
                )

        # Janelas do lado oposto ao embarque.
        for pos_z in [-1.20, 0.0, 1.20]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.055, 0.78, 0.88),
                self.material_vidro, [-1.0, 1.76, pos_z]
            )

        # Janelas do lado de embarque, uma de cada lado das portas.
        for pos_z in [-1.32, 1.32]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.055, 0.78, 0.76),
                self.material_vidro, [1.0, 1.76, pos_z]
            )

        # Colunas da carroceria e batentes que delimitam as portas.
        for pos_z in [-1.78, -0.90, 0.90, 1.78]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.12, 1.58, 0.13),
                self.material_amarelo, [0.99, 1.75, pos_z]
            )

        # A lateral oposta tambem recebe colunas e contornos amarelos.
        for pos_z in [-1.78, -0.60, 0.60, 1.78]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.12, 1.58, 0.13),
                self.material_amarelo, [-0.99, 1.75, pos_z]
            )

        # Duas partes da porta se abrem para fora, cada uma em seu proprio eixo.
        # Como os grupos sao filhos do onibus, acompanham a carroceria sem
        # recalcular posicoes globais a cada quadro.
        self.porta_esquerda = Group()
        self.porta_esquerda.set_position([1.04, 1.72, -0.90])
        self.onibus.add(self.porta_esquerda)

        self.adicionar_peca(
            self.porta_esquerda, BoxGeometry(0.06, 1.48, 0.90),
            self.material_azul, [0, 0, 0.45]
        )
        self.adicionar_peca(
            self.porta_esquerda, BoxGeometry(0.035, 0.20, 0.035),
            self.material_metal, [0.045, 0, 0.80]
        )

        self.porta_direita = Group()
        self.porta_direita.set_position([1.04, 1.72, 0.90])
        self.onibus.add(self.porta_direita)

        self.adicionar_peca(
            self.porta_direita, BoxGeometry(0.06, 1.48, 0.90),
            self.material_azul, [0, 0, -0.45]
        )
        self.adicionar_peca(
            self.porta_direita, BoxGeometry(0.035, 0.20, 0.035),
            self.material_metal, [0.045, 0, -0.80]
        )

        # Teto com duas partes: reforca o formato do onibus, mas deixa
        # uma abertura central para a camera mostrar o caracol.
        for lado in [-1, 1]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.16, 0.18, 3.55),
                self.material_amarelo, [lado * 0.86, 2.62, 0]
            )

        for pos_z in [-1.70, 1.70]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(1.84, 0.18, 0.16),
                self.material_amarelo, [0, 2.62, pos_z]
            )

        for pos_z in [-1.30, 1.30]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(1.72, 0.14, 0.92),
                self.material_amarelo, [0, 2.62, pos_z]
            )

        # Para-brisa dianteiro e vidro traseiro.
        self.adicionar_peca(
            self.onibus, BoxGeometry(1.58, 0.84, 0.055), self.material_vidro,
            [0, 1.78, -1.92]
        )
        self.adicionar_peca(
            self.onibus, BoxGeometry(1.58, 0.84, 0.055), self.material_vidro,
            [0, 1.78, 1.92]
        )

        # Faixa de identificacao acima do para-brisa.
        self.adicionar_peca(
            self.onibus, BoxGeometry(1.10, 0.22, 0.10), self.material_cinza,
            [0, 2.25, -1.93]
        )

        # Para-choques dianteiro e traseiro.
        self.adicionar_peca(
            self.onibus, BoxGeometry(2.05, 0.18, 0.14), self.material_metal,
            [0, 0.42, -1.98]
        )
        self.adicionar_peca(
            self.onibus, BoxGeometry(2.05, 0.18, 0.14), self.material_metal,
            [0, 0.42, 1.98]
        )

        # Rodas e cubos.
        self.rodas = []
        for lado in [-1, 1]:
            for pos_z in [-1.25, 1.25]:
                roda = self.adicionar_peca(
                    self.onibus, CylinderGeometry(radius=0.38, height=0.18),
                    self.material_pneu, [lado * 1.02, 0.38, pos_z]
                )
                roda.rotate_z(math.pi / 2)
                self.rodas.append(roda)

                cubo = self.adicionar_peca(
                    self.onibus, CylinderGeometry(radius=0.16, height=0.20),
                    self.material_metal, [lado * 1.02, 0.38, pos_z]
                )
                cubo.rotate_z(math.pi / 2)
                self.rodas.append(cubo)

        # Faróis e lanternas.
        for lado in [-1, 1]:
            self.adicionar_peca(
                self.onibus, SphereGeometry(radius=0.13), self.material_luz,
                [lado * 0.68, 0.68, -2.02]
            )
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.22, 0.22, 0.08), self.material_cinza,
                [lado * 0.68, 0.68, 2.02]
            )

        # Espelhos laterais ajudam a identificar a frente do veiculo.
        for lado in [-1, 1]:
            self.adicionar_peca(
                self.onibus, BoxGeometry(0.12, 0.10, 0.20), self.material_metal,
                [lado * 1.12, 1.88, -1.55]
            )

    def criar_antena(self, grupo, posicao):
        """Cria uma antena que pode se movimentar separadamente."""
        antena = Group()
        antena.set_position(posicao)
        grupo.add(antena)

        self.adicionar_peca(
            antena, CylinderGeometry(radius=0.045, height=0.48),
            self.material_antena, [0, 0.24, 0]
        )
        self.adicionar_peca(
            antena, SphereGeometry(radius=0.13), self.material_luz,
            [0, 0.49, 0]
        )
        return antena

    def criar_caracol(self):
        """Monta o caracol e coloca o grupo dentro do onibus."""
        self.caracol = Group()
        self.caracol.rotate_y(math.pi)
        self.caracol.scale(ESCALA_CARACOL)

        # O caracol e filho do onibus: depois do embarque, ele viaja junto.
        self.onibus.add(self.caracol)

        # Corpo e cabeca.
        self.adicionar_peca(
            self.caracol, EllipsoidGeometry(1.55, 0.62, 0.62),
            self.material_verde, [0, 0.43, 0]
        )
        self.adicionar_peca(
            self.caracol, EllipsoidGeometry(0.72, 0.72, 0.66),
            self.material_verde, [0.64, 0.67, 0]
        )

        # Casco e pequeno sensor.
        self.adicionar_peca(
            self.caracol, EllipsoidGeometry(1.10, 1.18, 1.00),
            self.material_casco, [-0.18, 0.93, 0]
        )
        sensor = self.adicionar_peca(
            self.caracol, SphereGeometry(radius=0.22),
            self.material_antena, [-0.18, 0.94, 0.52]
        )
        sensor.scale(0.75)

        # Duas antenas articuladas.
        self.antena_esquerda = self.criar_antena(self.caracol, [0.82, 1.02, -0.22])
        self.antena_direita = self.criar_antena(self.caracol, [0.82, 1.02, 0.22])

    def update(self):
        """Atualiza os movimentos e desenha a cena."""
        # A barra de espaco pausa ou continua a animacao.
        if self.input.is_key_down("space"):
            self.pausado = not self.pausado

        # A camera continua funcionando durante a pausa.
        self.camera_rig.update(self.input, self.delta_time)

        if not self.pausado:
            self.animacao.atualizar(self.delta_time)
            self.tempo_cena += self.delta_time

        # Move o grupo do onibus.
        self.onibus.set_position([ONIBUS_X, 0, self.animacao.z_onibus])

        # Antes do embarque, calculamos a posicao do caracol em relacao ao onibus.
        if self.animacao.embarcado:
            # Esta posicao local fixa faz o caracol viajar dentro do onibus.
            self.caracol.set_position([0, self.animacao.y_caracol, 0])
        else:
            self.caracol.set_position([
                self.animacao.x_caracol - ONIBUS_X,
                self.animacao.y_caracol,
                POSICAO_CARACOL_Z - self.animacao.z_onibus
            ])

        # Abre as duas folhas para fora, mantendo os eixos presos ao onibus.
        novo_angulo_porta = self.animacao.porta * (math.pi / 2)
        diferenca_porta = novo_angulo_porta - self.angulo_porta
        self.porta_esquerda.rotate_y(diferenca_porta)
        self.porta_direita.rotate_y(-diferenca_porta)
        self.angulo_porta = novo_angulo_porta

        # As rodas giram somente enquanto o onibus esta andando.
        if not self.pausado and self.animacao.onibus_esta_se_movendo():
            for roda in self.rodas:
                roda.rotate_y(-5.0 * self.delta_time)

        # As antenas balancam durante a chegada e o embarque.
        if self.animacao.etapa == "embarque":
            progresso = self.animacao.tempo_etapa / self.animacao.DURACOES["embarque"]
            intensidade = 0.08 + 0.20 * progresso
        elif self.animacao.etapa == "espera_embarcado":
            progresso = self.animacao.tempo_etapa / self.animacao.DURACOES["espera_embarcado"]
            intensidade = 0.28 - 0.20 * progresso
        else:
            intensidade = 0.08

        novo_angulo_antena = math.sin(self.tempo_cena * 5.0) * intensidade
        diferenca_antena = novo_angulo_antena - self.angulo_antena
        self.antena_esquerda.rotate_z(diferenca_antena)
        self.antena_direita.rotate_z(-diferenca_antena)
        self.angulo_antena = novo_angulo_antena

        # Vira o caracol para a frente quando ele termina de entrar.
        diferenca_caracol = self.animacao.angulo_caracol - self.angulo_caracol
        self.caracol.rotate_y(diferenca_caracol)
        self.angulo_caracol = self.animacao.angulo_caracol

        # O renderer atualiza a cena e o mapa de sombras a cada quadro.
        self.renderer.render(self.scene, self.camera)


# PONTO DE ENTRADA DO PROJETO
# Para iniciar a cena, execute: python main.py

def main():
    """Cria a aplicacao e inicia o loop principal do framework."""
    aplicacao = TrabalhoComputacaoGrafica()
    aplicacao.run()


# Esta condicao chama main() somente quando este arquivo e executado diretamente.
if __name__ == "__main__":
    main()
