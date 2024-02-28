import pygame, sys, subprocess
pygame.init()
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
SCREEN_WIDTH, SCREEN_HEIGHT, y, pos1, pos2 = 800, 600, 10, 0, 0
prefix, current_player = "user@ubuntu:~$", 'X'
tictactoe, winner = False, False
class Terminal:
    def __init__(self):
        pygame.display.set_caption("RulsTerminal")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("lucidaconsole", 15)
        self.text, self.text_history_list, self.input_text = [], [[], []], ""
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    def commands(self):
        global tictactoe, WHITE, BLACK
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
                if text_color not in colors:
                    self.text.append("Color de texto incorrecto, 'help color' para más información.")
                else:
                    WHITE = colors[text_color]
                if bg_color not in colors:
                    self.text.append("Color de fondo incorrecto, 'help color' para más información.")
                else:
                    BLACK = colors[bg_color]
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
            self.text.append("El comando 'exit' sirve para cerrar el terminal.")
        elif not self.input_text.startswith(("help", "color", "clear", "exit", "tictactoe")):
            for i in (subprocess.getoutput(self.input_text)).split("\n"):
                self.text.append(i)
        self.input_text = ""
    def check_screen(self):
        global pos1, pos2, y
        if len(self.text) > 20 and self.text != self.text_history_list[pos2] and pos1 == pos2:
            self.text_history_list[pos2] = self.text[:20]
            del self.text[:20]
            pos2 += 1
            pos1 += 1
            self.text_history_list.append([])
            y = 10
    def render_text(self):
        global y, WHITE
        y = 10
        for i in self.text:
            self.screen.blit(self.font.render(i, True, WHITE), (10, y))
            y += 20
        self.screen.blit(self.font.render(prefix, True, WHITE), (10, SCREEN_HEIGHT - 30))
        self.screen.blit(self.font.render(self.input_text, True, WHITE), (10 + len(prefix)*10, SCREEN_HEIGHT - 30))
    def tictactoe(self):
        global WHITE
        for i in range(1, 3):
            pygame.draw.line(self.screen, WHITE, (625 + i*50, 25), (625 + i*50, 175), 3)
            pygame.draw.line(self.screen, WHITE, (625, 25 + i*50), (775, 25 + i*50), 3)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, WHITE, (col * 50 + 635, row * 50 + 35), ((col + 1) * 50 + 615, (row + 1) * 50 + 15), 3)
                    pygame.draw.line(self.screen, WHITE, (col * 50 + 635, (row + 1) * 50 + 15), ((col + 1) * 50 + 615, row * 50 + 35), 3)
                elif self.board[row][col] == 'O': pygame.draw.circle(self.screen, WHITE, (col * 50 + 650, row * 50 + 50), 16.667, 2)
    def run(self):
        global pos1, pos2, y, winner, tictactoe, current_player, BLACK
        while True:
            self.check_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        while pos1 != pos2 and event.key != pygame.K_UP and event.key != pygame.K_DOWN: pos1, self.text = pos1 + 1, []
                        self.commands()
                    elif event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_UP:
                        if len(self.text) > 0 and self.text != self.text_history_list[pos2] and pos1 == pos2:
                            self.text_history_list[pos2] = self.text[:22]
                            del self.text[:22]
                            pos2 += 1
                            pos1 += 1
                            self.text_history_list.append([])
                            y = 10
                        elif pos1 > 0:
                            pos1 -= 1
                            self.text = self.text_history_list[pos1]
                        elif pos1 == 0: pass
                    elif event.key == pygame.K_DOWN:
                        if pos1 == pos2:
                            pass
                        elif pos1 != pos2:
                            pos1 += 1
                            self.text = self.text_history_list[pos1]
                    else: self.input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and tictactoe:
                    mousex, mousey = pygame.mouse.get_pos()
                    clicked_row, clicked_col = (mousey - 25) // 50, (mousex - 625) // 50
                    try:
                        if self.board[clicked_row][clicked_col] == ' ':
                            self.board[clicked_row][clicked_col] = current_player
                            for i in range(3):
                                if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ': winner = True
                                if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ': winner = True
                            if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ': winner = True
                            if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ': winner = True
                            if winner:
                                self.text.append(f"Ha ganado el jugador {current_player}")
                                tictactoe = False
                                self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
                            elif all(' ' not in row for row in self.board):
                                self.text.append("¡Empate!")
                                tictactoe = False
                                self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
                            current_player = 'O' if current_player == 'X' else 'X'
                    except IndexError:
                        pass
            self.screen.fill(BLACK)
            self.render_text()
            if tictactoe: self.tictactoe()
            pygame.display.flip()
            pygame.time.Clock().tick(10)
Terminal().run()
