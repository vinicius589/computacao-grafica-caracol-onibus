# Caracol robótico e ônibus de brinquedo

Projeto acadêmico de Computação Gráfica da UNIPAC, desenvolvido em Python com Pygame, PyOpenGL e NumPy, usando o framework Py3D incluído neste repositório.

## Identificação da dupla

- **Vinícius da Mota Campos** — RA: **241-007-660**
- **Miguel Felipe Viana** — RA: **241-006-978**

**Temas representados:** Caracol robótico e ônibus de brinquedo.

## Contribuições individuais

Descrever nesta seção a contribuição efetiva de cada integrante para o desenvolvimento, a implementação, os testes e a apresentação do projeto. Essa divisão deve ser conferida e preenchida pela dupla, sem atribuir tarefas que não foram realizadas.

## Cena

A cena mostra um ponto de ônibus com calçada, cobertura, banco e placa posicionados fora do caminho do personagem. O ônibus amarelo tem carroceria, janelas, rodas, para-choques e duas folhas articuladas na entrada.

O caracol robótico chega ao ponto, espera o ônibus, caminha até a entrada lateral, sobe pela rampa metálica com três faixas de apoio e entra na cabine. As portas fecham e o ônibus parte levando o caracol.

O personagem teve seu tamanho ajustado para ficar proporcional ao ônibus e permanecer visível durante o embarque. O banco, a placa e as árvores ficam na parte de trás do cenário, sem bloquear o percurso.

## Como abrir no PyCharm

1. Baixe o repositório pelo botão **Code > Download ZIP** e extraia a pasta, ou clone o repositório.
2. Abra o PyCharm e escolha **Open**.
3. Selecione a pasta completa `computacao-grafica-caracol-onibus`.
4. Selecione um interpretador Python de 3.10 a 3.14 já instalado no computador.
5. Abra o arquivo `main.py`.
6. Clique no botão **Run** (Executar).

Na primeira execução, o próprio `main.py` identifica a versão do Python selecionada e instala automaticamente as versões compatíveis de Pygame, PyOpenGL e NumPy, caso estejam faltando. É necessário ter conexão com a internet nessa primeira execução. Não é necessário instalar outra versão do Python nem criar manualmente um ambiente virtual.

A pasta `py3d` já acompanha o projeto. Não é necessário executar instalador separado, arquivo BAT ou baixar outro framework.

Ao compactar ou enviar o projeto, não inclua as pastas `.venv`, `.venv311`, `venv` ou `.idea`. Elas são configurações locais do computador e não precisam acompanhar os arquivos-fonte. O arquivo `.gitignore` já evita que essas pastas entrem no repositório.

## Bibliotecas utilizadas

- Python 3.10 a 3.14, em Windows de 64 bits.
- Pygame: janela, teclado e controle do tempo. Em Python 3.14, o instalador usa Pygame Community Edition, que mantém o módulo `pygame` utilizado pelo código.
- PyOpenGL: acesso à renderização OpenGL.
- NumPy: operações com matrizes e vetores.

As versões dos pacotes são escolhidas automaticamente conforme a versão do Python. A configuração de dependências e a cena foram verificadas no Python 3.14. A seleção de pacotes também contempla Python 3.10, 3.11, 3.12 e 3.13; a execução visual deve ser conferida no computador em que o projeto será apresentado.

Não há dependências de pytest ou de outras bibliotecas externas.

## Arquivos principais

- `main.py`: ponto de entrada. Prepara as bibliotecas, cria a janela, monta a cena e atualiza a animação.
- `animacao.py`: controla a ordem dos movimentos e as posições dos personagens e da porta.
- `py3d/`: framework incluído no projeto, com geometrias, câmera, materiais, luzes e shaders.
- `assets/asfalto.png`: textura aplicada ao chão.
- `requirements.txt`: lista das três bibliotecas usadas.
- `tests/test_animacao.py`: testes da sequência usando `unittest`, que faz parte do Python.

## Testar a lógica da animação

Os testes não são necessários para abrir a cena. Para executá-los pelo terminal do PyCharm, use:

```bash
python -m unittest discover -s tests -v
```

## Controles

- W/S: frente e trás.
- A/D: esquerda e direita.
- R/F: subir e descer.
- Q/E: girar a câmera.
- T/G: olhar para cima e para baixo.
- Espaço: pausar ou retomar a animação.

## Recursos gráficos

- Modelos montados com caixas, esferas, cilindros e elipsoides.
- Translação, rotação, escala e hierarquia de objetos.
- Câmera em perspectiva controlada pelo teclado.
- Textura de imagem com coordenadas UV.
- Luz ambiente e direcional, materiais Phong e vetores normais.
- Shadow mapping por passagem de profundidade.
- Animação baseada em delta time.
- Portas articuladas em duas folhas, presas à carroceria.
- Embarque coordenado por uma rampa; depois de entrar, o caracol acompanha o ônibus durante a partida.

## Fontes

- STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. CRC Press, 2022. DOI: https://doi.org/10.1201/9781003181378.
- Repositório público de exemplos associado ao livro: https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021 (revisão `f3029550425385f90e0d66ba7f73bb310112039b`).

