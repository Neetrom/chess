import pygame, sys
from settings import *
from pieces import Piece, Rook, Queen, Pawn, Bishop, King, Horse
from copy import deepcopy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")
        self.board = pygame.surface.Surface(BOARD_SIZE)
        self.generate_board()
        self.graphics_piece_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
                

        self.pieces = PIECES
        
        self.piece_group = pygame.sprite.Group()
        self.kings = []
        self.import_pieces()
        self.x = 0
        self.y = 0
        self.copy = 0
        self.move_board = []
        
        self.turn = "W"

        self.won = "None"

        self.game_active = True


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
        for row_index, row in enumerate(self.pieces):
            for col_index, val in enumerate(row):
                if val != 0:
                    temp_piece = Piece(val, (col_index, row_index))
                    if val[1] == "R":
                        rook = Rook(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = rook
                        self.piece_group.add(rook)
                    elif val[1] == "Q":
                        queen = Queen(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = queen
                        self.piece_group.add(queen)
                    elif val[1] == "P":
                        pawn = Pawn(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = pawn
                        self.piece_group.add(pawn)
                    elif val[1] == "B":
                        bishop = Bishop(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = bishop
                        self.piece_group.add(bishop)
                    elif val[1] == "K":
                        king = King(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = king
                        self.piece_group.add(king)
                        self.kings.append(king)
                    elif val[1] == "H":
                        horse = Horse(val, (col_index, row_index))
                        self.graphics_piece_board[row_index][col_index] = horse
                        self.piece_group.add(horse)
    
    def mouse_move(self):
        if self.copy != 0:
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
        else:
            x,y = pygame.mouse.get_pos()
            self.x = int((x-x%TILE_SIZE)/TILE_SIZE)
            self.y = int((y-y%TILE_SIZE)/TILE_SIZE)
            if self.pieces[self.y][self.x] != 0:
                if self.pieces[self.y][self.x][0] != self.turn:
                    return
                self.move_board = self.graphics_piece_board[self.y][self.x].all_available(deepcopy(self.pieces))
        if self.pieces[self.y][self.x] != 0:
            for row_index, row in enumerate(self.move_board):
                for col_index, val in enumerate(row):
                    if val == "X":
                        pygame.draw.circle(self.screen, (130, 237, 92),(col_index*TILE_SIZE+50, row_index*TILE_SIZE+50), 20)
            self.copy = pygame.image.load(f"graphics/{self.pieces[self.y][self.x]}.png").convert_alpha()
            pygame.Surface.set_alpha(self.copy, 180)
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
            
    def check_valid_move(self):
        dest_x, dest_y = pygame.mouse.get_pos()
        dest_x = int((dest_x-dest_x%TILE_SIZE)/TILE_SIZE)
        dest_y = int((dest_y-dest_y%TILE_SIZE)/TILE_SIZE)
        if dest_x != self.x or dest_y != self.y:
            if self.move_board[dest_y][dest_x] == "X":
                if self.graphics_piece_board[dest_y][dest_x] != 0:
                    pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y][dest_x])
                self.graphics_piece_board[dest_y][dest_x] = self.graphics_piece_board[self.y][self.x]
                self.graphics_piece_board[dest_y][dest_x].update_pos((dest_x, dest_y))
                self.graphics_piece_board[self.y][self.x] = 0

                if self.pieces[dest_y][dest_x] != 0 and self.pieces[dest_y][dest_x][1] == "K":
                    self.game_active = False
                    self.won = self.pieces[self.y][self.x][0]

                self.pieces[dest_y][dest_x] = self.pieces[self.y][self.x]
                self.pieces[self.y][self.x] = 0


                if self.turn == "W":
                    self.turn = "B"
                else:
                    self.turn = "W"
        elif self.pieces[dest_y][dest_x][1] == "P":
            self.graphics_piece_board[dest_y][dest_x].didnt_move()

    def run(self):
        self.screen.blit(self.board, (0,0))
        self.piece_group.update()
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
    while game.game_active:
        game.run()