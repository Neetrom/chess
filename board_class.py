from settings import TILE_SIZE, BOARD_SIZE, BOARD_TILES, PIECES, get_cords
from graphic_piece import Graphic_piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        self.import_pieces()
        self.move_board = []

    def import_pieces(self):
        for row_index, row in enumerate(PIECES):
            for col_index, val in enumerate(row):
                self.add_piece(val, col_index, row_index)

    def add_piece(self, val, x, y):
        pass

    def move_pieces(self, start_y, start_x, dest_y, dest_x):
        self.board[dest_y][dest_x] = self.board[start_y][start_x]
        self.board[dest_y][dest_x].update_pos((dest_x, dest_y))
        self.empty_space(start_x, start_y)
    
    def empty_space(self, x, y):
        self.board[y][x] = 0
    

    def kill_piece(self, x, y):
        self.board[y][x] = 0
    
    def get_board(self):
        return self.board
    
    def get_moves(self):
        return self.move_board

    def wrong_figure_picked(self, dest_x, dest_y):
        attacked = self.move_board[dest_y][dest_x]
        if not attacked.can_be_attacked():
            return False
        if (dest_x == self.x and dest_y == self.y):
            return False
        if attacked.color() == self.move_board[self.y][self.x].color():
            return False
        return True