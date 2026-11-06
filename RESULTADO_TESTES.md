# Resultado dos testes automatizados

## Testes previstos nesta revisão

A lógica da animação foi executada localmente nesta revisão: **13 testes passaram**. Eles verificam:
- O ônibus chega primeiro e espera o caracol.
- A porta abre antes do embarque.
- O caracol caminha até a rampa sem subir antes da hora.
- O caracol sobe pela rampa e entra na cabine.
- O caracol fica marcado como embarcado ao terminar a entrada.
- A porta só fecha depois que o caracol entra.
- O ônibus só parte depois de fechar a porta.
- O passageiro permanece embarcado durante a partida.
- O ciclo reinicia com o caracol fora do ônibus.
- Delta time zero não altera o estado.
- Passos de tempo diferentes chegam ao mesmo ponto.
- Um quadro longo aproveita o tempo restante sem pular o embarque.
- As rodas giram somente enquanto o ônibus se desloca.

## Limite da validação

Os 13 testes executados nesta revisão cobrem a lógica da sequência, incluindo a aproximação da rampa, a subida, o fechamento da porta e a partida. A janela gráfica ainda precisa ser executada no Windows para conferir visualmente a abertura das duas folhas, o encaixe do caracol na rampa, a visibilidade da cabine, o novo posicionamento do banco e da placa, a textura, a câmera, a iluminação e as sombras. Os testes automatizados não substituem essa verificação visual.

Execute INICIAR.bat para abrir a cena e TESTAR.bat para repetir os testes.
