# Resultado dos testes automatizados

## Testes previstos nesta revisão

A suíte de animação foi executada localmente: **13 testes passaram**. Ela verifica:
- O ônibus chega primeiro e espera o caracol.
- Os dois chegam antes da abertura da porta.
- A porta abre antes do embarque.
- O caracol atravessa a porta durante a etapa de embarque.
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

Os 13 testes automatizados cobrem a lógica da sequência. A janela gráfica ainda deve ser executada no Windows para conferir visualmente a entrada pela porta, a visibilidade do passageiro, a textura, a câmera, a iluminação e as sombras. A revisão desta branch não substitui esse teste visual.

Execute INICIAR.bat para abrir a cena e TESTAR.bat para repetir os testes.
