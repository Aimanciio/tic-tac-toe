import pygame
from dataclasses import dataclass, field
import random
import time

# Configuración básica del juego
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 3, 3
SQUARE_SIZE = 200

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

@dataclass
class Board:
    squares: list = field(default_factory=lambda: [[None for _ in range(COLS)] for _ in range(ROWS)])

    def mark_square(self, row, col, player):
        if self.squares[row][col] is None:
            self.squares[row][col] = player
            return True
        return False

    def is_full(self):
        return all(all(cell is not None for cell in row) for row in self.squares)

    def check_winner(self, player):
        # Check rows, columns and diagonals
        for i in range(ROWS):
            if all(self.squares[i][j] == player for j in range(COLS)):
                return (True, i, 'row')
            if all(self.squares[j][i] == player for j in range(ROWS)):
                return (True, i, 'col')

        if all(self.squares[i][i] == player for i in range(ROWS)):
            return (True, 0, 'diag_desc')
        if all(self.squares[i][COLS - i - 1] == player for i in range(ROWS)):
            return (True, 0, 'diag_asc')

        return (False, None, None)

@dataclass
class Game:
    board: Board = field(default_factory=Board)
    current_player: str = 'X'
    game_over: bool = False
    en_menu: bool = True
    difficulty: str = 'Easy'
    two_player_mode: bool = False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def handle_click(self, row, col, win):
        if self.board.mark_square(row, col, self.current_player):
            win_status, line, direction = self.board.check_winner(self.current_player)
            if win_status:
                self.game_over = True
                draw_board(win, self.board)  # Dibujar el tablero antes de la línea de victoria
                pygame.display.update()
                time.sleep(1)  # Esperar 1 segundo antes de dibujar la línea de victoria
                self.draw_winning_line(line, direction, win)
                print(f"Player {self.current_player} wins!")
                pygame.time.wait(1000)  # Esperar 1 segundo antes de volver al menú
                self.return_to_menu()
            elif self.board.is_full():
                self.game_over = True
                print("It's a tie!")
                pygame.time.wait(1000)  # Esperar 1 segundo antes de volver al menú
                self.return_to_menu()
            else:
                self.switch_player()
                if self.current_player == 'O' and not self.two_player_mode:
                    self.ai_move(win)

    def ai_move(self, win):
        time.sleep(1)  # Retraso de 1 segundo para que el bot piense
        empty_squares = [(r, c) for r in range(ROWS) for c in range(COLS) if self.board.squares[r][c] is None]

        # Lógica para dificultad "Hard": intentar ganar o bloquear al jugador
        for r, c in empty_squares:
            self.board.squares[r][c] = 'O'
            if self.board.check_winner('O')[0]:
                self.board.squares[r][c] = None
                self.board.mark_square(r, c, 'O')
                return
            self.board.squares[r][c] = None

        for r, c in empty_squares:
            self.board.squares[r][c] = 'X'
            if self.board.check_winner('X')[0]:
                self.board.squares[r][c] = 'O'
                return
            self.board.squares[r][c] = None

        row, col = random.choice(empty_squares)
        self.board.mark_square(row, col, 'O')
        win_status, line, direction = self.board.check_winner('O')
        if win_status:
            self.game_over = True
            draw_board(win, self.board)  # Dibujar el tablero antes de la línea de victoria
            pygame.display.update()
            time.sleep(1)  # Esperar 1 segundo antes de dibujar la línea de victoria
            self.draw_winning_line(line, direction, win)
            print("AI wins!")
            pygame.time.wait(1000)  # Esperar 1 segundo antes de volver al menú
            self.return_to_menu()
        elif self.board.is_full():
            self.game_over = True
            print("It's a tie!")
            pygame.time.wait(1000)  # Esperar 1 segundo antes de volver al menú
            self.return_to_menu()
        else:
            self.switch_player()

    def draw_winning_line(self, line, direction, win):
        color = RED if self.current_player == 'X' else BLUE
        if direction == 'row':
            pygame.draw.line(win, color, (0, SQUARE_SIZE * line + 150 + SQUARE_SIZE // 2), (WIDTH, SQUARE_SIZE * line + 150 + SQUARE_SIZE // 2), 5)
        elif direction == 'col':
            pygame.draw.line(win, color, (SQUARE_SIZE * line + SQUARE_SIZE // 2, 150), (SQUARE_SIZE * line + SQUARE_SIZE // 2, HEIGHT - 50), 5)
        elif direction == 'diag_desc':
            pygame.draw.line(win, color, (0, 150), (WIDTH, HEIGHT - 50), 5)
        elif direction == 'diag_asc':
            pygame.draw.line(win, color, (0, HEIGHT - 50), (WIDTH, 150), 5)
        pygame.display.update()

    def reset_game(self):
        self.board = Board()
        self.current_player = 'X'
        self.game_over = False

    def return_to_menu(self):
        self.en_menu = True
        pygame.display.set_caption("Tic Tac Toe - Menú de Inicio")
        self.reset_game()

def draw_board(win, board):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, LINE_COLOR, rect, 1)
            if board.squares[row][col] == 'X':
                pygame.draw.line(win, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 120),
                                 (col * SQUARE_SIZE + 180, row * SQUARE_SIZE + 280), 5)
                pygame.draw.line(win, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 280),
                                 (col * SQUARE_SIZE + 180, row * SQUARE_SIZE + 120), 5)
            elif board.squares[row][col] == 'O':
                pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + 100, row * SQUARE_SIZE + 200), 80, 5)

def draw_menu(win, game):
    win.fill(BLACK)
    font = pygame.font.SysFont(None, 40)

    # Draw START button
    start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 80)
    pygame.draw.rect(win, GREEN, start_rect, border_radius=10)
    start_text = font.render('START', True, BLACK)
    win.blit(start_text, start_text.get_rect(center=start_rect.center))

    # Draw 2 PLAYERS button
    players_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 80)
    pygame.draw.rect(win, BLUE, players_rect, border_radius=10)
    players_text = font.render('2 PLAYERS', True, BLACK)
    win.blit(players_text, players_text.get_rect(center=players_rect.center))

    # Draw DIFFICULTY button
    difficulty_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 80)
    pygame.draw.rect(win, RED, difficulty_rect, border_radius=10)
    difficulty_text = font.render('DIFFICULTY', True, BLACK)
    win.blit(difficulty_text, difficulty_text.get_rect(center=difficulty_rect.center))

    pygame.display.flip()
    return start_rect, players_rect, difficulty_rect

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tic Tac Toe - Menú de Inicio')
    clock = pygame.time.Clock()

    game = Game()

    while True:
        if game.en_menu:
            start_rect, players_rect, difficulty_rect = draw_menu(win, game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        game.en_menu = False
                        game.two_player_mode = False
                        game.reset_game()
                        pygame.display.set_caption("Tic Tac Toe - Modo 1 Jugador")
                    elif players_rect.collidepoint(event.pos):
                        game.two_player_mode = True
                        game.en_menu = False
                        game.reset_game()
                        pygame.display.set_caption("Tic Tac Toe - Modo 2 Jugadores")
                    elif difficulty_rect.collidepoint(event.pos):
                        if game.difficulty == 'Easy':
                            game.difficulty = 'Medium'
                        elif game.difficulty == 'Medium':
                            game.difficulty = 'Hard'
                        else:
                            game.difficulty = 'Easy'
                        print(f"Difficulty set to {game.difficulty}")
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = (event.pos[1] - 100) // SQUARE_SIZE
                    game.handle_click(mouseY, mouseX, win)

            draw_board(win, game.board)
            pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()
