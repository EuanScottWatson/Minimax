import numpy as np
import pygame, os
from pygame.locals import *


# Minimising = AI
AI = -1
HUMAN = 1

# Message at end of game
END = {
    -1: "You Lose",
    0: "Draw",
    1: "You win"
}

# Pieces on board
VALUES = {
    -1: "O",
    0: " ",
    1: "X"
}


# Houses the board and the minimax logic
class Board:
    def __init__(self, start=None):
        self.board = np.zeros((3, 3)) if start is None else start

        self.memoisation = {}

    def place(self, x, y, value):
        if (self.board[x][y] != 0):
            return False
        
        self.board[x][y] = value
        return True

    def best_move(self):
        # AI plays best move based on minimax
        best = float('inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = AI

                    if (score := self.minimax(np.copy(self.board), False)) < best:
                        best = score
                        move = (i, j)

                    self.board[i][j] = 0
        
        self.board[move[0]][move[1]] = AI
    
    def minimax(self, b, minimising=True):
        # Check if game is finished
        if not ((s := self.win(b)) is None):
            return s

        # Otherwise perform minimax algorithm on all possible moves
        best = float('inf') if minimising else float('-inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == 0:
                    b[i][j] = AI if minimising else HUMAN

                    if np.array_str(b) in self.memoisation.keys():
                        score = self.memoisation[np.array_str(b)]
                    else:
                        score = self.minimax(np.copy(b), not minimising)
                    
                    b[i][j] = 0

                    if minimising:
                        best = min(score, best)
                    else:
                        best = max(score, best)
        
        self.memoisation[np.array_str(b)] = best

        return best 

    def win(self, board):
        for i in range(3):
            # Checks for straight line wins
            if (sum(board[i]) in [-3, 3]):
                return board[i][0] 
            if (sum(board.T[i]) in [-3, 3]):
                return board.T[i][0] 
        
        # Checks the diagonal
        if (((board[0][0] + board[1][1] + board[2][2]) in [-3, 3]) or 
                ((board[2][0] + board[1][1] + board[0][2]) in [-3, 3])):
                return board[1][1]
        
        # Checks for draw
        if 0 not in board:
            return 0
        
        return None

    def get_winner(self):
        return self.win(self.board)
    
    def copy(self):
        return Board(np.copy(self.board))

    def all_available_moves(self, player):
        available = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    next = self.copy()
                    next.place(i, j, player)
                    available.append(next)
        
        return available

    # toString
    def __repr__(self) -> str:
        return np.array_str(self.board)


class Minimax:
    def __init__(self):
        self.board = Board()
        self.turn = HUMAN
        self.done = False

        # Square chosen by user
        self.x, self.y = None, None

    def play(self):
        if self.done:
            return

        if self.turn == HUMAN:
            valid = False
            if not (self.x is None):
                while not valid:
                    valid = self.board.place(self.y, self.x, self.turn)

                    if not valid:
                        self.x, self.y = None, None
                        return
            else:
                return
        else:
            self.board.best_move()

        self.turn *= -1  
        
        if not (self.board.get_winner() is None):
            self.done = True

    '''
        PYGAME Section to display game
    '''

    def display(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 75)
        if self.done:
            message = END[self.board.get_winner()]
            score = font.render(message, True, (0, 0, 0))
            screen.blit(score, (50, 250))
        else:
            for j in range(3):
                for i in range(3):
                    value = VALUES[self.board.board[j][i]]
                    score = font.render(value, True, (0, 0, 0))
                    screen.blit(score, (200 * i + 75, 200 * j + 75))
                pygame.draw.line(screen, (0, 0, 0), (0, 200 * j), (600, 200 * j), 5)
                pygame.draw.line(screen, (0, 0, 0), (200 * j, 0), (200 * j, 600), 5)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.x = pos[0] // 200
                self.y = pos[1] // 200

    def display_screen(self, screen):
        screen.fill((255, 255, 255))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Tic Tac Toe")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 600, 600

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Minimax()

    while not done:
        done = game.events()
        game.play()
        game.display_screen(screen)

        clock.tick(60)


if __name__ == "__main__":
    main()