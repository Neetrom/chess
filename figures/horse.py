from copy import deepcopy, copy
from single_tile_attack_piece import Single_Tile_Attack_Class
from settings import HORSE_DIR


class Horse(Single_Tile_Attack_Class):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = HORSE_DIR