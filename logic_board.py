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

    def make_a_move_if_valid(self, x, y, dest_x, dest_y, turn, enemy):
        self.get_moves(x, y, enemy)

        if not self.wrong_figure_picked(x, y, dest_x, dest_y):
            return True
        
        self.turn_off_en_pass()
        
        if not self.is_tile_empty(dest_x, dest_y):
            self.kill_piece(dest_x, dest_y, enemy)

        self.move_pieces(x, y, dest_x, dest_y)

        self.king_logic(x, dest_x, dest_y, turn)

        self.pawn_logic(x, y, dest_x, dest_y, enemy)

        return False

    def move_pieces(self, start_x, start_y, dest_x, dest_y):
        super().move_pieces(start_y, start_x, dest_y, dest_x)
        self.mark_piece_movement(dest_x, dest_y)

    def king_logic(self, x, dest_x, dest_y, turn):
        if self.get_figure_of_piece(dest_x, dest_y) != "K":
            return
        self.update_king_pos(dest_x, dest_y, turn)
        self.roszada(x, dest_x, dest_y)
    
    def roszada(self, x, dest_x, y):
        temp = abs(dest_x - x)
        if temp < 2:
            return
        if dest_x == 2:
           self.move_pieces(dest_x-2, y, dest_x+1, y)
        else:
            self.move_pieces(dest_x+1, y, dest_x-1, y)

    def pawn_logic(self, start_x, start_y, x, y, enemy):
        if self.get_figure_of_piece(x, y) != "P":
            return
        if abs(y-start_y) == 2:
            self.mark_en_pass(x, y)
        
        self.pass_enn(start_x, start_y, x, y, enemy)
            
    def pass_enn(self, start_x, start_y, x, y, enemy):
        if start_x == x:
            return
        if not self.move_board[y][x].is_empty():
            return
        self.kill_piece(x, start_y, enemy)

    def wrong_figure_picked(self, x, y, dest_x, dest_y):
        attacked = self.move_board[dest_y][dest_x]
        if not attacked.can_be_attacked():
            return False
        if (dest_x == x and dest_y == y):
            return False
        if attacked.color() == self.move_board[y][x].color():
            return False
        return True

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