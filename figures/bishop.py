from copy import deepcopy, copy
from piece_class import Piece
from single_tile_attack_piece import Single_Tile_Attack_Class
from settings import HORSE_DIR, BISH_DIR, ROOK_DIR, QUEEN_DIR


class Bishop(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = BISH_DIR