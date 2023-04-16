from copy import deepcopy, copy
from piece_class import Piece, KingAndHorse
from settings import HORSE_DIR, BISH_DIR, ROOK_DIR, QUEEN_DIR


        

class Horse(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = HORSE_DIR

class Bishop(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = BISH_DIR

class Queen(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR

class Rook(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = ROOK_DIR
        self.moved = False