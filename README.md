# Simulador de Gravidade - Algoritmo de Barnes-Hut

Este projeto é um simulador de gravidade que utiliza o algoritmo de Barnes-Hut para calcular as forças gravitacionais entre corpos. O simulador é implementado em Python usando a biblioteca Pygame para renderização gráfica.

## Funcionalidades

- Simulação de corpos celestes com gravidade.
- Utilização do algoritmo de Barnes-Hut para otimizar os cálculos gravitacionais.
- Adição de novos corpos com clique do mouse.
- Visualização das forças atuando em cada corpo.

## Estrutura do Código

### Classes Principais

- **Body**: Representa cada objeto na simulação. Contém métodos para atualizar a posição, aplicar gravidade, verificar colisões e desenhar o corpo na tela.
- **QuadTree**: Utilizada para dividir o espaço e aplicar o algoritmo de Barnes-Hut. Contém métodos para inserir corpos, subdividir o espaço e calcular a gravidade.

### Função Principal

A função `main()` inicializa a simulação, cria corpos aleatórios e gerencia o loop principal do Pygame. Dentro do loop, a função:

1. Processa eventos do Pygame (como cliques do mouse).
2. Calcula as forças gravitacionais usando a QuadTree.
3. Verifica colisões e mescla corpos se necessário.
4. Atualiza as posições dos corpos e redesenha a tela.

## Como Executar

1. Certifique-se de ter o Python e a biblioteca Pygame instalados.
2. Execute o script `app.py`:

```bash
python app.py
```

3. A simulação será iniciada e você poderá adicionar novos corpos clicando e arrastando o mouse.

## Requisitos

- Python 3.x
- Pygame

## Instalação do Pygame

Você pode instalar o Pygame usando pip:

```bash
pip install pygame
```

## Controles

- **Clique e arraste**: Adiciona um novo corpo com velocidade inicial baseada no movimento do mouse.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou novas funcionalidades. Para isso, faça um fork deste repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE.txt).
