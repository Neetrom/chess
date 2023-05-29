from settings import TILE_SIZE, BOARD_SIZE, BOARD_TILES, PIECES, get_cords
import pygame
from graphic_piece import Graphic_piece
from copy import deepcopy

class Graphic_Interface():
    def __init__(self, start_piece_positions):
        pygame.init()
        self.background = pygame.surface.Surface(BOARD_SIZE)
        self.piece_group = pygame.sprite.Group()
        self.generate_board()
        self.update_board(start_piece_positions)
        self.copy = 0
        self.holding_a_piece = False
        self.x = 0
        self.y = 0

    def generate_board(self):
        for row_index, row in enumerate(BOARD_TILES):
            for col_index, val in enumerate(row):
                tile = pygame.Surface((TILE_SIZE,TILE_SIZE))
                tile_rect = tile.get_rect(topleft=(TILE_SIZE*row_index, TILE_SIZE*col_index))
                if val == 0:
                    tile.fill((238,238,210))
                else:
                    tile.fill((118,150,86))
                tile_rect = tile.get_rect(topleft=(TILE_SIZE*row_index, TILE_SIZE*col_index))
                self.background.blit(tile, tile_rect)

    def update_board(self, board):
        self.clear_board()
        for row_index, row in enumerate(board):
            for col_index, val in enumerate(row):
                self.add_piece(val.full_type(), col_index, row_index)

    def clear_board(self):
        for sprite in self.piece_group:
            sprite.kill()
            self.piece_group.remove(sprite)

    def add_piece(self, type, x, y):
        if type == "00": #tile empty
            return
        graphic_piece = Graphic_piece(f"{type}", (x, y))
        self.piece_group.add(graphic_piece)

    def get_background(self):
        return self.background
    
    def get_pieces(self):
        self.piece_group.update()
        return self.piece_group
    
    def mouse_move(self, logic_board, enemy, screen, turn):
        color_pieces = logic_board.get_color_pieces()
        board = logic_board.get_board()
        if self.holding_a_piece:
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            screen.blit(self.copy, copy_rect)
        else:
            self.x, self.y = get_cords()
            if self.tile_at_cords(self.x, self.y, board).is_empty():
                return
            if self.tile_at_cords(self.x, self.y, board).color() != turn:
                return
            self.move_board = self.tile_at_cords(self.x, self.y, board).all_available(deepcopy(board), enemy, color_pieces, False)
        self.draw_transp(board, screen)
    
    def tile_at_cords(self, x, y, board):
        return board[y][x]
    
    def get_x_y(self):
        return self.x, self.y

    def draw_board(self, screen):
        screen.blit(self.get_background(), (0,0))
        self.get_pieces().draw(screen)

    def draw_transp(self, board, screen):
        if self.tile_at_cords(self.x, self.y, board).is_empty():
            return
        for row_index, row in enumerate(self.move_board):
            for col_index, val in enumerate(row):
                if val.can_be_attacked():
                    pygame.draw.circle(screen, (130, 237, 92),(col_index*TILE_SIZE+50, row_index*TILE_SIZE+50), 20)
        self.copy = pygame.image.load(f"graphics/{self.tile_at_cords(self.x, self.y, board).full_type()}.png").convert_alpha()
        pygame.Surface.set_alpha(self.copy, 100)
        copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
        screen.blit(self.copy, copy_rect)
        self.holding_a_piece = True

    def figure_picked(self):
        if self.holding_a_piece:
            return True
        return False

    def let_go_of_a_piece(self):
        self.copy = 0
        self.holding_a_piece = False