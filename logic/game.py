import pygame, sys
from settings import *
from graphics.graphic_interface import Graphic_Interface
from logic.logic_board import Logic_Board
from graphics.promo_menu import Promo_Menu
from random import shuffle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        pygame.display.set_caption("lmao")

        self.logic_board = Logic_Board()
        self.cells = self.logic_board.get_cells()
        self.graphic_interface = Graphic_Interface(self.logic_board.get_board())
        self.promo_menu = Promo_Menu()

        self.turn = "W"
        self.enemy = "B"

        self.game_active = True
    

    def do_a_move(self, piece_picked, target):
        if self.logic_board.make_a_move_if_valid(piece_picked, target, self.turn, self.enemy):
            return

        self.change_turn()
        self.cells = self.logic_board.get_cells()
        self.graphic_interface.update_board(self.logic_board.get_board())

    def change_turn(self):
        if self.turn == "W":
            self.turn = "B"
            self.enemy = "W"
        else:
            self.turn = "W"
            self.enemy = "B"
        
    def player_turn(self):
        if pygame.mouse.get_pressed()[0]:
            self.graphic_interface.mouse_move(self.logic_board, self.enemy, self.screen, self.turn)
        else:
            if self.graphic_interface.figure_picked():
                start_x, start_y = self.graphic_interface.get_x_y()
                dest_x, dest_y = get_cords()

                target = self.cells[dest_y][dest_x]
                piece_picked = self.cells[start_y][start_x]

                self.do_a_move(piece_picked, target)
                self.graphic_interface.let_go_of_a_piece()

    def bot_turn(self):
        enemy_team = self.logic_board.get_color_pieces()[self.turn]
        shuffle(enemy_team)
        # generate moves for enemy team in random order
        for piece in enemy_team:
            start_x, start_y = piece.pos
            piece_picked = self.cells[start_y][start_x]
            moves = self.logic_board.generate_moves(piece_picked, self.enemy)
            # look for a tile that can be attacked
            for row in moves:
                for cell in row:
                    if cell.can_be_attacked():
                        dest_x, dest_y = cell.pos
                        target = self.cells[dest_y][dest_x]
                        self.do_a_move(piece_picked, target)

                        return
        # if there are none tiles that can be attacked, then it's game over
        self.game_active = False

    def run(self):
        self.graphic_interface.draw_board(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if self.turn == "W":
            self.player_turn()
        else:
            self.bot_turn()


        pygame.display.update()

