import pygame
from copy import deepcopy, copy
from piece_class import Piece

class Pawn(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.moved = False
        self.en_pass = False
    
    def all_available(self, board, enemy, piece_dict, rek = False):
        b_copy = deepcopy(board)
        if self.en_pass:
            self.en_pass = False
        if self.type[0] == "W":
            direction = -1
        else:
            direction = 1
        if board[self.pos[1]+direction][self.pos[0]] == 0:
            if not rek:
                if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction,self.pos[0])):
                    board[self.pos[1]+direction][self.pos[0]] = "X"
            else:
                board[self.pos[1]+direction][self.pos[0]] = "X"
        if (not self.moved) and (board[self.pos[1]+direction*2][self.pos[0]] == 0) and (board[self.pos[1]+direction][self.pos[0]] == "X"):
            if not rek:
                if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction*2, self.pos[0])):
                    board[self.pos[1]+direction*2][self.pos[0]] = "XL"
            else:
                board[self.pos[1]+direction*2][self.pos[0]] = "XL"
        if (self.pos[0] + 1) < 8:
            if board[self.pos[1]+direction][self.pos[0]+1] != 0 and board[self.pos[1]+direction][self.pos[0]+1][0] != self.type[0]:
                if not rek:
                    if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction, self.pos[0]+1)):
                        board[self.pos[1]+direction][self.pos[0]+1] = "X"
                else:
                    board[self.pos[1]+direction][self.pos[0]+1] = "X"
        if (self.pos[0] - 1) >= 0:
            if board[self.pos[1]+direction][self.pos[0]-1] != 0 and board[self.pos[1]+direction][self.pos[0]-1][0] != self.type[0]:
                if not rek:
                    if self.check_for_check(deepcopy(b_copy), enemy, piece_dict, (self.pos[1]+direction, self.pos[0]-1)):
                        board[self.pos[1]+direction][self.pos[0]-1] = "X"
                else:
                    board[self.pos[1]+direction][self.pos[0]-1] = "X"
        return board

    def en(self):
        self.en_pass = True
    
    def ne(self):
        self.en_pass = False