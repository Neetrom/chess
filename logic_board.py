from settings import  PIECES
from copy import deepcopy
from figures.import_pieces import IMPORT_PIECES
from figures.piece import Piece
from cell import Cell


class Logic_Board():
    def __init__(self):
        self.color_pieces = {"W": [], "B": [], "WK": (0,0), "BK": (0,0)}
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        self.cell_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]]
        self.import_pieces()
        self.move_board = []
        self.previous_piece = 0

    def import_pieces(self):
        for row_index, row in enumerate(PIECES):
            for col_index, val in enumerate(row):
                self.add_piece(val, col_index, row_index)

    def get_cells(self):
        return self.cell_board

    def make_a_move_if_valid(self, starting_tile, target, turn, enemy):
        self.generate_moves(starting_tile, enemy)

        if not self.wrong_figure_picked(starting_tile, target):
            return True
        
        if not self.is_tile_empty(target):
            self.kill_piece(target, enemy)

        self.move_piece(starting_tile, target)

        self.king_logic(starting_tile, target, turn)

        self.pawn_logic(starting_tile, target, enemy)

        return False

    def move_piece(self, starting_tile, target):
        self.board[target.y][target.x] = self.board[starting_tile.y][starting_tile.x]
        self.board[target.y][target.x].update_pos((target.x, target.y))
        self.empty_space(starting_tile)

        self.mark_piece_movement(target)

    def king_logic(self,starting_tile, target, turn):
        if self.get_figure_of_piece(target) != "K":
            return
        self.update_king_pos(target, turn)
        self.castle(starting_tile, target)
    
    def castle(self, starting_tile, target):
        temp = abs(target.x - starting_tile.x)
        if temp < 2:
            return
        if target.x == 2:
           rook_start = self.cell_at_cords(target.x-2, target.y)
           rook_target = self.cell_at_cords(target.x+1, target.y)
        else:
            rook_start = self.cell_at_cords(target.x+1, target.y)
            rook_target = self.cell_at_cords(target.x-1, target.y)
        self.move_piece(rook_start, rook_target)

    def pawn_logic(self, starting_tile, target, enemy):
        self.turn_off_en_pass_for_the_last_piece()
        if self.get_figure_of_piece(target) != "P":
            return
        if target.y == 7 or target.y == 0:
            color = self.get_color_of_piece(target)
            self.kill_piece(target, color)
            self.add_piece(f"{color}Q", target.x, target.y)
        if abs(target.y-starting_tile.y) == 2:
            self.mark_en_pass(target)
        
        self.pass_enn(starting_tile, target, enemy)
            
    def pass_enn(self, starting_tile, target, enemy):
        if starting_tile.x == target.x:
            return
        if not self.piece_from_target(target).is_empty():
            return
        en_pass_target = self.cell_at_cords(target.x, starting_tile.y)
        self.kill_piece(en_pass_target, enemy)

    def wrong_figure_picked(self, starting_tile, target):
        attacked = self.move_board[target.y][target.x]
        if not attacked.can_be_attacked():
            return False
        if (target.x == starting_tile.x and target.y == starting_tile.y):
            return False
        if attacked.color() == self.piece_from_target(starting_tile).color():
            return False
        return True

    def piece_from_target(self, target):
        return self.board[target.y][target.x]

    def cell_at_cords(self, x, y):
        return self.get_cells()[y][x]

    def add_piece(self, type, x, y):
        new_cell = Cell(x, y)
        if type == "00":
            piece = Piece(type, (x, y))
        else:
            new_cell.place_piece()
            piece = IMPORT_PIECES.get(type[1])(type, (x, y))
            self.color_pieces[type[0]].append(piece)
        self.board[y][x] = piece
        self.cell_board[y][x] = new_cell
        if type[1] == "K":
            self.color_pieces[type] = new_cell

    def kill_piece(self, target, enemy):
        self.color_pieces[enemy].remove(self.board[target.y][target.x])
        self.cell_board[target.y][target.x].remove_piece()
        self.board[target.y][target.x] = Piece("00", (target.x, target.y))
    
    def empty_space(self, target):
        self.board[target.y][target.x] = Piece("00", (target.x, target.y))
        self.cell_board[target.y][target.x].remove_piece()
        
    def mark_piece_movement(self, target):
        self.piece_from_target(target).did_move()

    def update_king_pos(self, target, turn):
        self.color_pieces[f"{turn}K"] = target

    def get_type_of_piece(self, target):
        return self.piece_from_target(target).full_type()
    
    def get_color_of_piece(self, target):
        return self.piece_from_target(target).color()
    
    def get_figure_of_piece(self, target):
        return self.piece_from_target(target).figure()
    
    def generate_moves(self, target, enemy):
        self.move_board = self.piece_from_target(target).all_available(deepcopy(self.get_board()), enemy, self.color_pieces, False)
        return self.move_board
    
    def mark_en_pass(self, target):
        self.piece_from_target(target).en()
        self.previous_piece = self.piece_from_target(target)
    
    def turn_off_en_pass_for_the_last_piece(self):
        if self.previous_piece != 0:
            self.previous_piece.cant_en_passa()
            self.previous_piece = 0
    
    def get_color_pieces(self):
        return self.color_pieces

    def is_tile_empty(self, target):
        return self.piece_from_target(target).is_empty()
    
    def get_board(self):
        return self.board