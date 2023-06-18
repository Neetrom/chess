from figures.single_tile_attack_piece import Single_Tile_Attack_Class
from copy import copy, deepcopy

class King(Single_Tile_Attack_Class):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = [[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]]
        self.moved = False

    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            self.castle(board, enemy, piece_dict, rek)
        return super().all_available(board, enemy, piece_dict, rek)
    
    def castle(self, board, enemy, piece_dict, rek):
        if self.did_it_move():
            return
        if self.illegal_move(deepcopy(board), enemy, piece_dict, (self.pos[1], self.pos[0])):
            return
        
        self.left_castle(board, enemy, piece_dict, rek)
        
    def right_castle(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x+3].did_it_move():
            return
        if board[y][x+3].full_type() != f"{self.color()}R":
            return
        if not board[y][x+1].is_empty() or not board[y][x+2].is_empty():
            return
        if not rek:
            if self.illegal_move(deepcopy(board), enemy, piece_dict, (y, x+1)):
                return
            if self.illegal_move(deepcopy(board), enemy, piece_dict, (y, x+2)):
                return
        board[y][x+2].attacked()

    def left_castle(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x-4].full_type() != f"{self.color()}R":
            return
        if board[y][x-4].did_it_move():
            return
        if not board[y][x-3].is_empty() or not board[y][x-2].is_empty() or not board[y][x-1].is_empty():
            return
        if not rek:
            if self.illegal_move(deepcopy(board), enemy, piece_dict, (y, x-1)):
                return
            if self.illegal_move(deepcopy(board), enemy, piece_dict, (y, x-2)):
                return
        board[y][x-2].attacked()

    
    def illegal_move(self, board, enemy, piece_dict, dest):
        board = self.board_after_temporary_move_of_this_piece(board, dest)
        king = board[dest[0]][dest[1]]
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if king.can_be_attacked():
                return True
        return False