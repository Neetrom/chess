from settings import QUEEN_DIR
from piece_class import KingAndHorse
from copy import copy
from piece_class import Piece

class King(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
        self.moved = False
    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = copy(board[self.pos[1]][self.pos[0]])
        board[self.pos[1]][self.pos[0]] = Piece("00", (self.pos))
        king = piece_dict[f"{self.get_type('color')}K"]
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if king.can_be_attacked():
                return False
        return True