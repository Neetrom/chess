from settings import QUEEN_DIR
from piece_class import KingAndHorse
from copy import copy, deepcopy
from piece_class import Piece

class King(KingAndHorse):
    def __init__(self, piece_type, pos):
        super().__init__(piece_type, pos)
        self.directions = QUEEN_DIR
        self.moved = False

    def all_available(self, board, enemy, piece_dict, rek):
        # self.roszada(board, enemy, piece_dict, rek)
        return super().all_available(board, enemy, piece_dict, rek)
    
    def roszada(self, board, enemy, piece_dict, rek):
        if self.did_it_move():
            return
        if self.check_for_check(deepcopy(board), enemy, piece_dict, (self.pos[1], self.pos[0])):
            return
        
    def right_roszada(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x+3].get_type("full") != f"{self.get_type('color')}R":
            return
        if board[y][x+3].did_it_move():
            return
        if not self.pieces[y][x+1].empty() or not self.pieces[y][x+2].empty():
            return

    def left_roszada(self, board, enemy, piece_dict, rek):
        x, y = self.pos
        if board[y][x-4].get_type("full") != f"{self.get_type('color')}R":
            return
        if board[y][x-4].did_it_move():
            return
        if not self.pieces[y][x-3].empty() or not self.pieces[y][x-2].empty() or not self.pieces[y][x-1].empty():
            return


    
    def check_for_check(self, board, enemy, piece_dict, dest):
        board[dest[0]][dest[1]] = copy(board[self.pos[1]][self.pos[0]])
        board[self.pos[1]][self.pos[0]] = Piece("00", (self.pos))
        for piece in piece_dict[enemy]:
            piece.all_available(board, enemy, piece_dict, True)
            if board[dest[0]][dest[1]].can_be_attacked():
                return False
        return True