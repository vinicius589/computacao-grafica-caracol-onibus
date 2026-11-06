# Roteiro de apresentação - Computação Gráfica

## 1. Apresentação da ideia

A cena representa um ponto de ônibus. O caracol chega, espera o ônibus, caminha até a porta lateral, sobe pela rampa e entra na cabine. A porta fecha e o ônibus parte com o passageiro.

## 2. Demonstração

1. Mostre o caracol chegando ao ponto.
2. Mostre o ônibus parando e aguardando.
3. Mostre as duas folhas da porta girando para fora.
4. Mostre o caracol caminhando até a entrada.
5. Mostre o caracol subindo pela rampa e chegando ao piso da cabine.
6. Mostre as duas folhas voltando aos batentes depois que ele entra.
7. Mostre o ônibus saindo com o caracol dentro.

A câmera permite observar a cabine pela entrada lateral e pela abertura central do teto. O banco e a placa ficam na calçada, afastados do caminho do caracol.

## 3. Controles

- W/S, A/D, R/F: movimentar a câmera.
- Q/E: girar a câmera.
- T/G: olhar para cima e para baixo.
- Espaço: pausar e retomar a animação.

## 4. Explicação do código

Comece pelo final do main.py e mostre a função main(). Depois explique initialize(), criar_onibus(), criar_caracol() e update().

Em seguida, abra animacao.py. Explique as etapas da sequência e mostre que o valor da porta vai de fechada a aberta e volta a zero antes da partida. No main.py, mostre que cada folha gira em torno de um eixo que é filho do grupo do ônibus.

## 5. Conceitos gráficos

- Modelagem por composição de formas geométricas.
- Translação, rotação, escala e hierarquia.
- Câmera em perspectiva.
- Textura com coordenadas UV.
- Iluminação Phong e vetores normais.
- Shadow mapping.
- Animação baseada em delta time.
- Relação hierárquica: o caracol é filho do ônibus e acompanha a partida.

## 6. Pergunta importante

**Como o caracol permanece dentro quando o ônibus sai?**

Ele é adicionado ao grupo do ônibus. Depois de subir pela rampa e chegar ao piso, sua posição local fica fixa dentro da cabine. Quando o grupo do ônibus se desloca, o caracol acompanha a mesma transformação.

## 7. Antes da apresentação

- Confirmar os temas sorteados e os nomes dos integrantes.
- Executar o projeto no computador da apresentação.
- Testar entrada, fechamento da porta e partida.
- Demonstrar câmera, pausa, textura, iluminação e sombra.
- Cada integrante deve saber explicar o código e sua contribuição real.
