import pygame, sys
from settings import *
from copy import deepcopy, copy
from king import King
from pawn import Pawn
from basic_pieces import Rook, Queen, Bishop, Horse
from piece_class import Piece, Graphic_piece

IMPORT_PIECES = {"Q": Queen, "K": King, "P": Pawn, "B": Bishop, "H": Horse, "R": Rook}

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
        
        self.logic_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
                
        
        self.piece_group = pygame.sprite.Group()
        self.color_pieces = {"W": [], "B": [], "WK": (0,0), "BK": (0,0)}
        self.import_pieces()
        self.x = 0
        self.y = 0
        self.copy = 0
        self.move_board = []
        
        self.turn = "W"
        self.enemy = "B"

        self.won = "None"

        self.game_active = True
        self.promo_menu_bool = False

        self.direction = 0

        self.prev = 0


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
                if val == "00":
                    piece = Piece(val, (col_index, row_index))
                else:
                    graphic_piece = Graphic_piece(val, (col_index, row_index))
                    piece = IMPORT_PIECES.get(val[1])(val, (col_index, row_index))

                    self.color_pieces[val[0]].append(piece)
                    self.piece_group.add(graphic_piece)
                    self.graphics_piece_board[row_index][col_index] = graphic_piece

                self.logic_board[row_index][col_index] = piece
                if val[1] == "K":
                    self.color_pieces[val] = (row_index, col_index)
    
    def get_cords(self):
        x,y = pygame.mouse.get_pos()
        x = (x-x%TILE_SIZE)//TILE_SIZE
        y = (y-y%TILE_SIZE)//TILE_SIZE
        return x,y

    def mouse_move(self):
        if self.copy != 0:
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
        else:
            self.x, self.y = self.get_cords()
            if self.logic_board[self.y][self.x].is_empty():
                return
            if self.logic_board[self.y][self.x].get_type("color") != self.turn:
                return
            self.move_board = self.logic_board[self.y][self.x].all_available(deepcopy(self.logic_board), self.enemy, self.color_pieces, False)
        
        self.draw_trans()

    def draw_trans(self):
        if self.logic_board[self.y][self.x].is_empty():
            return
        for row_index, row in enumerate(self.move_board):
            for col_index, val in enumerate(row):
                if val.can_be_attacked():
                    pygame.draw.circle(self.screen, (130, 237, 92),(col_index*TILE_SIZE+50, row_index*TILE_SIZE+50), 20)
        self.copy = pygame.image.load(f"graphics/{self.logic_board[self.y][self.x].get_type('full')}.png").convert_alpha()
        pygame.Surface.set_alpha(self.copy, 100)
        copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
        self.screen.blit(self.copy, copy_rect)
    

    def move_pieces(self, start_y, start_x, dest_y, dest_x):
        if not self.logic_board[dest_y][dest_x].is_empty():
            pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y][dest_x])
        self.graphics_piece_board[dest_y][dest_x] = self.graphics_piece_board[start_y][start_x]
        self.graphics_piece_board[dest_y][dest_x].update_pos((dest_x, dest_y))
        self.graphics_piece_board[start_y][start_x] = 0

        self.logic_board[dest_y][dest_x] = self.logic_board[start_y][start_x]
        self.logic_board[dest_y][dest_x].update_pos((dest_x, dest_y))
        self.logic_board[start_y][start_x] = Piece("00", (start_x, start_y))

        self.logic_board[dest_y][dest_x].did_move()

    def wrong_figure_picked(self, dest_x, dest_y, attacked):
        if not attacked.can_be_attacked():
            return False
        if (dest_x == self.x and dest_y == self.y):
            return False
        if attacked.get_type("color") == self.move_board[self.y][self.x].get_type("color"):
            return False
        return True

    def update_king_pos(self, x, y):
        self.color_pieces[f"{self.turn}K"] = (y, x)
    
    def king_logic(self, x, y):
        if self.logic_board[y][x].get_type("figure") != "K":
            return
        self.update_king_pos(x, y)
        temp = abs(self.x - x)
        if temp < 2:
            return
        if x == 2:
           self.move_pieces(y, x-2, y, x+1)
        else:
            self.move_pieces(y, x+1, y, x-1)
        
    def pass_enn(self, start_y, start_x, x, y):
        if start_x == x:
            return
        if not self.move_board[y][x].is_empty():
            return
        pygame.sprite.Sprite.kill(self.graphics_piece_board[start_y][x])
        self.graphics_piece_board[start_y][x] = 0
        self.logic_board[start_y][x] = Piece("00", (x, start_y))
        

    def pawn_logic(self, start_y, start_x, x, y):
        if self.logic_board[y][x].get_type("figure") != "P":
            return
        if abs(y-start_y) == 2:
            self.logic_board[y][x].en()
            self.prev = self.logic_board[y][x]
        
        self.open_promo(x, y)
        
        self.pass_enn(start_y, start_x, x, y)

    def open_promo(self, x, y):
        if y != 0 and y != 7:
            return
        self.promo_menu_bool = True
        self.gen_promo_menu()
        while self.promo_menu_bool:
            self.handle_promo(x, y)

    def check_valid_move(self):
        dest_x, dest_y = pygame.mouse.get_pos()
        dest_x = (dest_x-dest_x%TILE_SIZE)//TILE_SIZE
        dest_y = (dest_y-dest_y%TILE_SIZE)//TILE_SIZE
        attacked = self.move_board[dest_y][dest_x]

        if not self.wrong_figure_picked(dest_x, dest_y, attacked):
            return
        
        if self.prev != 0:
            self.prev.ne()
            self.prev = 0
        
        self.move_pieces(self.y, self.x, dest_y, dest_x)

        self.king_logic(dest_x, dest_y)

        self.pawn_logic(self.y, self.x, dest_x, dest_y)

        if self.turn == "W":
            self.turn = "B"
            self.enemy = "W"
        else:
            self.turn = "W"
            self.enemy = "B"
        

    def gen_promo_menu(self):
        self.promo_menu = pygame.surface.Surface((TILE_SIZE*4, TILE_SIZE))
        self.promo_menu.fill((140, 232, 130))
        separator = pygame.surface.Surface((4, TILE_SIZE))
        separator.fill("black")
        
        i = 0
        for piece in PROMO:
            image = pygame.image.load(f"graphics/{self.turn}{piece}.png")
            image_rect = image.get_rect(topleft=(i, 0))
            self.promo_menu.blit(image, image_rect)
            self.promo_menu.blit(separator, (i,0))
            i = i+TILE_SIZE

        self.promo_menu.blit(separator, (i-5,0))
        border = pygame.transform.scale(separator, (TILE_SIZE*4, 4))
        self.promo_menu.blit(border, (0,0))
        self.promo_menu.blit(border, (0,TILE_SIZE-5))

        self.promo_menu = pygame.transform.rotozoom(self.promo_menu, 0, 1.1)
        self.promo_menu_rect = self.promo_menu.get_rect(center=(BOARD_SIZE[0]/2, BOARD_SIZE[1]/2))
        


    def pick_promo(self, dest_x, dest_y):
        if not pygame.mouse.get_pressed()[0]:
            return
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.promo_menu_rect, mouse_pos):
            x = (mouse_pos[0] - self.promo_menu_rect.topleft[0])//TILE_SIZE
            funny_dict = {0: "Q", 1: "B", 2: "H", 3: "R", 4: "R"}
            piece_type = funny_dict[x]
            
            self.color_pieces[self.turn].remove(self.logic_board[dest_y][dest_x])
            self.piece_group.remove(self.graphics_piece_board[dest_y][dest_x])
            pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y][dest_x])

            piece = IMPORT_PIECES.get(piece_type)(f"{self.turn}{piece_type}", (dest_x, dest_y))
            graphic_piece = Graphic_piece(f"{self.turn}{piece_type}", (dest_x, dest_y))

            self.color_pieces[self.turn].append(piece)
            self.graphics_piece_board[dest_y][dest_x] = graphic_piece
            self.piece_group.add(graphic_piece)
            self.logic_board[dest_y][dest_x] = piece

            self.promo_menu_bool = False

    def handle_promo(self, dest_x, dest_y):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.screen.blit(self.promo_menu, self.promo_menu_rect)
        self.pick_promo(dest_x, dest_y)
        pygame.display.update()

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