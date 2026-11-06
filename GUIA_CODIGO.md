# Guia para entender o código

Este guia explica o projeto em linguagem simples. Para apresentar, comece pelo final de `main.py` e depois mostre `animacao.py`.

## 1. Como executar

Abra a pasta completa no PyCharm, selecione um interpretador Python já instalado (de 3.6 a 3.15), abra `main.py` e clique em **Run**.

Antes de abrir a janela, o próprio arquivo identifica a versão do Python e verifica se Pygame, PyOpenGL e NumPy podem ser importados. Caso falte alguma biblioteca, ele instala versões compatíveis usando o mesmo interpretador do PyCharm. Em Python 3.14 e 3.15, utiliza Pygame Community Edition, cujo módulo continua sendo importado como `pygame`. A pasta `py3d` já está incluída no projeto.

## 2. Como o código está dividido

- `main.py`: monta e desenha a cena.
- `animacao.py`: controla a ordem dos movimentos.
- `py3d/`: contém as classes do framework, as geometrias, os materiais e os shaders.
- `assets/asfalto.png`: textura do chão.
- `tests/test_animacao.py`: testa a lógica usando o módulo `unittest`, que já vem com Python.

## 3. Funções principais de main.py

- `obter_pacotes_compativeis()`: escolhe as versões das bibliotecas de acordo com a versão do Python.
- `preparar_bibliotecas()`: verifica e instala as três bibliotecas permitidas, se alguma estiver faltando.
- `criar_material(cor, textura)`: prepara a cor e a iluminação de uma peça.
- `adicionar_peca(grupo, geometria, material, posicao)`: cria uma peça e coloca no grupo.
- `initialize()`: prepara câmera, luzes, materiais, cenário e personagens.
- `criar_ambiente()`: monta a rua e o ponto de ônibus.
- `criar_onibus()`: monta a carroceria, as janelas, as rodas e as duas folhas da porta.
- `criar_caracol()`: monta corpo, casco, sensor e antenas.
- `update()`: atualiza os movimentos e chama o renderizador.
- `main()`: cria a aplicação e inicia o programa.

## 4. Como a porta funciona

Cada folha da porta é um grupo separado, adicionado ao grupo do ônibus. O ponto de origem de cada grupo fica na dobradiça. O valor da animação é convertido em um ângulo de rotação.

A cada quadro, o código monta novamente a matriz de posição e rotação de cada folha. Assim, a rotação é calculada a partir do valor atual da animação, sem acumular pequenos giros de quadros anteriores.

## 5. Como o caracol fica visível

O piso fica na parte inferior do ônibus. A entrada lateral permanece aberta quando as duas folhas giram para fora, e a rampa liga o chão ao piso interno. A abertura central do teto também permite observar o personagem.

O banco, a placa e as árvores ficam atrás do percurso, para não cobrir o caracol na visão inicial da câmera. Depois de embarcar, o caracol fica ligeiramente deslocado para o lado da abertura, sem sair da cabine.

## 6. Por que o caracol acompanha o ônibus

O caracol é adicionado ao grupo do ônibus com `self.onibus.add(self.caracol)`.

Isso cria uma hierarquia. Antes do embarque, o programa calcula a posição do caracol em relação ao ônibus para que ele caminhe até a porta. Depois de entrar, sua posição local fica fixa dentro da cabine.

Quando o ônibus se desloca, o caracol acompanha automaticamente porque faz parte do grupo dele.

## 7. Como funciona animacao.py

A classe `SequenciaAnimacao` guarda:

- `x_caracol`: posição do caracol no percurso.
- `y_caracol`: altura do caracol.
- `z_onibus`: posição do ônibus.
- `porta`: abertura da porta, de 0 (fechada) a 1 (aberta).
- `embarcado`: informa se o caracol já terminou de entrar.
- `etapa`: parte atual da sequência.
- `tempo_etapa`: tempo passado nessa parte.

As etapas são:

1. `aproximacao`: o ônibus chega e espera o caracol.
2. `abrir_porta`: as duas folhas giram para fora.
3. `embarque`: o caracol caminha até a entrada e sobe pela rampa.
4. `espera_embarcado`: o caracol já está dentro e o ônibus aguarda.
5. `fechar_porta`: as duas folhas voltam aos batentes.
6. `partida`: o ônibus sai com o caracol dentro.
7. `reiniciar`: pequena pausa antes de repetir.

A função `interpolar(inicio, fim, progresso)` calcula uma posição entre dois pontos. A função `suavizar(progresso)` deixa o começo e o fim do movimento mais graduais.

## 8. O que é delta time

`delta_time` é o tempo passado desde o quadro anterior. A animação usa esse valor para calcular o movimento. Assim, ela não depende diretamente da quantidade de quadros por segundo.

## 9. Transformações e hierarquia

- Translação muda a posição: `set_position()`.
- Rotação muda a orientação: `rotate_x()`, `rotate_y()` e `rotate_z()`.
- Escala muda o tamanho: `scale()`.
- Hierarquia organiza objetos em grupos: `self.onibus.add(self.caracol)`.

## 10. Câmera, pausa, textura, luz e sombra

A câmera usa perspectiva e o `MovementRig` lê as teclas. Espaço altera a variável `pausado`: a animação para, mas a câmera continua funcionando.

A textura `assets/asfalto.png` é carregada por `Texture` e aplicada ao chão. A luz ambiente ilumina a cena de maneira geral; a luz direcional representa uma fonte de luz em uma direção. O material Phong utiliza as normais das geometrias para calcular a iluminação.

O shadow mapping faz uma passagem pela câmera da luz e grava a profundidade dos objetos. Depois, o shader consulta esse mapa para calcular as sombras.

## 11. Perguntas que podem aparecer

**Como sabemos que o caracol está dentro?**

Ele termina o movimento na posição interna da cabine. Depois disso, a variável `embarcado` fica verdadeira e ele passa a acompanhar o grupo do ônibus.

**Por que o caracol acompanha o ônibus?**

Porque ele é filho do grupo do ônibus. A transformação do grupo também afeta os objetos que estão dentro dele.

**Como a porta abre sem sair do lugar?**

Cada folha gira no próprio grupo, cujo ponto de origem está na dobradiça. A posição e a rotação são recalculadas a cada quadro.

**Como a animação não depende do FPS?**

Ela usa o tempo decorrido, chamado `delta_time`, para calcular o progresso de cada etapa.
