from copy import deepcopy, copy
from piece_class import Piece
from settings import ROOK_DIR

class Rook(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = ROOK_DIR
        self.moved = False