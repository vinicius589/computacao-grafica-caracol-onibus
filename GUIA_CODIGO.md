# Guia para entender o código

Este guia explica os trechos mais importantes em linguagem simples. Para apresentar, comece por main.py e depois mostre a lógica de animacao.py.

## 1. Como iniciar o programa

No final de main.py existe uma função main(). Ela cria a aplicação e chama run(), que pertence ao framework. O framework abre a janela e chama os métodos initialize() e update().

A condição no final do arquivo faz a função main() ser executada quando main.py é aberto diretamente.

## 2. Como o código está dividido

- main.py: monta e desenha a cena.
- animacao.py: controla a ordem dos movimentos.
- py3d/: contém as classes do framework, os materiais e os shaders.
- assets/asfalto.png: textura do chão.
- tests/: verifica a sequência sem precisar abrir a janela 3D.

## 3. Funções principais de main.py

- criar_material(cor, textura): prepara a cor e a iluminação de uma peça.
- adicionar_peca(grupo, geometria, material, posicao): cria uma malha e coloca no grupo.
- initialize(): prepara câmera, luzes, materiais, cenário e personagens.
- criar_ambiente(): monta a rua e o ponto de ônibus.
- criar_onibus(): monta a carroceria, as rodas, a porta e as aberturas da cabine.
- criar_caracol(): monta corpo, casco, sensor e antenas.
- update(): atualiza os movimentos e chama o renderizador.
- main(): inicia a aplicação.

## 4. Como o ônibus deixa o caracol visível

A carroceria inferior forma o piso. A lateral de embarque é feita com colunas separadas, deixando espaços abertos entre elas. O teto também usa barras, em vez de uma placa fechada.

Isso permite ver o caracol atravessando a porta e depois dentro da cabine.

## 5. Por que o caracol acompanha o ônibus

O caracol é adicionado ao grupo do ônibus com a chamada self.onibus.add(self.caracol).

Isso cria uma relação hierárquica. Antes de embarcar, o programa calcula a posição local do caracol para que ele caminhe até a porta. Depois do embarque, o caracol fica na posição local fixa [0, altura, 0].

Como essa posição é relativa ao grupo do ônibus, quando o ônibus se desloca, o caracol acompanha automaticamente.

## 6. Como funciona animacao.py

A classe SequenciaAnimacao guarda:

- x_caracol: posição do caracol no percurso.
- y_caracol: altura do caracol.
- z_onibus: posição do ônibus.
- porta: abertura da porta, de 0 (fechada) a 1 (aberta).
- embarcado: informa se o caracol já está dentro.
- etapa: parte atual da sequência.
- tempo_etapa: tempo passado na etapa atual.

As etapas são:

1. aproximacao: o ônibus chega e espera o caracol no ponto.
2. abrir_porta: a porta desliza e libera a entrada.
3. embarque: o caracol atravessa a abertura e sobe para o piso da cabine.
4. espera_embarcado: o caracol já está dentro e o ônibus aguarda.
5. fechar_porta: a porta fecha depois do embarque.
6. partida: o ônibus sai com o caracol dentro.
7. reiniciar: pausa curta antes de repetir a cena.

A função interpolar(inicio, fim, progresso) calcula posições intermediárias. Assim, o movimento é gradual, sem saltar diretamente de uma posição para outra.

## 7. O que é delta time

delta_time é o tempo decorrido desde o quadro anterior. A animação usa esse valor para avançar o tempo da etapa. Assim, a velocidade não depende diretamente da quantidade de quadros por segundo.

O método atualizar() também aproveita o tempo que sobrar de um quadro longo na etapa seguinte. Isso evita que uma atualização demorada deixe a sequência atrasada.

## 8. Transformações e hierarquia

- Translação muda a posição: set_position().
- Rotação muda a orientação: rotate_x(), rotate_y() e rotate_z().
- Escala muda o tamanho: scale().
- Hierarquia organiza objetos dentro de grupos: self.onibus.add(self.caracol).

## 9. Câmera, pausa e controles

A câmera usa perspectiva e o MovementRig lê as teclas. Espaço alterna a variável pausado: a animação para, mas a câmera continua funcionando.

## 10. Textura, iluminação e sombras

O arquivo assets/asfalto.png é carregado por Texture e aplicado ao chão. As geometrias fornecem coordenadas UV.

A luz ambiente ilumina a cena de forma geral. A luz direcional representa uma fonte de luz em uma direção. O material Phong usa as normais dos vértices para calcular a iluminação.

O shadow mapping faz uma passagem pela câmera da luz e grava a profundidade dos objetos. Depois, o shader Phong consulta esse mapa para decidir se um ponto está atrás de outro objeto e deve receber sombra.

Os arquivos principais são:

- py3d/material/phong.py: shader Phong e leitura do mapa de sombra.
- py3d/material/depth.py: shader da passagem de profundidade.
- py3d/core_ext/renderer.py: executa as passagens de sombra e de imagem.
- py3d/light/shadow.py: configura a câmera e a textura de sombra.

## 11. Perguntas que podem aparecer

**Como sabemos que o caracol está dentro?**
A posição dele passa pela porta e termina dentro do grupo do ônibus. Depois, fica em uma posição local fixa dentro da cabine.

**Por que o caracol acompanha o ônibus?**
Porque ele é filho do grupo do ônibus. A transformação do pai também afeta os filhos.

**Como evitamos que a porta feche antes da entrada?**
O controlador só passa para a etapa de fechar depois de terminar a etapa de embarque.

**Como a animação não depende do FPS?**
Ela usa o tempo decorrido, chamado delta time, e calcula o progresso de cada etapa.

**Qual a diferença entre iluminação e sombra?**
A iluminação calcula como a luz atinge a superfície. A sombra projetada verifica se outro objeto bloqueia a luz naquele ponto.
