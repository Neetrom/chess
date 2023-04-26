from settings import QUEEN_DIR
from single_tile_attack_piece import Single_Tile_Attack_Class
from copy import copy, deepcopy
from piece_class import Piece

class King(Single_Tile_Attack_Class):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
        self.moved = False

    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            self.roszada(board, enemy, piece_dict, rek)
        return super().all_available(board, enemy, piece_dict, rek)
    
    def roszada(self, board, enemy, piece_dict, rek):
        if self.did_it_move():
            return
        if not self.check_for_check(deepcopy(board), enemy, piece_dict, (self.pos[1], self.pos[0])):
            return
        
        self.right_roszada(board, enemy, piece_dict, rek)
        self.left_roszada(board, enemy, piece_dict, rek)
        
    def right_roszada(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x+3].did_it_move():
            return
        if board[y][x+3].full_type() != f"{self.color()}R":
            return
        if not board[y][x+1].is_empty() or not board[y][x+2].is_empty():
            return
        if not rek:
            if not self.check_for_check(deepcopy(board), enemy, piece_dict, (y, x+1)):
                return
            if not self.check_for_check(deepcopy(board), enemy, piece_dict, (y, x+2)):
                return
        board[y][x+2].attacked()

    def left_roszada(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x-4].full_type() != f"{self.color()}R":
            return
        if board[y][x-4].did_it_move():
            return
        if not board[y][x-3].is_empty() or not board[y][x-2].is_empty() or not board[y][x-1].is_empty():
            return
        if not rek:
            if not self.check_for_check(deepcopy(board), enemy, piece_dict, (y, x-1)):
                return
            if not self.check_for_check(deepcopy(board), enemy, piece_dict, (y, x-2)):
                return
        board[y][x-2].attacked()


    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = copy(board[self.pos[1]][self.pos[0]])
        board[self.pos[1]][self.pos[0]] = Piece("00", (self.pos))
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if board[dest[0]][dest[1]].can_be_attacked():
                return False
        return True