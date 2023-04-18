import pygame
from settings import QUEEN_DIR
from piece_class import KingAndHorse

class King(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
        self.moved = False
    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = board[self.pos[1]][self.pos[0]]
        board[self.pos[1]][self.pos[0]] = 0
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if board[dest[0]][dest[1]] != self.type:
                return False
        return True