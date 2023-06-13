from figures.piece import Piece

class Rook(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.moved = False