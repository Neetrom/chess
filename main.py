import pygame, sys
from settings import *
from pieces import Piece, Rook

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")
        self.board = pygame.surface.Surface(BOARD_SIZE)
        self.generate_board()
        self.logic_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
                

        self.pieces = [["BR", "BH", "BB", "BQ", "BK", "BB", "BH", "BR"],
                       ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                       ["WR", "WH", "WB", "WQ", "WK", "WB", "WH", "WR"]]
        
        self.piece_group = pygame.sprite.Group()
        self.import_pieces()
        self.x = 0
        self.y = 0
        self.copy = 0


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
                self.board.blit(tile, tile_rect)

    def import_pieces(self):
        for row_index, row in enumerate(PIECES):
            for col_index, val in enumerate(row):
                if val:
                    temp_piece = Piece(val, (col_index*TILE_SIZE, row_index*TILE_SIZE))
                    self.piece_group.add(temp_piece)
                    if val[1] == "R":
                        self.logic_board[row_index][col_index] = Rook(val[0], (row_index, col_index))
    
    def mouse_move(self):
        x, y = pygame.mouse.get_pos()
        x = int((x-x%TILE_SIZE)/TILE_SIZE)
        y = int((y-y%TILE_SIZE)/TILE_SIZE)
        if self.copy != 0:
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
        elif self.pieces[y][x] != 0:
            self.x = y
            self.y = x
            self.copy = pygame.image.load(f"graphics/{self.pieces[y][x].type}.png").convert_alpha()
            pygame.Surface.set_alpha(self.copy, 180)
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
            
    def check_valid_move(self):
        dest_x, dest_y = pygame.mouse.get_pos()
        dest_x = int((dest_x-dest_x%TILE_SIZE)/TILE_SIZE)
        dest_y = int((dest_y-dest_y%TILE_SIZE)/TILE_SIZE)

        temp_board = self.logic_board[self.x][self.y].all_available(self.pieces)
        if temp_board[dest_y][dest_x] == "X":
            self.logic_board[dest_y][dest_x] = self.logic_board[self.x][self.y]
            self.logic_board[self.x][self.y] = 0
 
            self.pieces[dest_y][dest_x] = self.pieces[self.x][self.y]
            self.pieces[dest_y][dest_x].update_pos((dest_x*TILE_SIZE, dest_y*TILE_SIZE))
            self.pieces[self.x][self.y] = 0

    def run(self):
        self.screen.blit(self.board, (0,0))
        self.piece_group.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            self.mouse_move()
        else:
            if self.copy != 0:
                self.check_valid_move()
                self.copy = 0

        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    while True:
        game.run()