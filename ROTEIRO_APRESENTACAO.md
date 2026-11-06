# Roteiro de apresentação - Computação Gráfica

## 1. Ideia do projeto

A cena representa um ponto de ônibus. O caracol robótico chega, espera o ônibus, caminha até a entrada lateral, sobe pela rampa e entra na cabine. As duas folhas da porta fecham e o ônibus parte com o passageiro.

## 2. Demonstração

1. Mostre o caracol chegando ao ponto.
2. Mostre o ônibus parando e aguardando.
3. Mostre as duas folhas da porta abrindo para fora.
4. Mostre o caracol caminhando até a entrada.
5. Mostre o caracol subindo pela rampa e chegando ao piso.
6. Mostre as portas fechando.
7. Mostre o ônibus partindo com o caracol dentro.

A câmera permite observar a cabine pela entrada lateral e pela abertura no teto. O banco, a placa e as árvores ficam na parte de trás do cenário para não esconder a ação.

## 3. Como executar

Abra a pasta completa no PyCharm, configure Python 3.11, abra `main.py` e clique em **Run**. Na primeira execução, o arquivo instala automaticamente Pygame, PyOpenGL e NumPy se estiverem faltando.

## 4. Controles

- W/S, A/D, R/F: movimentar a câmera.
- Q/E: girar a câmera.
- T/G: olhar para cima e para baixo.
- Espaço: pausar e retomar a animação.

## 5. Explicação do código

Comece pelo final do `main.py` e mostre a função `main()`. Explique que ela cria a aplicação e chama o método `run()` do framework.

Depois mostre:

- `initialize()`: prepara a câmera, as luzes, os materiais e os objetos.
- `criar_ambiente()`: monta o ponto de ônibus.
- `criar_onibus()`: monta a carroceria, as janelas, as rodas e as portas.
- `criar_caracol()`: monta o personagem.
- `update()`: atualiza a animação e desenha a cena.

Por último, abra `animacao.py`. Explique que ele controla as etapas: aproximação, abertura, embarque, espera, fechamento, partida e reinício.

## 6. Conceitos gráficos

- Modelagem por composição de formas geométricas.
- Translação, rotação, escala e hierarquia.
- Câmera em perspectiva.
- Textura com coordenadas UV.
- Iluminação Phong e vetores normais.
- Shadow mapping.
- Animação baseada em delta time.

## 7. Perguntas importantes

**Como o caracol permanece dentro quando o ônibus sai?**

O caracol é filho do grupo do ônibus. Depois que termina o embarque, sua posição fica fixa dentro da cabine. Quando o ônibus se desloca, o caracol acompanha a mesma transformação.

**Como a porta abre?**

As duas folhas são grupos separados. Cada uma gira em torno do próprio ponto de dobradiça, usando o valor da abertura calculado pela animação.

## 8. Antes da apresentação

- Abrir e executar o projeto no computador da apresentação.
- Testar a entrada, as portas e a partida.
- Demonstrar a câmera, a pausa, a textura, a iluminação e a sombra.
- Saber explicar os métodos principais e os movimentos.
