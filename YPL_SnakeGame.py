# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ Yellow Python Little Snake Game | YPL Snake Game 🐍 - Jogo da Cobrinha Píton Amarela - Versão para Linux e Windows │
# ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

version = "1.0"

# The MIT License (MIT)
Author = "Copyright (C) 2026 Jayme Gonçalves"

import pygame
import random
import os
import sys
import webbrowser

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# Configurações do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GRID_SIZE = 40
SCREEN_WIDTH = (1280 // GRID_SIZE) * GRID_SIZE
SCREEN_HEIGHT = (720 // GRID_SIZE) * GRID_SIZE
SPRITE_SIZE = GRID_SIZE

INITIAL_SNAKE_X = 5  # Posição x inicial em unidades de GRID_SIZE
INITIAL_SNAKE_Y = 3  # Posição y inicial em unidades de GRID_SIZE

TOP_BAR_HEIGHT = 72
INITIAL_FPS = 10

COLORS = {
    'GRAY': (128, 128, 128),
    'GREEN': (0, 200, 0),
    'BLACK': (0, 50, 0),
    'WHITE': (255, 255, 255),
    'BCKGROUND_1': (118, 173, 139),  # Verde padrão (primavera)
    'BCKGROUND_2': (171, 208, 68),   # Verde amarelado (verão)
    'BCKGROUND_3': (169, 143, 113),  # Bege (outono)
    'BCKGROUND_4': (0, 0, 0),        # Preto (noite)
    'BCKGROUND_5': (255, 255, 255)   # Branco (inverno)
}

# Definição de temas e músicas associadas
THEMES = [
  {
      'color': COLORS['BCKGROUND_1'],
      'name': 'Primavera',
      'music': 'spring_music.mp3',
      'ascii_lines': [
          '   *   ',
          ' *   * ',
          '*     *',
          '**   **',
          '  |||  ',
          '  |||  ',
          '  |||  '
      ],
      'ascii_color': (148, 203, 169)    # Verde padrão mais claro
  },
  {
      'color': COLORS['BCKGROUND_2'],
      'name': 'Verão',
      'music': 'summer_music.mp3',
      'ascii_lines': [
          '   ^   ',
          ' ^^ ^^ ',
          '^     ^',
          '  |||  ',
          '  |||  ',
          '  |||  '
      ],
      'ascii_color': (201, 238, 98)    # Verde amarelado mais claro
  },
  {
      'color': COLORS['BCKGROUND_3'],
      'name': 'Outono',
      'music': 'autumn_music.mp3',
      'ascii_lines': [
          '  ~~~  ',
          '~~   ~~',
          '  ~~~  ',
          '  |||  ',
          '  |||  ',
          '  |||  '
      ],
      'ascii_color': (199, 173, 143)    # Bege mais claro
  },
  {
      'color': COLORS['BCKGROUND_4'],
      'name': 'Noite',
      'music': 'night_music.mp3',
      'ascii_lines': [
          '  | |  ',
          ' |   | ',
          '||   ||',
          '  |||  ',
          '  |||  ',
          '  |||  '
      ],
      'ascii_color': (30, 30, 30)   # Preto mais claro
  },
  {
      'color': COLORS['BCKGROUND_5'],
      'name': 'Inverno',
      'music': 'winter_music.mp3',
      'ascii_lines': [
          '   |   ',
          ' ==|== ',
          '   |   ',
          '   |   ',
          '  |||  ',
          '  |||  '
      ],
      'ascii_color': (225, 225, 225)   # Branco mais escuro
  }
]

FPS_LEVELS = [5, 8, 5, 12, 3]

# Dicionário de aliases para power-ups
POWER_UP_ALIASES = {
    'speed': 'Super Rápido',
    'invincibility': 'Invencibilidade',
    'double_score': 'Dupla Pontuação',
    'obstacle_eater': 'Obstáculos Comestíveis'
}

# Caminhos dos arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_COBRA = os.path.join(BASE_DIR, "Imagens", "img_cobra.png")
IMG_COMIDA = os.path.join(BASE_DIR, "Imagens", "img_comida.png")
IMG_OBSTACULO = os.path.join(BASE_DIR, "Imagens", "img_obstaculo.png")
IMG_SPEED = os.path.join(BASE_DIR, "Imagens", "img_speed.png")
IMG_INVINCIBILITY = os.path.join(BASE_DIR, "Imagens", "img_invincibility.png")
IMG_DOUBLE_SCORE = os.path.join(BASE_DIR, "Imagens", "img_double_score.png")
IMG_OBSTACLE_EATER = os.path.join(BASE_DIR, "Imagens", "img_obstacle_eater.png")
SND_EAT = os.path.join(BASE_DIR, "Sons", "eat.mp3")
SND_GAME_OVER = os.path.join(BASE_DIR, "Sons", "game_over.mp3")
SND_LIFE_UP = os.path.join(BASE_DIR, "Sons", "life_up.mp3")
SND_POWER_UP = os.path.join(BASE_DIR, "Sons", "power_up.mp3")
MUSIC_DIR = os.path.join(BASE_DIR, "Sons")

class Snake:
    # Classe que representa a cobra no jogo.
    def __init__(self, game):
        self.game = game  # Armazena referência ao objeto Game
        self.position = [GRID_SIZE * INITIAL_SNAKE_X, GRID_SIZE * INITIAL_SNAKE_Y]
        self.body = [
            [GRID_SIZE * 5, GRID_SIZE * 3],
            [GRID_SIZE * 4, GRID_SIZE * 3],
            [GRID_SIZE * 3, GRID_SIZE * 3]
        ]
        self.direction = 'RIGHT'

        try:
            self.head_images = {
                'UP': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "head_up.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE)),
                'DOWN': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "head_down.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE)),
                'LEFT': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "head_left.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE)),
                'RIGHT': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "head_right.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE))
            }
            self.body_image = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "body.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE))
            self.tail_image = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "tail.png")).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE))
        except FileNotFoundError:
            self.game.add_message("Erro: Imagens da cobra não encontradas. Usando recurso da interface.")
            self.head_images = {dir: pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)) for dir in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
            for img in self.head_images.values():
                img.fill(COLORS['GREEN'])
            self.body_image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            self.body_image.fill(COLORS['GREEN'])
            self.tail_image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            self.tail_image.fill(COLORS['GREEN'])

        self.invincible = False
        self.can_eat_obstacles = False

    def move(self):
        # Move a cobra na direção atual.
        if self.direction == 'UP':
            self.position[1] -= GRID_SIZE
        elif self.direction == 'DOWN':
            self.position[1] += GRID_SIZE
        elif self.direction == 'LEFT':
            self.position[0] -= GRID_SIZE
        elif self.direction == 'RIGHT':
            self.position[0] += GRID_SIZE
        self.body.insert(0, list(self.position))

    def reset(self):
        # Reinicia a cobra para a posição e direção iniciais, alinhada à grade.
        self.position = [GRID_SIZE * INITIAL_SNAKE_X, GRID_SIZE * INITIAL_SNAKE_Y]
        self.body = [
            [GRID_SIZE * 5, GRID_SIZE * 3],
            [GRID_SIZE * 4, GRID_SIZE * 3],
            [GRID_SIZE * 3, GRID_SIZE * 3]
        ]
        self.direction = 'RIGHT'

class Food:
    # Classe que representa a comida no jogo.
    def __init__(self, snake, obstacles=None, game=None):
        # Inicializa a comida com uma posição válida.
        self.snake = snake
        self.obstacles = obstacles or []
        self.game = game  # Armazena referência ao objeto Game
        try:
            self.image = pygame.transform.scale(pygame.image.load(IMG_COMIDA).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE))
        except FileNotFoundError:
            self.game.add_message(f"Erro: Imagem {IMG_COMIDA} não encontrada.")
            self.image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            self.image.fill(COLORS['WHITE'])
        self.position = self.generate_position()

    def generate_position(self):
        # Gera uma nova posição para a comida, evitando a cobra e obstáculos.
        while True:
            pos = [
                random.randrange(0, (SCREEN_WIDTH // GRID_SIZE)) * GRID_SIZE,
                random.randrange((TOP_BAR_HEIGHT + GRID_SIZE - 1) // GRID_SIZE, (SCREEN_HEIGHT // GRID_SIZE)) * GRID_SIZE
            ]
            if (pos[1] >= TOP_BAR_HEIGHT and pos not in self.snake.body and
                all(pos != obstacle.position for obstacle in self.obstacles)):
                return pos

class Obstacle:
    # Classe que representa os obstáculos no jogo.
    def __init__(self, snake, food, game):
        # Inicializa o obstáculo com uma posição válida.
        self.snake = snake
        self.food = food
        self.game = game  # Armazena referência ao objeto Game
        try:
            self.image = pygame.transform.scale(pygame.image.load(IMG_OBSTACULO).convert_alpha(), (SPRITE_SIZE, SPRITE_SIZE))
        except FileNotFoundError:
            self.game.add_message(f"Erro: Imagem {IMG_OBSTACULO} não encontrada.")
            self.image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            self.image.fill(COLORS['GRAY'])
        self.position = self.generate_position()

    def generate_position(self):
        # Gera uma nova posição para o obstáculo, evitando a cobra e a comida.
        while True:
            pos = [
                random.randrange(0, (SCREEN_WIDTH // GRID_SIZE)) * GRID_SIZE,  # Inicia de 0
                random.randrange((TOP_BAR_HEIGHT + GRID_SIZE - 1) // GRID_SIZE, (SCREEN_HEIGHT // GRID_SIZE)) * GRID_SIZE
            ]
            if (pos[1] >= TOP_BAR_HEIGHT and pos not in self.snake.body and pos != self.food.position):
                return pos

class PowerUp:
    # Classe que representa power-ups no jogo.
    def __init__(self, snake, food, obstacles):
        # Inicializa o power-up com uma posição válida.
        self.snake = snake
        self.food = food
        self.obstacles = obstacles
        self.type = random.choice(['speed', 'invincibility', 'double_score', 'obstacle_eater'])
        self.alias = POWER_UP_ALIASES.get(self.type, self.type)  # Obtém o alias ou usa o tipo como fallback
        try:
            self.image = pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "Imagens", f"img_{self.type}.png")).convert_alpha(),
                (SPRITE_SIZE, SPRITE_SIZE)
            )
        except FileNotFoundError:
            self.add_message(f"Erro: Imagem de Power-Up {self.alias} não encontrada.")
            self.image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            self.image.fill((255, 0, 255))  # Placeholder magenta
        self.position = self.generate_position()

    def generate_position(self):
        # Gera uma nova posição para o power-up, evitando a cobra, comida e obstáculos.
        while True:
            pos = [
                random.randrange(0, (SCREEN_WIDTH // GRID_SIZE)) * GRID_SIZE,
                random.randrange((TOP_BAR_HEIGHT + GRID_SIZE - 1) // GRID_SIZE, (SCREEN_HEIGHT // GRID_SIZE)) * GRID_SIZE
            ]
            if (pos[1] >= TOP_BAR_HEIGHT and pos not in self.snake.body and pos != self.food.position and
                all(pos != obs.position for obs in self.obstacles)):
                return pos

    def add_message(self, text):
        game = pygame.display.get_surface().game
        game.add_message(text)

class Game:
    def __init__(self):
        # Inicializa o jogo com configurações iniciais.
        self.is_fullscreen = True  # Rastreia o estado de tela cheia
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h

        # Configura a tela inicial (tela cheia ou janela)
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.virtual_width = SCREEN_WIDTH  # 1280 (ajustado para grade)
        self.virtual_height = SCREEN_HEIGHT  # 720 (ajustado para grade)
        self.virtual_screen = pygame.Surface((self.virtual_width, self.virtual_height))
        pygame.display.set_caption(f'Yellow Python Little Snake Game | YPL Snake Game 🐍 - Jogo da Cobrinha Píton Amarela - Versão {version}')
        self.clock = pygame.time.Clock()
        self.snake = Snake(self)  # Passa referência ao Game
        self.position = [GRID_SIZE * INITIAL_SNAKE_X, GRID_SIZE * INITIAL_SNAKE_Y]
        self.obstacles = []
        self.food = Food(self.snake, self.obstacles, self)  # Passa referência ao Game
        self.power_up = None
        self.power_up_inventory = []  # Lista para armazenar power-ups coletados
        self.max_inventory_size = 3  # Limite máximo de power-ups armazenados
        self.active_power_up_type = None
        self.power_up_timer = 0
        self.power_up_duration = 15000
        self.temp_inv_active = False
        self.temp_inv_timer = 0
        self.temp_inv_duration = 3000
        self.score = 0
        self.score_multiplier = 1
        self.high_score = self.load_high_score()
        self.lives = 3
        self.paused = False
        self.game_over = False
        self.theme_index = 0
        self.background = THEMES[self.theme_index]['color']
        self.fps = FPS_LEVELS[self.theme_index]
        self.food_count = 0
        self.obstacle_count = 3
        self.top_frame = pygame.Surface((self.virtual_width, TOP_BAR_HEIGHT))
        self.font = pygame.font.SysFont('Arial', 24)
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.text_paused = self.font.render("Jogo Pausado. Pressione 'Espaço' para continuar.", True, COLORS['WHITE'])
        self.transition = False
        self.transition_alpha = 0
        self.transition_duration = 2000
        self.transition_start_time = 0
        self.next_theme_index = 0
        self.messages = []  # Lista para armazenar mensagens temporárias
        self.message_duration = 5000  # Duração em ms para exibir cada mensagem
        self.message_font = pygame.font.SysFont('Arial', 20)  # Fonte para mensagens

        try:
            self.eat_sound = pygame.mixer.Sound(SND_EAT)
            self.game_over_sound = pygame.mixer.Sound(SND_GAME_OVER)
            self.life_up_sound = pygame.mixer.Sound(SND_LIFE_UP)
            self.power_up_sound = pygame.mixer.Sound(SND_POWER_UP)
        except FileNotFoundError:
            self.add_message("Aviso: Arquivo(s) de som não encontrado(s). O jogo continuará sem 1 ou mais arquivos de som.")
            self.eat_sound = None
            self.game_over_sound = None
            self.life_up_sound = None
            self.power_up_sound = None

        self.load_music()

        try:
            self.power_up_icons = {
                'speed': pygame.transform.scale(pygame.image.load(IMG_SPEED).convert_alpha(), (24, 24)),
                'invincibility': pygame.transform.scale(pygame.image.load(IMG_INVINCIBILITY).convert_alpha(), (24, 24)),
                'double_score': pygame.transform.scale(pygame.image.load(IMG_DOUBLE_SCORE).convert_alpha(), (24, 24)),
                'obstacle_eater': pygame.transform.scale(pygame.image.load(IMG_OBSTACLE_EATER).convert_alpha(), (24, 24))
            }
        except FileNotFoundError:
            self.add_message("Erro: Imagens de Power-Ups não encontradas. Usando recurso da interface.")
            self.power_up_icons = {
                typ: pygame.Surface((24, 24)).fill((255, 0, 255)) for typ in ['speed', 'invincibility', 'double_score', 'obstacle_eater']
            }

        try:
            self.score_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "img_score.png")).convert_alpha(), (24, 24))
        except FileNotFoundError:
            self.score_icon = pygame.Surface((24, 24))
            self.score_icon.fill((255, 215, 0))

        try:
            self.lives_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "img_lives.png")).convert_alpha(), (24, 24))
        except FileNotFoundError:
            self.lives_icon = pygame.Surface((24, 24))
            self.lives_icon.fill((255, 0, 0))

        try:
            self.theme_icon = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "Imagens", "img_theme.png")).convert_alpha(), (24, 24))
        except FileNotFoundError:
            self.theme_icon = pygame.Surface((24, 24))
            self.theme_icon.fill((0, 191, 255))

        self.generate_obstacles()
        self.ascii_font = pygame.font.SysFont('consolas', 74)  # Fonte monoespaçada para ASCII
        self.ascii_lines = THEMES[self.theme_index]['ascii_lines']
        self.ascii_color = THEMES[self.theme_index]['ascii_color']
        if self.ascii_lines:
            self.ascii_art_width = max(len(line.strip()) for line in self.ascii_lines) * 8
            self.ascii_art_height = len(self.ascii_lines) * 12
            x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - self.ascii_art_width - 50)
            y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - self.ascii_art_height - 50)
            self.ascii_pos = (x, y)

    def toggle_fullscreen(self):
        # Alterna entre os modos tela cheia e janela.
        self.is_fullscreen = not self.is_fullscreen
        display_info = pygame.display.Info()

        if self.is_fullscreen:
            # Modo tela cheia
            self.screen = pygame.display.set_mode(
                (display_info.current_w, display_info.current_h),
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        else:
            # Modo janela
            self.screen = pygame.display.set_mode(
                (self.virtual_width, self.virtual_height),
                pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
            )

    def render(self):
        # Escala a tela virtual para a tela real, preservando proporção.
        self.screen.fill((0, 0, 0))  # Preenche com preto para letterbox
        scale_factor = min(self.screen.get_width() / self.virtual_width, self.screen.get_height() / self.virtual_height)
        scaled_width = int(self.virtual_width * scale_factor)
        scaled_height = int(self.virtual_height * scale_factor)
        scaled_surface = pygame.transform.smoothscale(self.virtual_screen, (scaled_width, scaled_height))
        x = (self.screen.get_width() - scaled_width) // 2
        y = (self.screen.get_height() - scaled_height) // 2
        self.screen.blit(scaled_surface, (x, y))
        pygame.display.flip()  # Usa flip() para FULLSCREEN com DOUBLEBUF
        pygame.display.update()

    def update_power_flags(self):
        # Atualiza as flags de invencibilidade e comer obstáculos com base nos estados ativos.
        self.snake.invincible = (self.active_power_up_type == 'invincibility' or self.temp_inv_active)
        self.snake.can_eat_obstacles = (self.active_power_up_type == 'obstacle_eater')

    def handle_death(self):
        # Lida com a lógica de perda de vida e game over.
        if self.game_over_sound:
            self.game_over_sound.play()
        self.lives -= 1
        self.flash_screen()
        if self.active_power_up_type == 'speed':
            self.fps = FPS_LEVELS[self.theme_index]

        elif self.active_power_up_type == 'double_score':
            self.score_multiplier = 1

        self.active_power_up_type = None
        self.snake.reset()  # Reseta a cobra
        self.temp_inv_active = True
        self.temp_inv_timer = pygame.time.get_ticks()
        self.update_power_flags()  # Atualiza flags (invencível por 3s)
        self.food.position = self.food.generate_position()
        self.power_up = None  # Remove qualquer power-up ativo
        self.power_up_inventory = []  # Limpa inventário ao perder vida
        self.generate_obstacles()

        if self.lives < 0:
            self.save_high_score()
            pygame.mixer.music.stop()
            self.show_game_over()

    def load_high_score(self):
        # Carrega a pontuação máxima do arquivo.
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        # Salva a pontuação máxima se for maior que a atual.
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("high_score.txt", "w") as f:
                    f.write(str(self.high_score))
            except:
                self.add_message("Aviso: Não foi possível salvar o High Score. Verifique se a pasta do jogo está com permissão de escrita.")

    def load_music(self):
        # Carrega a música inicial ou ignora se o caminho estiver incorreto.
        music_path = os.path.join(MUSIC_DIR, THEMES[self.theme_index]['music'])
        # Verifica se o caminho do arquivo é válido e o arquivo existe
        if os.path.exists(music_path) and os.path.isfile(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                self.add_message(f"Aviso: Erro ao carregar a música {music_path}: {e}")
        else:
            self.add_message(f"Aviso: Caminho inválido ou música {music_path} não encontrada. Prosseguindo sem música.")

    def generate_obstacles(self):
        # Gera obstáculos em posições aleatórias com base em obstacle_count.
        self.obstacles = []
        for _ in range(self.obstacle_count):
            obstacle = Obstacle(self.snake, self.food, self)  # Passa referência ao Game
            self.obstacles.append(obstacle)
        self.food.obstacles = self.obstacles

    def update_background(self):
        # Inicia a transição para o próximo tema, regenera obstáculos e incrementa obstacle_count no fim do ciclo.
        self.next_theme_index = (self.theme_index + 1) % len(THEMES)

        # Configura ASCII art para a nova estação
        next_theme = THEMES[self.next_theme_index]
        self.ascii_lines = next_theme['ascii_lines']
        self.ascii_color = next_theme['ascii_color']

        # Calcula dimensões do ASCII
        if self.ascii_lines:
            self.ascii_art_width = max(len(line.strip()) for line in self.ascii_lines) * 8  # Aprox. 8px por char
            self.ascii_art_height = len(self.ascii_lines) * 12  # 12px por linha

            # Posição randômica dentro da área visível (abaixo da barra superior)
            x = random.randint(0, SCREEN_WIDTH - self.ascii_art_width)  # De 0 até o limite da largura
            y = random.randint(TOP_BAR_HEIGHT, SCREEN_HEIGHT - self.ascii_art_height)  # De TOP_BAR_HEIGHT até o limite da altura
            self.ascii_pos = (x, y)
        else:
            self.ascii_pos = (0, 0)  # Reseta posição se não houver arte ASCII

        if self.next_theme_index == 0:  # Fim do ciclo de temas
            self.lives += 1
            if self.life_up_sound:
                self.life_up_sound.play()
            self.obstacle_count += 1  # Incrementa apenas no fim do ciclo

        self.transition = True
        self.transition_start_time = pygame.time.get_ticks()
        pygame.mixer.music.fadeout(500)
        music_path = os.path.join(MUSIC_DIR, THEMES[self.next_theme_index]['music'])
        if os.path.exists(music_path) and os.path.isfile(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                self.add_message(f"Aviso: Erro ao carregar a música {music_path}: {e}")
        else:
            self.add_message(f"Aviso: Caminho inválido ou música {music_path} não encontrada. Prosseguindo sem música.")

        # Regenera obstáculos e reposiciona a comida
        self.generate_obstacles()
        self.food.position = self.food.generate_position()

    def flash_screen(self):
        for _ in range(3):
            self.virtual_screen.fill((255, 0, 0))
            self.render()
            pygame.time.wait(100)
            self.virtual_screen.fill(self.background)
            self.render()
            pygame.time.wait(100)

    def add_message(self, text):
            # Adiciona uma mensagem à lista com timestamp.
            self.messages.append({
                'text': text,
                'time': pygame.time.get_ticks()
            })

    def show_menu(self):
        # Exibe o menu inicial do jogo.
        while True:
            additional_texts = [
                ("Pressione 'ENTER' para jogar, 'R' para o repositório do jogo ou 'Q' para sair", 0),
                (f"Yellow Python Little Snake Game | YPL Snake Game | High Score: {self.high_score}", 0),
                ("https://github.com/Jayme-G/YPL_SnakeGame", 0),
                (f"{Author}", 0)
            ]
            self.show_overlay(f"Jogo da Cobrinha Píton Amarela - Versão {version}", alpha=255, additional_texts=additional_texts)
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:  # Permite redimensionamento apenas em modo janela
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        url = "https://github.com/Jayme-G/YPL_SnakeGame"
                        try:
                            webbrowser.open(url, new=2)
                            self.add_message("Abrindo o link no navegador…")
                        except Exception as e:
                            self.add_message(f"Erro ao abrir URL: {e}")
                        # Depois de abrir o link, continuamos na tela do menu
                        continue
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_RETURN:
                        self.load_music()
                        return True
                    elif event.key == pygame.K_q:
                        return False

    def activate_power_up_from_inventory(self, index):
        # Ativa um power-up do inventário pelo índice (0-based).
        if 0 <= index < len(self.power_up_inventory):
            power_up = self.power_up_inventory.pop(index)  # Remove do inventário

            # Toca o som de power-up
            if self.power_up_sound:
                self.power_up_sound.play()

            # Desativa o power-up atual, se houver
            if self.active_power_up_type:
                if self.active_power_up_type == 'speed':
                    self.fps = FPS_LEVELS[self.theme_index]
                elif self.active_power_up_type == 'double_score':
                    self.score_multiplier = 1
                self.active_power_up_type = None

            # Ativa o novo
            self.active_power_up_type = power_up.type
            self.power_up_timer = pygame.time.get_ticks()
            if self.active_power_up_type == 'speed':
                self.fps *= 1.5
            elif self.active_power_up_type == 'double_score':
                self.score_multiplier = 2

            self.update_power_flags()
            self.add_message(f"Power-Up {power_up.alias} ativado do inventário!")
        else:
            self.add_message("Índice inválido no inventário.")

    def update(self):
        # Verifica se o power-up ativo expirou
        if self.active_power_up_type and pygame.time.get_ticks() - self.power_up_timer > self.power_up_duration:
            if self.active_power_up_type == 'speed':
                self.fps = FPS_LEVELS[self.theme_index]
            elif self.active_power_up_type == 'double_score':
                self.score_multiplier = 1
            self.active_power_up_type = None  # Limpa o power-up ativo

        # Verifica se a invencibilidade temporária expirou
        if self.temp_inv_active and pygame.time.get_ticks() - self.temp_inv_timer > self.temp_inv_duration:
            self.temp_inv_active = False

        # Atualiza as flags de power-ups após checagens de expiração
        self.update_power_flags()

        self.snake.move()
        snake_rect = pygame.Rect(self.snake.position[0], self.snake.position[1], SPRITE_SIZE, SPRITE_SIZE)
        food_rect = pygame.Rect(self.food.position[0], self.food.position[1], SPRITE_SIZE, SPRITE_SIZE)

        grow = False  # Flag para controlar o crescimento (comida ou obstáculo comido)

        if snake_rect.colliderect(food_rect):
            if self.eat_sound:
                self.eat_sound.play()
            self.score += len(self.snake.body) * self.score_multiplier
            self.food_count += 1
            self.food.position = self.food.generate_position()
            grow = True  # Cresce ao comer comida
            if random.random() < 0.1:  # 10% de chance de gerar power-up
                self.power_up = PowerUp(self.snake, self.food, self.obstacles)
            if self.food_count % 10 == 0:
                self.update_background()

        # Verifica colisão com obstáculos
        obstacle_collision = False
        for i in range(len(self.obstacles) - 1, -1, -1):
            obs = self.obstacles[i]
            snake_rect = pygame.Rect(self.snake.position[0], self.snake.position[1], SPRITE_SIZE, SPRITE_SIZE)
            obstacle_rect = pygame.Rect(obs.position[0], obs.position[1], SPRITE_SIZE, SPRITE_SIZE)
            if snake_rect.colliderect(obstacle_rect):
                obstacle_collision = True
                if self.snake.can_eat_obstacles:
                    del self.obstacles[i]
                    if self.eat_sound:
                        self.eat_sound.play()
                    self.score += len(self.snake.body) * self.score_multiplier
                    grow = True
                    break
                elif self.snake.invincible:
                    break
                else:
                    self.handle_death()
                    return

        if not grow:
            self.snake.body.pop()

        if self.power_up:
            power_up_rect = pygame.Rect(self.power_up.position[0], self.power_up.position[1], SPRITE_SIZE, SPRITE_SIZE)
            if snake_rect.colliderect(power_up_rect):
                if self.eat_sound:
                    self.eat_sound.play()
                # Adiciona ao inventário
                if len(self.power_up_inventory) < self.max_inventory_size:
                    self.power_up_inventory.append(self.power_up)
                    self.add_message(f"Power-Up {self.power_up.alias} adicionado ao inventário!")
                else:
                    self.add_message("Inventário cheio! Power-Up descartado.")
                self.power_up = None
                self.update_power_flags()

        # Lida com colisões restantes
        wall_collision = (self.snake.position[0] < 0 or self.snake.position[0] > SCREEN_WIDTH - SPRITE_SIZE or
                          self.snake.position[1] < TOP_BAR_HEIGHT or self.snake.position[1] > SCREEN_HEIGHT - SPRITE_SIZE)
        body_collision = self.snake.position in self.snake.body[1:]

        if wall_collision:
            if self.snake.invincible:
                # Lógica quando invencível
                min_x = 0
                max_x = SCREEN_WIDTH - SPRITE_SIZE
                # min_y: próxima grade abaixo da barra (80)
                min_y = ((TOP_BAR_HEIGHT + GRID_SIZE - 1) // GRID_SIZE) * GRID_SIZE  # =80
                max_y = SCREEN_HEIGHT - SPRITE_SIZE  # Já alinhado (680)

                if self.snake.position[0] < min_x:
                    self.snake.position[0] = 2 * min_x - self.snake.position[0]
                    self.snake.direction = 'RIGHT'
                elif self.snake.position[0] > max_x:
                    self.snake.position[0] = 2 * max_x - self.snake.position[0]
                    self.snake.direction = 'LEFT'

                if self.snake.position[1] < min_y:  # Agora usa min_y=80, mas detecção já foi <72
                    self.snake.position[1] = 2 * min_y - self.snake.position[1]
                    self.snake.direction = 'DOWN'
                elif self.snake.position[1] > max_y:
                    self.snake.position[1] = 2 * max_y - self.snake.position[1]
                    self.snake.direction = 'UP'

                # Atualiza corpo com posição
                self.snake.body[0] = list(self.snake.position)
            else:
                self.handle_death()
                return

        # Checa colisão com o corpo (separado de obstáculos)
        if body_collision and not self.snake.invincible:
            self.handle_death()
            return

    def draw_gradient(self, surface, color1, color2, rect):
        # Desenha um gradiente vertical em uma superfície.
        h = rect[3]
        for y in range(h):
            r = color1[0] + (color2[0] - color1[0]) * y / h
            g = color1[1] + (color2[1] - color1[1]) * y / h
            b = color1[2] + (color2[2] - color1[2]) * y / h
            pygame.draw.line(surface, (int(r), int(g), int(b)), (rect[0], rect[1] + y), (rect[0] + rect[2], rect[1] + y))

    def draw_rounded_rect(self, surface, rect, color, radius=10):
        # Desenha um retângulo arredondado.
        if rect[2] <= 0 or rect[3] <= 0:
            return  # Não desenha nada se largura ou altura for <= 0

        # Ajusta o raio para não exceder metade da largura ou altura (evita transbordamento)
        radius = min(radius, rect[2] / 2, rect[3] / 2)

        # Parte horizontal do meio (com largura segura)
        h_width = max(0, rect[2] - 2 * radius)
        pygame.draw.rect(surface, color, (rect[0] + radius, rect[1], h_width, rect[3]))

        # Parte vertical do meio (com altura segura, embora geralmente não precise)
        v_height = max(0, rect[3] - 2 * radius)
        pygame.draw.rect(surface, color, (rect[0], rect[1] + radius, rect[2], v_height))

        # Círculos nos cantos
        pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + radius), radius)
        pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + radius), radius)
        pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + rect[3] - radius), radius)
        pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + rect[3] - radius), radius)

    def draw_text_with_shadow(self, surface, text, font, color, pos, shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
        # Desenha texto com sombra para melhor visibilidade.
        shadow_text = font.render(text, True, shadow_color)
        surface.blit(shadow_text, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
        main_text = font.render(text, True, color)
        surface.blit(main_text, pos)

    def draw(self):
        # Desenha todos os elementos na tela virtual.
        self.virtual_screen.fill(self.background)

        # Renderiza ASCII art apenas se não estiver em transição
        if self.ascii_lines and not self.transition:
            for i, line in enumerate(self.ascii_lines):
                padded_line = line.center(self.ascii_art_width // 8)  # Centraliza chars
                text_surf = self.ascii_font.render(padded_line, True, self.ascii_color)
                y_pos = self.ascii_pos[1] + (i * 12)
                self.virtual_screen.blit(text_surf, (self.ascii_pos[0], y_pos))

        if self.paused:
            self.show_overlay("Jogo Pausado. Pressione 'Espaço' para continuar.", blink=True)
        elif self.transition:
            self.show_transition()
        else:
            if self.snake.invincible:
                blink = (pygame.time.get_ticks() % 400) < 200
                if blink:
                    for i, pos in enumerate(self.snake.body):
                        if i == 0:  # Cabeça
                            self.virtual_screen.blit(self.snake.head_images[self.snake.direction], (pos[0], pos[1]))
                        elif i == len(self.snake.body) - 1:  # Cauda
                            self.virtual_screen.blit(self.snake.tail_image, (pos[0], pos[1]))
                        else:  # Corpo
                            self.virtual_screen.blit(self.snake.body_image, (pos[0], pos[1]))
            else:
                for i, pos in enumerate(self.snake.body):
                    if i == 0:  # Cabeça
                        self.virtual_screen.blit(self.snake.head_images[self.snake.direction], (pos[0], pos[1]))
                    elif i == len(self.snake.body) - 1:  # Cauda
                        self.virtual_screen.blit(self.snake.tail_image, (pos[0], pos[1]))
                    else:  # Corpo
                        self.virtual_screen.blit(self.snake.body_image, (pos[0], pos[1]))
            self.virtual_screen.blit(self.food.image, (self.food.position[0], self.food.position[1]))
            for obstacle in self.obstacles:
                self.virtual_screen.blit(obstacle.image, (obstacle.position[0], obstacle.position[1]))
            if self.power_up:
                self.virtual_screen.blit(self.power_up.image, (self.power_up.position[0], self.power_up.position[1]))

            # Desenha o top frame
            theme_color = THEMES[self.theme_index]['color']
            dark_theme_color = (max(0, theme_color[0] - 50), max(0, theme_color[1] - 50), max(0, theme_color[2] - 50))
            self.draw_gradient(self.top_frame, dark_theme_color, theme_color, (0, 0, self.virtual_width, TOP_BAR_HEIGHT))

            # Renderiza textos com sombra
            text_score = f'Placar: {self.score}'
            text_lives = f'Vidas: {self.lives}'
            text_high_score = f'High Score: {self.high_score}'
            text_theme = f'Fase: {THEMES[self.theme_index]["name"]}'

            # Desenha o placar
            self.top_frame.blit(self.score_icon, (20, 10))
            self.draw_text_with_shadow(self.top_frame, text_score, self.font, COLORS['WHITE'], (50, 10))

            # Desenha a barra de progresso
            progress = (self.food_count % 10) / 10
            progress_bar_rect = (20, 50, 200, 20)
            self.draw_rounded_rect(self.top_frame, progress_bar_rect, COLORS['GRAY'])
            fill_rect = (20, 50, 200 * progress, 20)
            self.draw_rounded_rect(self.top_frame, fill_rect, COLORS['GREEN'])

            # Desenha o texto da fase
            self.top_frame.blit(self.theme_icon, (self.virtual_width - 1010, 45))  # Ícone da fase
            self.draw_text_with_shadow(self.top_frame, text_theme, self.font, COLORS['WHITE'], (self.virtual_width - 1010 + 30, 45))

            # Desenha o high score
            self.draw_text_with_shadow(self.top_frame, text_high_score, self.font, COLORS['WHITE'], (self.virtual_width // 2 - self.font.size(text_high_score)[0] // 2, 24))

            # Desenha as vidas
            lives_icon_pos = (self.virtual_width - 980 - 30, 10)
            self.top_frame.blit(self.lives_icon, lives_icon_pos)
            self.draw_text_with_shadow(self.top_frame, text_lives, self.font, COLORS['WHITE'], (lives_icon_pos[0] + 30, 10))

            # Indicador de power-up ativo
            if self.active_power_up_type:
                icon = self.power_up_icons[self.active_power_up_type]
                icon_pos = (self.virtual_width - 450, 30)
                self.top_frame.blit(icon, icon_pos)
                elapsed = pygame.time.get_ticks() - self.power_up_timer
                remaining_progress = max(0, (self.power_up_duration - elapsed) / self.power_up_duration)
                bar_width = 200
                bar_height = 20
                bar_x = icon_pos[0] + 30
                bar_y = icon_pos[1]
                bar_rect = (bar_x, bar_y, bar_width, bar_height)
                self.draw_rounded_rect(self.top_frame, bar_rect, COLORS['GRAY'])
                fill_rect = (bar_x, bar_y, bar_width * remaining_progress, bar_height)
                self.draw_rounded_rect(self.top_frame, fill_rect, COLORS['GREEN'])

            # Tabela de Power-Ups
            cell_width = 40  # Largura de cada célula
            cell_height = 30 # Altura de cada célula
            cell_margin = 5  # Margem entre células
            table_x = self.virtual_width - 150  # Inicia à esquerda do texto de vidas
            table_y = 5      # Alinha com o topo do top_frame
            for i in range(3):
                # Posição da célula
                cell_x = table_x + i * (cell_width + cell_margin)
                cell_y_top = table_y
                cell_y_bottom = table_y + cell_height + cell_margin
                # Desenha células da primeira linha (números 1, 2, 3)
                cell_rect_top = (cell_x, cell_y_top, cell_width, cell_height)
                self.draw_rounded_rect(self.top_frame, cell_rect_top, COLORS['GRAY'], radius=5)
                number_text = str(i + 1)
                text_surface = self.font.render(number_text, True, COLORS['WHITE'])
                text_rect = text_surface.get_rect(center=(cell_x + cell_width / 2, cell_y_top + cell_height / 2))
                self.draw_text_with_shadow(self.top_frame, number_text, self.font, COLORS['WHITE'], (text_rect.x, text_rect.y))
                # Desenha células da segunda linha (ícones de power-ups)
                cell_rect_bottom = (cell_x, cell_y_bottom, cell_width, cell_height)
                self.draw_rounded_rect(self.top_frame, cell_rect_bottom, COLORS['GRAY'], radius=5)
                if i < len(self.power_up_inventory):
                    icon = self.power_up_icons[self.power_up_inventory[i].type]
                    icon_rect = icon.get_rect(center=(cell_x + cell_width / 2, cell_y_bottom + cell_height / 2))
                    self.top_frame.blit(icon, icon_rect)

            # Linha de separação
            pygame.draw.line(self.virtual_screen, theme_color, (0, TOP_BAR_HEIGHT), (self.virtual_width, TOP_BAR_HEIGHT), 4)
            self.virtual_screen.blit(self.top_frame, (0, 0))

            # Desenha mensagens no canto inferior esquerdo
            current_time = pygame.time.get_ticks()
            y_offset = self.virtual_height - 30  # Começa a 30px da borda inferior
            # Filtra mensagens expiradas e desenha as válidas
            self.messages = [msg for msg in self.messages if current_time - msg['time'] < self.message_duration]
            for msg in reversed(self.messages):  # Reversed para exibir mais recente no topo
                self.draw_text_with_shadow(
                    self.virtual_screen,
                    msg['text'],
                    self.message_font,
                    (255, 255, 0),  # Amarelo
                    (10, y_offset),  # Canto inferior esquerdo (10px da borda esquerda)
                    shadow_color=(0, 0, 0),  # Sombra preta
                    shadow_offset=(2, 2)
                )
                y_offset -= 25  # Espaço entre mensagens

    def show_transition(self):
        # Exibe uma tela de transição com o nome da nova estação.
        elapsed_time = pygame.time.get_ticks() - self.transition_start_time
        progress = min(elapsed_time / (self.transition_duration / 2), 1)
        if elapsed_time > self.transition_duration / 2:
            progress = max(1 - (elapsed_time - self.transition_duration / 2) / (self.transition_duration / 2), 0)
        alpha = 255 * progress
        theme_name = THEMES[self.next_theme_index]['name']
        self.show_overlay(f"{theme_name}", alpha=alpha)
        if elapsed_time >= self.transition_duration:
            self.transition = False
            self.theme_index = self.next_theme_index
            self.background = THEMES[self.theme_index]['color']

            # Desativa qualquer power-up ativo da fase anterior
            if self.active_power_up_type:
                if self.active_power_up_type == 'speed':
                    self.fps = FPS_LEVELS[self.theme_index]  # Restaura FPS base (sem multiplicador)
                elif self.active_power_up_type == 'double_score':
                    self.score_multiplier = 1
                self.active_power_up_type = None
                self.power_up_timer = 0  # Reseta o timer para evitar persistência

            # Atualiza o FPS base da nova fase (sem carregar efeitos anteriores)
            self.fps = FPS_LEVELS[self.theme_index]

            # Ativa invencibilidade temporária após transição de fase
            self.temp_inv_active = True
            self.temp_inv_timer = pygame.time.get_ticks()
            self.update_power_flags()  # Atualiza flags (invencível por 3s)
            pygame.mixer.music.fadeout(500)
            # Carrega a música inicial ou ignora se o caminho estiver incorreto.
            music_path = os.path.join(MUSIC_DIR, THEMES[self.theme_index]['music'])
            # Verifica se o caminho do arquivo é válido e o arquivo existe
            if os.path.exists(music_path) and os.path.isfile(music_path):
                try:
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play(-1)
                except pygame.error as e:
                    self.add_message(f"Aviso: Erro ao carregar a música {music_path}: {e}")
            else:
                self.add_message(f"Aviso: Caminho inválido ou música {music_path} não encontrada. Prosseguindo sem música.")

    def show_overlay(self, text, alpha=255, blink=False, additional_texts=None):
        # Exibe uma tela de sobreposição com texto centralizado.
        overlay = pygame.Surface((self.virtual_width, self.virtual_height))  # Modificado: Use tamanhos virtuais
        overlay.fill(COLORS['BLACK'])
        if blink:
            # Efeito piscante para a pausa (varia alpha entre 128 e 255 a cada 1s)
            alpha = 128 + 127 * (pygame.time.get_ticks() % 1000) / 1000
        overlay.set_alpha(int(alpha))
        self.virtual_screen.blit(overlay, (0, 0))

        # Renderiza o texto principal
        text_surface = self.font_large.render(text, True, COLORS['GREEN'])
        # Centraliza o texto principal verticalmente, com leve deslocamento para cima
        text_rect = text_surface.get_rect(center=(self.virtual_width / 2, self.virtual_height / 2 - 50 if additional_texts else self.virtual_height / 2))
        self.virtual_screen.blit(text_surface, text_rect)

        # Renderiza os textos adicionais, se existirem
        if additional_texts:
            # Calcula o espaçamento vertical proporcional
            spacing = 50  # Espaçamento entre linhas
            total_height = len(additional_texts) * spacing
            # Inicia os textos adicionais abaixo do texto principal
            start_y = SCREEN_HEIGHT / 2 + 20  # Pequeno deslocamento após o texto principal

            for i, (add_text, offset_y_relativo) in enumerate(additional_texts):
                add_text_surface = self.font.render(add_text, True, COLORS['GREEN'])
                add_text_rect = add_text_surface.get_rect(center=(self.virtual_width / 2, start_y + i * spacing + offset_y_relativo))
                self.virtual_screen.blit(add_text_surface, add_text_rect)

    def show_game_over(self):
        # Exibe a tela de game over.
        while True:
            # Desenha o fundo do jogo (incluindo arte ASCII) antes do overlay
            self.draw()
            additional_texts = [
                (f"Placar: {self.score}", 0),
                (f"High Score: {self.high_score}", 0),
                ("Pressione ENTER para jogar novamente", 0),
                ("Pressione Q para sair", 0)
            ]
            self.show_overlay("Game Over!", alpha=255, additional_texts=additional_texts)
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.snake.reset()
                        self.food.position = self.food.generate_position()
                        self.power_up = None
                        self.power_up_inventory = []
                        self.score = 0
                        self.score_multiplier = 1
                        self.lives = 3
                        self.theme_index = 0
                        self.food_count = 0
                        self.obstacle_count = 3
                        self.generate_obstacles()
                        self.background = THEMES[self.theme_index]['color']
                        self.fps = FPS_LEVELS[self.theme_index]

                        # Reinicie a arte ASCII
                        self.ascii_lines = THEMES[self.theme_index]['ascii_lines']
                        self.ascii_color = THEMES[self.theme_index]['ascii_color']
                        if self.ascii_lines:
                            self.ascii_art_width = max(len(line.strip()) for line in self.ascii_lines) * 8
                            self.ascii_art_height = len(self.ascii_lines) * 12
                            x = random.randint(0, SCREEN_WIDTH - self.ascii_art_width)
                            y = random.randint(TOP_BAR_HEIGHT, SCREEN_HEIGHT - self.ascii_art_height)
                            self.ascii_pos = (x, y)
                        else:
                            self.ascii_pos = (0, 0)

                        self.load_music()
                        self.game_over = False
                        # Ativa invencibilidade temporária ao reiniciar
                        self.temp_inv_active = True
                        self.temp_inv_timer = pygame.time.get_ticks()
                        self.update_power_flags()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def run(self):
        # Executa o loop principal do jogo.
        if not self.show_menu():
            pygame.quit()
            sys.exit()

        # Ativa invencibilidade temporária ao iniciar o jogo (3 segundos)
        self.temp_inv_active = True
        self.temp_inv_timer = pygame.time.get_ticks()
        self.update_power_flags()  # Atualiza as flags para ativar a invencibilidade na cobra

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:  # Permite redimensionamento apenas em modo janela
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                        self.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                        self.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                        self.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                        self.snake.direction = 'RIGHT'
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_1 and len(self.power_up_inventory) >= 1:
                        self.activate_power_up_from_inventory(0)
                    elif event.key == pygame.K_2 and len(self.power_up_inventory) >= 2:
                        self.activate_power_up_from_inventory(1)
                    elif event.key == pygame.K_3 and len(self.power_up_inventory) >= 3:
                        self.activate_power_up_from_inventory(2)
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            if self.transition:
                self.show_transition()
                self.render()
            elif not self.paused and not self.game_over:
                self.update()
                self.draw()
                self.render()
            else:
                self.draw()
                self.render()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run()
