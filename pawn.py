import pygame
from copy import deepcopy, copy
from piece_class import Piece

class Pawn(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.moved = False
        self.en_pass = False
    
    def all_available(self, board, enemy, piece_dict, rek):
        b_copy = deepcopy(board)

        if self.get_type("color") == "W":
            direction = -1
        else:
            direction = 1

        self.go_one(board, enemy, piece_dict, rek, b_copy, direction)
        self.go_two(board, enemy, piece_dict, rek, b_copy, direction)
        self.attack_left(board, enemy, piece_dict, rek, b_copy, direction)
        self.attack_right(board, enemy, piece_dict, rek, b_copy, direction)

        return board

    def go_one(self, board, enemy, piece_dict, rek, b_copy, direction):
        if not board[self.pos[1]+direction][self.pos[0]].is_empty():
            return
        if not rek:
            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction,self.pos[0])):
                board[self.pos[1]+direction][self.pos[0]].attacked()
        else:
            board[self.pos[1]+direction][self.pos[0]].attacked()

    def go_two(self, board, enemy, piece_dict, rek, b_copy, direction):
        if self.moved:
            return
        if not board[self.pos[1]+direction][self.pos[0]].can_be_attacked():
            return
        if not board[self.pos[1]+direction*2][self.pos[0]].is_empty():
            return
        if not rek:
            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction*2, self.pos[0])):
                board[self.pos[1]+direction*2][self.pos[0]].attacked()
        else:
            board[self.pos[1]+direction*2][self.pos[0]].attacked()

    def attack_right(self, board, enemy, piece_dict, rek, b_copy, direction):
        if (self.pos[0] + 1) > 7:
            return
        if board[self.pos[1]+direction][self.pos[0]+1].is_empty() or board[self.pos[1]+direction][self.pos[0]+1].get_type("color") == self.get_type("color"):
            return
        if not rek:
            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction, self.pos[0]+1)):
                board[self.pos[1]+direction][self.pos[0]+1].attacked()
        else:
            board[self.pos[1]+direction][self.pos[0]+1].attacked()

    def attack_left(self, board, enemy, piece_dict, rek, b_copy, direction):
        if (self.pos[0] - 1) < 0:
            return
        if board[self.pos[1]+direction][self.pos[0]-1].is_empty() or board[self.pos[1]+direction][self.pos[0]-1].get_type("color") == self.get_type("color"):
            return
        if not rek:
            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction, self.pos[0]-1)):
                board[self.pos[1]+direction][self.pos[0]-1].attacked()
        else:
            board[self.pos[1]+direction][self.pos[0]-1].attacked()

    def en(self):
        self.en_pass = True
    
    def ne(self):
        self.en_pass = False