import pygame, sys
from settings import *
from copy import deepcopy, copy
from graphic_interface import Graphic_Interface
from logic_board import Logic_Board
from promo_menu import Promo_Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")

        self.logic_board = Logic_Board()
        self.graphic_interface = Graphic_Interface(self.logic_board.get_board())
        self.promo_menu = Promo_Menu()
        self.x = 0
        self.y = 0
        self.move_board = []
        
        self.turn = "W"
        self.enemy = "B"

        self.won = "None"

        self.game_active = True
        self.promo_menu_bool = False
    

    def check_valid_move(self):
        dest_x, dest_y = get_cords()
        
        if self.logic_board.make_a_move_if_valid(self.x, self.y, dest_x, dest_y, self.turn, self.enemy):
            return

        self.change_turn()
        self.graphic_interface.update_board(self.logic_board.get_board())

    def change_turn(self):
        if self.turn == "W":
            self.turn = "B"
            self.enemy = "W"
        else:
            self.turn = "W"
            self.enemy = "B"
        
    def run(self):
        self.graphic_interface.draw_board(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            self.graphic_interface.mouse_move(deepcopy(self.logic_board.get_board()), self.enemy, self.logic_board.get_color_pieces(), self.screen, self.turn)
        else:
            if self.graphic_interface.figure_picked():
                self.x, self.y = self.graphic_interface.get_x_y()
                self.check_valid_move()
                self.graphic_interface.let_go_of_a_piece()
        pygame.display.update()

