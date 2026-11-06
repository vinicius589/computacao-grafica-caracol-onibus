# Resultado dos testes automatizados

## Testes da animação

Os testes usam o módulo `unittest`, que faz parte do Python. Não é necessário instalar pytest nem outra biblioteca de testes.

A suíte verifica:
- A chegada do ônibus e a espera pelo caracol.
- A abertura da porta antes do embarque.
- A aproximação do caracol até a rampa.
- A subida pela rampa e a entrada na cabine.
- A chegada ao nível do piso antes de o caracol avançar para dentro da cabine.
- A marcação do passageiro como embarcado.
- O fechamento da porta depois da entrada.
- A partida somente depois do fechamento.
- A permanência do caracol dentro do ônibus.
- O reinício da sequência.
- O comportamento com delta time zero.
- A consistência com passos de tempo diferentes.
- A ordem das etapas mesmo quando um quadro demora mais.
- O giro das rodas somente quando o ônibus está andando.

Para executar pelo terminal do PyCharm:

```bash
python -m unittest discover -s tests -v
```

## Limite da validação

Os testes verificam a lógica da sequência. A seleção automática das dependências está configurada para Python 3.10 a 3.14. A cena gráfica foi executada visualmente em Python 3.14; isso não significa que tenha sido executada em todas as versões desse intervalo. Os testes automatizados verificam a lógica da animação, mas não substituem a conferência visual nos demais interpretadores.
