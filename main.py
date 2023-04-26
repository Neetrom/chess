import pygame, sys
from settings import *
from copy import deepcopy, copy
from king import King
from pawn import Pawn
from basic_pieces import Rook, Queen, Bishop, Horse
from piece_class import Piece
from graphic_piece import Graphic_piece
from graphic_board import Graphic_Board
from import_pieces import IMPORT_PIECES


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")

        self.graphic_board = Graphic_Board()

        self.logic_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
                
        
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


    def import_pieces(self):
        for row_index, row in enumerate(PIECES):
            for col_index, val in enumerate(row):
                if val == "00":
                    piece = Piece(val, (col_index, row_index))
                else:
                    piece = IMPORT_PIECES.get(val[1])(val, (col_index, row_index))
                    self.color_pieces[val[0]].append(piece)

                self.logic_board[row_index][col_index] = piece
                if val[1] == "K":
                    self.color_pieces[val] = (row_index, col_index)
    

    def move_pieces(self, start_y, start_x, dest_y, dest_x):
        if not self.logic_board[dest_y][dest_x].is_empty():
            self.graphic_board.kill_piece(dest_x, dest_y)
            self.color_pieces[self.enemy].remove(self.logic_board[dest_y][dest_x])

        self.graphic_board.move_pieces(start_y, start_x, dest_y, dest_x)        

        self.logic_board[dest_y][dest_x] = self.logic_board[start_y][start_x]
        self.logic_board[dest_y][dest_x].update_pos((dest_x, dest_y))
        self.logic_board[start_y][start_x] = Piece("00", (start_x, start_y))

        self.logic_board[dest_y][dest_x].did_move()

    def wrong_figure_picked(self, dest_x, dest_y, attacked):
        if not attacked.can_be_attacked():
            return False
        if (dest_x == self.x and dest_y == self.y):
            return False
        if attacked.color() == self.move_board[self.y][self.x].color():
            return False
        return True

    def update_king_pos(self, x, y):
        self.color_pieces[f"{self.turn}K"] = (y, x)
    
    def king_logic(self, x, y):
        if self.logic_board[y][x].figure() != "K":
            return
        self.update_king_pos(x, y)
        self.roszada(x)
    
    def roszada(self, x, y):
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
        self.graphic_board.kill_piece(x, start_y)
        self.logic_board[start_y][x] = Piece("00", (x, start_y))
        
    def pawn_logic(self, start_y, start_x, x, y):
        if self.logic_board[y][x].figure() != "P":
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
        dest_x, dest_y = get_cords()
        self.move_board = self.logic_board[self.y][self.x].all_available(deepcopy(self.logic_board), self.enemy, self.color_pieces, False)
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
            self.graphic_board.kill_piece(dest_x, dest_y)
            self.graphic_board.add_piece(f"{self.turn}{piece_type}", dest_x, dest_y)

            piece = IMPORT_PIECES.get(piece_type)(f"{self.turn}{piece_type}", (dest_x, dest_y))
            self.color_pieces[self.turn].append(piece)
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
        self.screen.blit(self.graphic_board.get_board(), (0,0))
        self.graphic_board.get_pieces().draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            self.graphic_board.mouse_move(deepcopy(self.logic_board), self.enemy, self.color_pieces, self.screen, self.turn)
        else:
            if self.graphic_board.copy != 0:
                self.x, self.y = self.graphic_board.get_x_y()
                self.check_valid_move()
                self.graphic_board.copy = 0
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    while game.game_active:
        game.run()