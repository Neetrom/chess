import pygame
from settings import DIRECTIONS

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, pos):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{piece_type}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.type = piece_type
        self.points = 0
    def update_pos(self,pos):
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)

class Piece_Not_Sprite:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def move(self):
        pass

class Rook(Piece_Not_Sprite):
    def all_available(self, b):
        board = b.copy()
        for direction in DIRECTIONS:
            check = [self.pos[0], self.pos[1]]
            attack = False
            while True:
                check[0] += direction[0]
                check[1] += direction[1]
                if check[0] == 8 or check[0] == -1 or check[1] == 8 or check[1] == -1:
                    break
                attacking = board[check[0]][check[1]]
                if attacking != 0 and attacking != "X":
                    if attacking.type[0] == self.color:
                        break
                    elif attack:
                        break
                    else:
                        attack = True
                board[check[0]][check[1]] = "X"
        return board
