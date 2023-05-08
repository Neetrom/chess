import pygame
from settings import TILE_SIZE, PROMO, BOARD_SIZE
import sys

class Promo_Menu:
    def __init__(self):
        self.black_menu, self.black_menu_reck = self.gen_promo_menu("B")
        self.white_menu, self.white_menu_rect = self.gen_promo_menu("W")
        self.funny_dict = {0: "Q", 1: "B", 2: "H", 3: "R", 4: "R"}
        self.open = False

    def gen_promo_menu(self, team):
        promo_menu = pygame.surface.Surface((TILE_SIZE*4, TILE_SIZE))
        promo_menu.fill((140, 232, 130))
        separator = pygame.surface.Surface((4, TILE_SIZE))
        separator.fill("black")
        
        i = 0
        for piece in PROMO:
            image = pygame.image.load(f"graphics/{team}{piece}.png")
            image_rect = image.get_rect(topleft=(i, 0))
            promo_menu.blit(image, image_rect)
            promo_menu.blit(separator, (i,0))
            i = i+TILE_SIZE

        promo_menu.blit(separator, (i-5,0))
        border = pygame.transform.scale(separator, (TILE_SIZE*4, 4))
        promo_menu.blit(border, (0,0))
        promo_menu.blit(border, (0,TILE_SIZE-5))

        promo_menu = pygame.transform.rotozoom(promo_menu, 0, 1.1)
        promo_menu_rect = promo_menu.get_rect(center=(BOARD_SIZE[0]/2, BOARD_SIZE[1]/2))
        return promo_menu, promo_menu_rect

    def get_menu(self, team):
        if team == "W":
            return self.white_menu
        else:
            return self.black_menu
    
    def get_menu_rect(self, team):
        if team == "W":
            return self.white_menu_rect
        else:
            return self.black_menu_reck
        
    
    def pick_promo(self, dest_x, dest_y, logic_board, team):
        if not pygame.mouse.get_pressed()[0]:
            return
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.get_menu_rect(team), mouse_pos):
            x = (mouse_pos[0] - self.get_menu_rect(team).topleft[0])//TILE_SIZE
            piece_type = self.funny_dict[x]
            
            logic_board.kill_piece(dest_x, dest_y, team)
            logic_board.add_piece(f"{team}{piece_type}", dest_x, dest_y)

            self.close()

    def handle_promo(self, dest_x, dest_y, logic_board, team, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(self.get_menu(team), self.get_menu_rect(team))
        self.pick_promo(dest_x, dest_y, logic_board, team)
        pygame.display.update()

    def is_on(self):
        return self.open
    
    def open_menu(self):
        self.open = True
    
    def close(self):
        self.open = False

    def open_promo(self, x, y, logic_board, turn, screen):
        self.open_menu()
        while self.is_on():
            self.handle_promo(x, y, logic_board, turn, screen)