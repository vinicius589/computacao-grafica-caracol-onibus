# Caracol robótico e ônibus de brinquedo

Projeto acadêmico de Computação Gráfica da UNIPAC, desenvolvido em Python, Pygame, OpenGL e no framework Py3D associado ao livro de Lee Stemkoski e Michael Pascale.

## Cena

A cena representa um ponto de ônibus. O caracol robótico chega ao ponto, espera o ônibus, entra pela porta lateral aberta e se posiciona dentro da cabine. A porta fecha e o ônibus parte levando o caracol.

O caracol faz parte do grupo hierárquico do ônibus. Antes do embarque, sua posição é calculada em relação ao ônibus para que ele possa caminhar até a porta. Depois de entrar, sua posição local fica fixa; assim, o movimento do ônibus leva o passageiro junto, sem uma segunda animação independente.

## Arquivos

- main.py: ponto de entrada; cria a janela, os modelos, a câmera, as luzes e a renderização.
- animacao.py: controla as etapas, os tempos, a porta e as posições do embarque.
- assets/asfalto.png: textura aplicada ao chão.
- requirements.txt: dependências Python.
- py3d/: componentes do framework e shaders usados.
- instalar_framework.py: instala o framework quando necessário.
- tests/: testes automatizados da animação e do instalador.
- GUIA_CODIGO.md: explicação do código para estudo.
- ROTEIRO_APRESENTACAO.md: roteiro de demonstração.

## Instalação no Windows

Requer Python 3.11 e conexão com a internet na primeira instalação.

1. Clone o repositório:
   git clone https://github.com/vinicius589/computacao-grafica-caracol-onibus.git
   cd computacao-grafica-caracol-onibus

2. Execute INICIAR.bat.

O BAT cria o ambiente virtual, instala as dependências, prepara o framework e abre a aplicação pelo arquivo main.py.

Para executar os testes, use TESTAR.bat.

## Executar diretamente pelo main.py

Depois de instalar as dependências e o framework, execute:

    .venv\Scripts\python.exe main.py

O arquivo main.py também possui uma função main(), que inicia a aplicação.

## Controles

- W/S: frente e trás.
- A/D: esquerda e direita.
- R/F: subir e descer.
- Q/E: girar a câmera.
- T/G: olhar para cima e para baixo.
- Espaço: pausar ou retomar a animação.

## Recursos gráficos

- Modelos montados por composição de caixas, esferas, cilindros e elipsoides.
- Translação, rotação, escala e hierarquia de objetos.
- Câmera em perspectiva controlada pelo teclado.
- Textura de imagem com coordenadas UV.
- Luz ambiente e luz direcional, materiais Phong e vetores normais.
- Shadow mapping por passagem de profundidade.
- Animação com delta time e pausa.
- Embarque coordenado: o caracol atravessa a porta, fica dentro da cabine e acompanha o ônibus durante a partida.

## Fontes

- STEMKOSKI, Lee; PASCALE, Michael. Developing Graphics Frameworks with Python and OpenGL. CRC Press, 2022. DOI: https://doi.org/10.1201/9781003181378.
- Repositório público de exemplos associado ao livro: https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021 (revisão f3029550425385f90e0d66ba7f73bb310112039b).

O projeto foi desenvolvido com apoio de IA na estruturação, comentários, testes e documentação. Os integrantes devem revisar, executar e compreender o código antes da apresentação.
