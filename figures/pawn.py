from copy import deepcopy, copy
from figures.piece import Piece

class Pawn(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.moved = False
        self.en_pass = False
        self.direction = 0
        self.set_direction()
    
    def set_direction(self):
        if self.color() == "W":
            self.direction = -1
        else:
            self.direction = 1
    
    def all_available(self, board, enemy, piece_dict, rek):
        b_copy = deepcopy(board)


        self.go_one_forward(board, enemy, piece_dict, rek, b_copy)
        self.go_two_forward(board, enemy, piece_dict, rek, b_copy)
        self.attack_left(board, enemy, piece_dict, rek, b_copy)
        self.attack_right(board, enemy, piece_dict, rek, b_copy)
        self.en_passa(board, enemy, piece_dict, rek, b_copy)

        return board

    def go_one_forward(self, board, enemy, piece_dict, rek, b_copy):
        if not board[self.pos[1] + self.direction][self.pos[0]].is_empty():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, self.direction, 0)

    def go_two_forward(self, board, enemy, piece_dict, rek, b_copy):
        if self.moved:
            return
        tile_one_ahead = board[self.pos[1] + self.direction][self.pos[0]]
        tile_two_ahead = board[self.pos[1] + self.direction*2][self.pos[0]]

        if not tile_one_ahead.is_empty():
            return
        if not tile_two_ahead.is_empty():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, self.direction*2, 0)

    def attack_right(self, board, enemy, piece_dict, rek, b_copy):
        if self.out_of_bounds_after_a_move():
            return
        tile_attacked = board[self.pos[1] + self.direction][self.pos[0]+1]
        if tile_attacked.is_empty() or tile_attacked.color() == self.color():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, self.direction, 1)

    def attack_left(self, board, enemy, piece_dict, rek, b_copy):
        if self.out_of_bounds_after_a_move():
            return
        tile_attacked = board[self.pos[1] + self.direction][self.pos[0]-1]
        if tile_attacked.is_empty() or tile_attacked.color() == self.color():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, self.direction, -1)

    def mark_attack(self, board, enemy, piece_dict, rek, b_copy, direction, offset):
        tile_attacked = board[self.pos[1]+direction][self.pos[0]+offset]
        if not rek:
            if not self.illegal_move(deepcopy(b_copy), enemy, piece_dict, (self.pos[1] + direction, self.pos[0]+offset)):
                tile_attacked.attacked()
        else:
            tile_attacked.attacked()

    def en_passa(self, board, enemy, piece_dict, rek, b_copy):
        for offset in [-1, 1]:
            if self.out_of_bounds_en_pass(offset):
                continue
            tile_attacked = board[self.pos[1]][self.pos[0]+offset]
            if tile_attacked.is_empty():
                continue
            if tile_attacked.full_type() != f"{enemy}P":
                continue
            if tile_attacked.en_pass:
                self.mark_attack(board, enemy, piece_dict, rek, b_copy, self.direction, offset)
    
    def out_of_bounds_en_pass(self, offset):
        if (self.pos[0] + offset) > 7:
            return True
        if (self.pos[0] + offset) < 0:
            return True
        return False

    def out_of_bounds_after_a_move(self):
        if (self.pos[0] + 1) > 7:
            return True
        if (self.pos[0] - 1) < 0:
            return True

    def en(self):
        self.en_pass = True
    
    def cant_en_passa(self):
        self.en_pass = False