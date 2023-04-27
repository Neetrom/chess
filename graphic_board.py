from settings import TILE_SIZE, BOARD_SIZE, BOARD_TILES, PIECES, get_cords
import pygame
from graphic_piece import Graphic_piece
from copy import deepcopy
from board_class import Board

class Graphic_Board(Board):
    def __init__(self):
        pygame.init()
        self.board_tiles = pygame.surface.Surface(BOARD_SIZE)
        self.piece_group = pygame.sprite.Group()
        super().__init__()
        self.generate_board()
        self.move_board = []
        self.copy = 0
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
                self.board_tiles.blit(tile, tile_rect)


    def kill_piece(self, x, y):
        pygame.sprite.Sprite.kill(self.board[y][x])
        self.piece_group.remove(self.board[y][x])
        super().kill_piece(x, y)

    def add_piece(self, type, x, y):
        if type == "00":
            return
        graphic_piece = Graphic_piece(f"{type}", (x, y))
        self.board[y][x] = graphic_piece
        self.piece_group.add(graphic_piece)

    def get_background(self):
        return self.board_tiles
    
    def get_pieces(self):
        self.piece_group.update()
        return self.piece_group
    
    def mouse_move(self, logic_board, enemy, color_pieces, screen, turn):
        if self.copy != 0:
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            screen.blit(self.copy, copy_rect)
        else:
            self.x, self.y = get_cords()
            if logic_board[self.y][self.x].is_empty():
                return
            if logic_board[self.y][self.x].color() != turn:
                return
            self.move_board = logic_board[self.y][self.x].all_available(deepcopy(logic_board), enemy, color_pieces, False)
        self.draw_trans(logic_board, screen)
    
    def get_x_y(self):
        return self.x, self.y

    def draw_trans(self, logic_board, screen):
        if logic_board[self.y][self.x].is_empty():
            return
        for row_index, row in enumerate(self.move_board):
            for col_index, val in enumerate(row):
                if val.can_be_attacked():
                    pygame.draw.circle(screen, (130, 237, 92),(col_index*TILE_SIZE+50, row_index*TILE_SIZE+50), 20)
        self.copy = pygame.image.load(f"graphics/{logic_board[self.y][self.x].full_type()}.png").convert_alpha()
        pygame.Surface.set_alpha(self.copy, 100)
        copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
        screen.blit(self.copy, copy_rect)