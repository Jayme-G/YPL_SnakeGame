# Yellow Python Little Snake Game | YPL Snake Game 🐍 - Jogo da Cobrinha Píton Amarela - Versão para Linux e Windows

## 1. Sobre o jogo

YPL Snake Game é uma releitura moderna, colorida e repleta de recursos do clássico jogo da cobrinha, feita em Python com Pygame.

### Principais características:
- **5 temas sazonais** (Primavera, Verão, Outono, Noite e Inverno), cada um com:
  - Cor de fundo diferente;
  - Música ambiente exclusiva; e
  - Arte ASCII temática no fundo.
- Ciclo de fases: a cada **10 comidas** coletadas, muda o tema. Ao completar o ciclo completo (50 comidas), você ganha **+1 vida** e o número de obstáculos aumenta;
- Sistema de **power-ups** com inventário (máximo 3);
- **3 vidas** iniciais + invencibilidade temporária após morte ou troca de fase;
- Salvamento automático do **High Score** em `high_score.txt`;
- Suporte a **tela cheia** (F11) e modo janela redimensionável;
- Barra superior com placar, vidas, fase atual, barra de progresso e inventário de power-ups; e
- Efeitos sonoros e visuais.

O jogo é 100% offline e roda com assets locais (imagens e músicas na pasta do executável).

## 2. Aviso Legal / Disclaimer

Este jogo é um projeto pessoal/hobby desenvolvido para diversão, ou seja: 
- Não há garantia de funcionamento em todas as máquinas ou configurações; 
- As imagens e músicas são de uso livre para este projeto;
- O autor não se responsabiliza por qualquer dano causado pelo uso do software; e
- Use por sua conta e risco e divirta-se com responsabilidade!

## 3. Baixar os binários conforme o seu sistema operacional (Linux ou Windows)

**Versões compiladas (recomendado):**

- **Windows**: `YPL_SnakeGame.zip`; ou
- **Linux**: `YPL_SnakeGame.tar.xz`

**Onde baixar:**
Disponível na página de Releases do repositório. Basta baixar o arquivo correspondente ao seu SO, descompactar e executar.

## 4. Se for executar a partir do Python, utilizar o Python 3.13 (não testei outras versões)

### Requisitos:
- Python 3.13 (recomendado); e
- Biblioteca `pygame` (instale com `pip install pygame`).
- Estrutura de pastas:
  ```
  .
  ├── Imagens/          (todas as .png)
  ├── Sons/             (todas as .mp3)
  ├── high_score.txt    (é criado automaticamente)
  └── YPL_SnakeGame.py
  ```

### Como rodar:
```bash
pip install pygame (ajustar o comando do pip conforme a sua necessidade, por exemplo: se usa venv, se não é o python global etc.)
python YPL_SnakeGame.py
```

## 5. Como jogar

### 5.1. Comandos do jogo

| Tecla          | Ação                              |
|----------------|-----------------------------------|
| **↑ ↓ ← →**    | Mover a cobra                     |
| **ESPAÇO**     | Pausar / Despausar                |
| **F11**        | Alternar entre tela cheia e janela|
| **1 / 2 / 3**  | Ativar power-up do slot 1/2/3 do inventário |
| **ENTER**      | Iniciar jogo / Reiniciar após Game Over |
| **Q**          | Sair do jogo                      |

### 5.2. Fases

O jogo possui **5 fases temáticas** que mudam automaticamente:

| Fase       | Nome       | FPS base | Estilo visual          |
|------------|------------|----------|------------------------|
| 1          | Primavera  | 5        | Verde suave            |
| 2          | Verão      | 8        | Verde amarelado        |
| 3          | Outono     | 5        | Bege / terra           |
| 4          | Noite      | 12       | Preto / escuro         |
| 5          | Inverno    | 3        | Branco / gelo          |

A cada **10 comidas** muda a fase. Ao terminar os 5 ciclos (50 comidas), você ganha **+1 vida** e o número de obstáculos aumenta permanentemente a cada novo ciclo.

### 5.3. Power-Ups

Aparecem aleatoriamente (10% de chance ao comer comida). Podem ser guardados no inventário (máximo 3).

| Power-Up            | Nome no jogo              | Efeito                                      | Duração    |
|---------------------|---------------------------|---------------------------------------------|------------|
| `speed`             | Super Rápido              | Cobra fica 50% mais rápida                  | 15 segundos |
| `invincibility`     | Invencibilidade           | Imune a colisões                            | 15 segundos |
| `double_score`      | Dupla Pontuação           | Pontuação x2                                | 15 segundos |
| `obstacle_eater`    | Obstáculos Comestíveis    | Pode comer obstáculos (ganha pontos)        | 15 segundos |

**Como usar:** pressione **1, 2 ou 3** para ativar o power-up do slot correspondente.

### 5.4. Vida

- Começa com **3 vidas**;
- Perde 1 vida ao colidir com parede, corpo ou obstáculo (exceto quando está invencível);
- Ganha **+1 vida** ao completar um ciclo completo de 5 fases;
- Após perder uma vida, a cobra ganha **3 segundos de invencibilidade temporária**; e
- Quando as vidas chegam a zero → **Game Over**.

### 5.5. High-Score

- Seu recorde é salvo automaticamente no arquivo `high_score.txt`;
- Aparece na barra superior e na tela de Game Over; e
- O recorde é mantido mesmo se você fechar o jogo.

---

Agradecimentos especiais à comunidade Pygame e a todos que ajudam a testar as builds!

Encontrou algum bug? Tem sugestão ou melhoria?  
→ Por favor abra uma issue ou mande sua ideia!

**Divirta-se com o YPL Snake Game 🐍 - Jogo da Cobrinha Píton Amarela!**  
Primavera 🌸 • Verão ☀️ • Outono 🍂 • Noite 🌙 • Inverno ❄️

Boa jogatina! 🚀
