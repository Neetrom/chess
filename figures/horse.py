from figures.single_tile_attack_piece import Single_Tile_Attack_Class

class Horse(Single_Tile_Attack_Class):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [-2, 1], [2, -1], [-2, -1]]