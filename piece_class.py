import pygame
from settings import ROOK_DIR, TILE_SIZE, QUEEN_DIR, NO_DIR, BISH_DIR, HORSE_DIR
from copy import deepcopy, copy

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

    def did_it_move(self):
        return self.moved
    
    def all_available(self, board, enemy, piece_dict, rek):
        b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            while True:
                check[0] += direction[0]
                check[1] += direction[1]
                if check[0] == 8 or check[0] == -1 or check[1] == 8 or check[1] == -1:
                    break
                attacking = board[check[0]][check[1]]
                if attacking != 0:
                    if attacking[0] != self.type[0] and attacking[0] != "X":
                        if not rek:
                            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, check):
                                board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
                        else:
                            board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
                            if attacking[0] == "0":
                                continue
                    break
                if not rek:
                    if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, check):
                        board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
                else:
                    board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
        return board
    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = board[self.pos[1]][self.pos[0]]
        board[self.pos[1]][self.pos[0]] = 0
        king_pos = piece_dict[f"{self.type[0]}K"]
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if board[king_pos[1]][king_pos[0]] != f"{self.type[0]}K":
                return False
        return True
    
    def __str__(self):
        return f"{self.type}"

    def did_move(self):
        self.moved = True

class KingAndHorse(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = NO_DIR

    def all_available(self, board, enemy, piece_dict, rek):
        b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            check[0] += direction[0]
            check[1] += direction[1]
            if (check[0] > 7) or (check[0] < 0) or (check[1] > 7) or (check[1] < 0):
                continue
            attacking = board[check[0]][check[1]]
            if attacking != 0:
                if attacking[0] == self.type[0]:
                    continue
            if not rek:
                if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (check[0], check[1])):
                    board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
            else:
                board[check[0]][check[1]] = str(board[check[0]][check[1]]) + "X"
        return board

