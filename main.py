import pygame
import sys
import subprocess
pygame.init()
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
y, prefix, current_player = 10, "user@ubuntu:~$", 'X'
tictactoe, pos, pos2 = False, 0, 0

class Terminal:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Terminal")
        self.font, self.text_history_list = pygame.font.SysFont("lucidaconsole", 15), [[], []]
        self.text, self.input_text, self.board = [], "", [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def render_text(self):
        self.screen.fill(BLACK)
        global y
        y = 10
        for i in self.text:
            text_surface = self.font.render(i, True, WHITE)
            self.screen.blit(text_surface, (10, y))
            y += 20
        input_prompt = self.font.render(prefix, True, WHITE)
        self.screen.blit(input_prompt, (10, SCREEN_HEIGHT - 30))
        input_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(input_surface, (10 + len(prefix)*10, SCREEN_HEIGHT - 30))

    def draw_grid(self):
        for i in range(1, 3):
            pygame.draw.line(self.screen, WHITE, (625 + i*50, 25), (625 + i*50, 175), 3)
            pygame.draw.line(self.screen, WHITE, (625, 25 + i*50), (775, 25 + i*50), 3)

    def draw_xo(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, WHITE, (col * 50 + 635, row * 50 + 35),
                                     ((col + 1) * 50 + 615, (row + 1) * 50 + 15), 3)
                    pygame.draw.line(self.screen, WHITE, (col * 50 + 635, (row + 1) * 50 + 15),
                                     ((col + 1) * 50 + 615, row * 50 + 35), 3)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, WHITE, (col * 50 + 650, row * 50 + 50), 16.667, 2)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def run(self):
        global y, current_player, tictactoe, WHITE, BLACK, pos, pos2
        clock = pygame.time.Clock()
        running = True
        while running:
            if len(self.text) > 20 and self.text != self.text_history_list[pos2] and pos == pos2:
                self.text_history_list[pos2] = self.text[:20]
                del self.text[:20]
                pos2 += 1
                pos += 1
                self.text_history_list.append([])
                y = 10
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        while pos != pos2 and event.key != pygame.K_UP and event.key != pygame.K_DOWN: pos, self.text = pos+1, []
                        self.text.append(f"{prefix} {self.input_text}")
                        if self.input_text == "help":
                            self.text.append("Comandos disponibles:")
                            self.text.append("help")
                            self.text.append("clear")
                            self.text.append("color")
                            self.text.append("exit")
                            self.text.append("tictactoe")
                        if self.input_text == "tictactoe":
                            tictactoe = 1
                            self.text.append("Tres en Raya Spawneado")
                        if self.input_text == "help tictactoe":
                            self.text.append("El comando 'tictactoe' inicia un juego de tres en raya para dos jugadores.")
                        if self.input_text == "help help":
                            self.text.append("El comando 'help' sirve para dar información sobre los otros comandos.")
                            self.text.append("Sintaxis: help nombredelcomando")
                            self.text.append("Ejemplo: help color")
                        if self.input_text == "clear":
                            self.text = []
                        if self.input_text == "help clear":
                            self.text.append("El comando 'clear' se encarga de limpiar el historial de comandos.")
                        if self.input_text.startswith("color "):
                            try:
                                text_color, bg_color = self.input_text[6:].split()
                                colors = {'white': (255, 255, 255), 'black': (0, 0, 0),
                                          'green': (0, 255, 0), 'red': (255, 0, 0),
                                          'blue': (0, 0, 255), 'pink': (255, 0, 255),
                                          'cyan': (0, 255, 255), 'yellow': (255, 255, 0)}
                                if text_color not in colors: self.text.append("Color de texto incorrecto, 'help color' para más información.")
                                else: WHITE = colors[text_color]
                                if bg_color not in colors: self.text.append("Color de fondo incorrecto, 'help color' para más información.")
                                else: BLACK = colors[bg_color]
                            except ValueError:
                                self.text.append("Formato incorrecto, 'help color' para más información.")
                        if self.input_text == "help color":
                            self.text.append("El comando 'color' sirve para cambiar el color del texto y del fondo del terminal.")
                            self.text.append("Sintaxis: color colortexto colorfondo")
                            self.text.append("Ejemplo: color red white")
                            self.text.append("Colores disponibles:")
                            self.text.append("white black")
                            self.text.append("blue yellow red")
                            self.text.append("cyan green pink")
                        if self.input_text == "exit":
                            pygame.quit()
                            sys.exit()
                        if self.input_text == "help exit":
                            self.text.append("El comando 'exit' sirve para \n cerrar el terminal.")
                        elif not self.input_text.startswith(("help", "color", "clear", "exit", "tictactoe")):
                            for i in (subprocess.getoutput(self.input_text)).split("\n"):
                                self.text.append(i)
                        self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_UP:
                        if len(self.text) > 0 and self.text != self.text_history_list[pos2] and pos == pos2:
                            self.text_history_list[pos2] = self.text[:22]
                            del self.text[:22]
                            pos2 += 1
                            pos += 1
                            self.text_history_list.append([])
                            y = 10
                        elif pos > 0:
                            pos -= 1
                            self.text = self.text_history_list[pos]
                        elif pos == 0: pass
                    elif event.key == pygame.K_DOWN:
                        if pos == pos2: pass
                        elif pos != pos2:
                            pos += 1
                            self.text = self.text_history_list[pos]
                    else:
                        self.input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and tictactoe:
                    mouseX, mouseY = event.pos
                    clicked_row, clicked_col = (mouseY - 25) // 50, (mouseX - 625) // 50
                    try:
                        if self.board[clicked_row][clicked_col] == ' ':
                            self.board[clicked_row][clicked_col] = current_player
                            winner = self.check_winner()
                            if winner:
                                self.text.append(f"Ha ganado el jugador {winner}")
                                tictactoe = False
                                self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
                            elif all(' ' not in row for row in self.board):
                                self.text.append("¡Empate!")
                                tictactoe = False
                                self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
                            current_player = 'O' if current_player == 'X' else 'X'
                    except IndexError:
                        pass

            self.render_text()
            if tictactoe:
                self.draw_grid()
                self.draw_xo()
            pygame.display.flip()
            clock.tick(10)
        pygame.quit()
        sys.exit()

Terminal().run()
