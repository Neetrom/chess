from figures.piece import Piece

class Queen(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = [[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]]
