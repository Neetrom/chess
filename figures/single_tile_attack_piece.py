from figures.piece import Piece
from copy import deepcopy, copy

class Single_Tile_Attack_Class(Piece):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = []

    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            check[0] += direction[0]
            check[1] += direction[1]
            if (check[0] > 7) or (check[0] < 0) or (check[1] > 7) or (check[1] < 0):
                continue
            attacking = board[check[0]][check[1]]
            if attacking.color() == self.color():
                continue
            if not rek:
                if not self.illegal_move(deepcopy(b_copy), enemy, piece_dict, check):
                    attacking.attacked()
            else:
                attacking.attacked()
        return board

