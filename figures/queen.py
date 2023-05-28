from copy import deepcopy, copy
from piece_class import Piece
from settings import QUEEN_DIR

class Queen(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
