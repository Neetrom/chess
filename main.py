import pygame, sys
from settings import *
from copy import deepcopy, copy
from graphic_board import Graphic_Board
from logic_board import Logic_Board
from promo_menu import Promo_Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")

        self.graphic_board = Graphic_Board()
        self.logic_board = Logic_Board()
        self.promo_menu = Promo_Menu()
        self.x = 0
        self.y = 0
        self.move_board = []
        
        self.turn = "W"
        self.enemy = "B"

        self.won = "None"

        self.game_active = True
        self.promo_menu_bool = False


    def move_pieces(self, start_y, start_x, dest_y, dest_x):
        if not self.logic_board.is_tile_empty(dest_x, dest_y):
            self.graphic_board.kill_piece(dest_x, dest_y)
            self.logic_board.kill_piece(dest_x, dest_y, self.enemy)

        self.graphic_board.move_pieces(start_y, start_x, dest_y, dest_x)        
        self.logic_board.move_pieces(start_y, start_x, dest_y, dest_x)

        self.logic_board.mark_piece_movement(dest_x, dest_y)

    def king_logic(self, x, y):
        if self.logic_board.get_figure_of_piece(x, y) != "K":
            return
        self.logic_board.update_king_pos(x, y, self.turn)
        self.roszada(x, y)
    
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
        self.logic_board.kill_piece(x, start_y, self.enemy)

    def pawn_logic(self, start_y, start_x, x, y):
        if self.logic_board.get_figure_of_piece(x, y) != "P":
            return
        if abs(y-start_y) == 2:
            self.logic_board.mark_en_pass(x, y)
        
        self.promo_menu.open_promo(x, y, self.logic_board, self.graphic_board, self.turn, self.enemy, self.screen)
        
        self.pass_enn(start_y, start_x, x, y)


    def check_valid_move(self):
        dest_x, dest_y = get_cords()
        self.move_board = self.graphic_board.get_moves()

        if not self.graphic_board.wrong_figure_picked(dest_x, dest_y):
            return
        
        self.logic_board.turn_off_en_pass()
        
        self.move_pieces(self.y, self.x, dest_y, dest_x)

        self.king_logic(dest_x, dest_y)

        self.pawn_logic(self.y, self.x, dest_x, dest_y)

        if self.turn == "W":
            self.turn = "B"
            self.enemy = "W"
        else:
            self.turn = "W"
            self.enemy = "B"
        

    def run(self):
        self.screen.blit(self.graphic_board.get_background(), (0,0))
        self.graphic_board.get_pieces().draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            self.graphic_board.mouse_move(deepcopy(self.logic_board.get_board()), self.enemy, self.logic_board.get_color_pieces(), self.screen, self.turn)
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