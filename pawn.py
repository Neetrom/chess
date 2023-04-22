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
        self.en_passa(board, enemy, piece_dict, rek, b_copy, direction)

        return board

    def go_one(self, board, enemy, piece_dict, rek, b_copy, direction):
        if not board[self.pos[1]+direction][self.pos[0]].is_empty():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, direction, 0)

    def go_two(self, board, enemy, piece_dict, rek, b_copy, direction):
        if self.moved:
            return
        if not board[self.pos[1]+direction][self.pos[0]].is_empty():
            return
        if not board[self.pos[1]+direction*2][self.pos[0]].is_empty():
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, direction*2, 0)

    def attack_right(self, board, enemy, piece_dict, rek, b_copy, direction):
        if (self.pos[0] + 1) > 7:
            return
        if board[self.pos[1]+direction][self.pos[0]+1].is_empty() or board[self.pos[1]+direction][self.pos[0]+1].get_type("color") == self.get_type("color"):
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, direction, 1)

    def attack_left(self, board, enemy, piece_dict, rek, b_copy, direction):
        if (self.pos[0] - 1) < 0:
            return
        if board[self.pos[1]+direction][self.pos[0]-1].is_empty() or board[self.pos[1]+direction][self.pos[0]-1].get_type("color") == self.get_type("color"):
            return
        self.mark_attack(board, enemy, piece_dict, rek, b_copy, direction, -1)

    def mark_attack(self, board, enemy, piece_dict, rek, b_copy, direction, offset):
        if not rek:
            if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction, self.pos[0]+offset)):
                board[self.pos[1]+direction][self.pos[0]+offset].attacked()
        else:
            board[self.pos[1]+direction][self.pos[0]+offset].attacked()

    def en_passa(self, board, enemy, piece_dict, rek, b_copy, direction):
        for offset in [-1, 1]:
            if self.pos[0]+offset > 7 or self.pos[0]+offset < 1:
                continue
            if board[self.pos[1]][self.pos[0]+offset].is_empty():
                continue
            if board[self.pos[1]][self.pos[0]+offset].get_type("full") != f"{enemy}P":
                continue
            if board[self.pos[1]][self.pos[0]+offset].en_pass:
                self.mark_attack(board, enemy, piece_dict, rek, b_copy, direction, offset)


    def en(self):
        self.en_pass = True
    
    def ne(self):
        self.en_pass = False