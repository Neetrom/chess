import pygame
from settings import ROOK_DIR, TILE_SIZE, QUEEN_DIR, NO_DIR, BISH_DIR, HORSE_DIR

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, pos):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{piece_type}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
        self.pos = pos

        self.type = piece_type
        self.points = 0

        self.directions = NO_DIR

        self.moved = False

    def update_pos(self,pos):
        self.pos = pos
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
    
    def all_available(self, board):
        for direction in self.directions:
            check = [self.pos[1], self.pos[0]]
            attack = False
            while True:
                check[0] += direction[0]
                check[1] += direction[1]
                if check[0] == 8 or check[0] == -1 or check[1] == 8 or check[1] == -1:
                    break
                attacking = board[check[0]][check[1]]
                if attacking != 0:
                    if attacking[0] == self.type[0]:
                        break
                    elif attack:
                        break
                    else:
                        attack = True
                board[check[0]][check[1]] = "X"
        return board

    def didnt_move(self):
        self.moved = False
    
    def did_move(self):
        self.moved = True

class Queen(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR

class Piece_Not_Sprite:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def move(self):
        pass

class Rook(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = ROOK_DIR
        self.moved = False

class KingAndHorse(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = NO_DIR
    
    def did_move(self):
        self.moved = True

    def didnt_move(self):
        self.moved = False

    def all_available(self, board):
        for direction in self.directions:
            check = [self.pos[1], self.pos[0]]
            check[0] += direction[0]
            check[1] += direction[1]
            if (check[0] > 7) or (check[0] < 0) or (check[1] > 7) or (check[1] < 0):
                continue
            attacking = board[check[0]][check[1]]
            if attacking != 0:
                if attacking[0] == self.type[0]:
                    continue
            board[check[0]][check[1]] = "X"
        return board

    def didnt_move(self):
        self.moved = False

class King(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
        self.moved = False
        


class Horse(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = HORSE_DIR


class Bishop(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = BISH_DIR

class Pawn(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.moved = False
    
    def all_available(self, board):
        if self.type[0] == "W":
            direction = -1
        else:
            direction = 1
        if board[self.pos[1]+direction][self.pos[0]] == 0:
            board[self.pos[1]+direction][self.pos[0]] = "X"
        if (not self.moved) and (board[self.pos[1]+direction*2][self.pos[0]] == 0) and board[self.pos[1]+direction][self.pos[0]] == "X":
            board[self.pos[1]+direction*2][self.pos[0]] = "X"
            self.moved = True
        if (self.pos[0] + 1) < 8:
            if board[self.pos[1]+direction][self.pos[0]+1] != 0 and board[self.pos[1]+direction][self.pos[0]+1][0] != self.type[0]:
                board[self.pos[1]+direction][self.pos[0]+1] = "X"
        if (self.pos[0] - 1) >= 0:
            if board[self.pos[1]+direction][self.pos[0]-1] != 0 and board[self.pos[1]+direction][self.pos[0]-1][0] != self.type[0]:
                board[self.pos[1]+direction][self.pos[0]-1] = "X"
        return board
    
    def didnt_move(self):
        self.moved = False