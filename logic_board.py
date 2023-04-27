from settings import TILE_SIZE, BOARD_SIZE, BOARD_TILES, PIECES, get_cords
from copy import deepcopy
from board_class import Board
from import_pieces import IMPORT_PIECES
from piece_class import Piece


class Logic_Board(Board):
    def __init__(self):
        self.color_pieces = {"W": [], "B": [], "WK": (0,0), "BK": (0,0)}
        super().__init__()
        self.prev = 0

    def add_piece(self, type, x, y):
        if type == "00":
            piece = Piece(type, (x, y))
        else:
            piece = IMPORT_PIECES.get(type[1])(type, (x, y))
            self.color_pieces[type[0]].append(piece)
        self.board[y][x] = piece
        if type[1] == "K":
            self.color_pieces[type] = (y, x)

    def kill_piece(self, x, y, enemy):
        self.color_pieces[enemy].remove(self.board[y][x])
        self.board[y][x] = Piece("00", (x, y))
    
    def empty_space(self, x, y):
        self.board[y][x] = Piece("00", (x, y))
        
    def mark_piece_movement(self, x, y):
        self.board[y][x].did_move()

    def update_king_pos(self, x, y, turn):
        self.color_pieces[f"{turn}K"] = (y, x)

    def get_type_of_piece(self, x, y):
        return self.board[y][x].full_type()
    
    def get_color_of_piece(self, x, y):
        return self.board[y][x].color()
    
    def get_figure_of_piece(self, x, y):
        return self.board[y][x].figure()
    
    def get_moves(self, x, y, enemy):
        self.move_board = self.board[y][x].all_available(deepcopy(self.board), enemy, self.color_pieces, False)
        return self.move_board
    
    def mark_en_pass(self, x, y):
        self.board[y][x].en()
        self.prev = self.board[y][x]
    
    def turn_off_en_pass(self):
        if self.prev != 0:
            self.prev.ne()
            self.prev = 0
    
    def get_color_pieces(self):
        return self.color_pieces

    def is_tile_empty(self, x, y):
        return self.board[y][x].is_empty()