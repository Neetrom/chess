import pygame
from settings import TILE_SIZE, NO_DIR
from copy import deepcopy, copy

class Graphic_piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, pos):
        super().__init__()
        if piece_type != "00":
            self.image = pygame.image.load(f"graphics/{piece_type}.png").convert_alpha()
        else:
            self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
    
    def update_pos(self,pos):
        self.pos = pos
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))

class Piece:
    def __init__(self, piece_type, pos):
        self.pos = pos

        self.type = piece_type
        self.points = 0
        self.valid_attack = False

        self.directions = NO_DIR

        self.moved = False

    def update_pos(self,pos):
        self.pos = pos

    def did_it_move(self):
        return self.moved

    def can_be_attacked(self):
        return self.valid_attack

    def attacked(self):
        self.valid_attack = True
    
    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            while True:
                check[0] += direction[0]
                check[1] += direction[1]
                if check[0] == 8 or check[0] == -1 or check[1] == 8 or check[1] == -1:
                    break
                attacking = board[check[0]][check[1]]
                if not attacking.is_empty():
                    if attacking.get_type("color") != self.get_type("color"):
                        if not rek:
                            if not attacking.can_be_attacked() and self.check_for_check(deepcopy(b_copy), enemy, piece_dict, check):
                                attacking.attacked()
                        else:
                            attacking.attacked()
                    break
                if not rek:
                    if not attacking.can_be_attacked() and self.check_for_check(deepcopy(b_copy), enemy, piece_dict, check):
                        attacking.attacked()
                else:
                    attacking.attacked()
        return board
    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = copy(board[self.pos[1]][self.pos[0]])
        board[self.pos[1]][self.pos[0]] = Piece("00", (self.pos))
        king_y, king_x = piece_dict[f"{self.get_type('color')}K"]
        for piece in piece_dict[enemy]:
            if (dest[1], dest[0]) == piece.pos:
                continue
            piece.all_available(board, enemy, piece_dict, True)
            if board[king_y][king_x].can_be_attacked():
                return False
        return True
    
    def __str__(self):
        return f"{self.type}"

    def did_move(self):
        self.moved = True

    def is_empty(self):
        if self.get_type("full") == "00":
            return True
        else:
            return False
    
    def get_type(self, part):
        if part == "full":
            return self.type
        elif part == "color":
            return self.type[0]
        elif part == "figure":
            return self.type[1]
        return

class KingAndHorse(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = NO_DIR

    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            check[0] += direction[0]
            check[1] += direction[1]
            if (check[0] > 7) or (check[0] < 0) or (check[1] > 7) or (check[1] < 0):
                continue
            attacking = board[check[0]][check[1]]
            if attacking.get_type("color") == self.get_type("color"):
                continue
            if not rek:
                if not attacking.can_be_attacked() and self.check_for_check(deepcopy(b_copy), enemy, piece_dict, check):
                    attacking.attacked()
            else:
                attacking.attacked()
        return board

