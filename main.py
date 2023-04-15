import pygame, sys
from settings import *
from pieces import Piece, Rook, Queen, Pawn, Bishop, King, Horse
from copy import deepcopy

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
                

        self.pieces = PIECES
        
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
        for row_index, row in enumerate(self.pieces):
            for col_index, val in enumerate(row):
                if val != 0:
                    piece = IMPORT_PIECES.get(val[1])(val, (col_index, row_index))
                    self.graphics_piece_board[row_index][col_index] = piece
                    self.piece_group.add(piece)
                    self.color_pieces[val[0]].append(piece)
                    if val[1] == "K":
                        self.color_pieces[val] = (col_index, row_index)
    
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
                self.move_board = self.graphics_piece_board[self.y][self.x].all_available(deepcopy(self.pieces), self.enemy, self.color_pieces, False)
                if self.pieces[self.y][self.x][1] == "K":
                    self.roszada()
                elif self.pieces[self.y][self.x][1] == "P":
                    self.en_passa()
        if self.pieces[self.y][self.x] != 0:
            for row_index, row in enumerate(self.move_board):
                for col_index, val in enumerate(row):
                    if val == 0:
                        continue
                    if val[0] == "X":
                        pygame.draw.circle(self.screen, (130, 237, 92),(col_index*TILE_SIZE+50, row_index*TILE_SIZE+50), 20)
            self.copy = pygame.image.load(f"graphics/{self.pieces[self.y][self.x]}.png").convert_alpha()
            pygame.Surface.set_alpha(self.copy, 100)
            copy_rect = self.copy.get_rect(center = pygame.mouse.get_pos())
            self.screen.blit(self.copy, copy_rect)
    
    def en_passa(self):
        if self.turn == "W":
            self.direction = -1
        else:
            self.direction = 1
        for offset in [-1, 1]:
            if self.x+offset > 7 or self.x+offset < 1:
                continue
            if self.graphics_piece_board[self.y][self.x+offset] != 0:
                if self.graphics_piece_board[self.y][self.x+offset].type[0] !=  self.graphics_piece_board[self.y][self.x].type[0]:
                    if self.graphics_piece_board[self.y][self.x+offset].type[1] == "P":
                        if self.graphics_piece_board[self.y][self.x+offset].en_pass:
                            self.move_board[self.y+self.direction][self.x+offset] = "XP"
    
    def roszada(self):
        if self.graphics_piece_board[self.y][self.x].did_it_move():
            return
        if self.graphics_piece_board[self.y][self.x+3] != 0:
            if self.graphics_piece_board[self.y][self.x+3].type[1] == "R":
                if not self.graphics_piece_board[self.y][self.x+3].moved and self.pieces[self.y][self.x+1] == 0 and self.pieces[self.y][self.x+2] == 0:
                    self.move_board[self.y][self.x+2] = "XO"

        if self.graphics_piece_board[self.y][self.x-4] != 0:
            if self.graphics_piece_board[self.y][self.x-4].type[1] == "R":     
                if self.pieces[self.y][self.x-3] == 0 and self.pieces[self.y][self.x-2] == 0 and not self.graphics_piece_board[self.y][self.x-4].moved:
                    self.move_board[self.y][self.x-2] = "XD"
    
    def move_pieces(self, start_y, start_x, dest_y, dest_x):
        self.graphics_piece_board[dest_y][dest_x] = self.graphics_piece_board[start_y][start_x]
        self.graphics_piece_board[dest_y][dest_x].update_pos((dest_x, dest_y))
        self.graphics_piece_board[start_y][start_x] = 0

        if self.pieces[dest_y][dest_x] != 0 and self.pieces[dest_y][dest_x][1] == "K":
            self.game_active = False
            self.won = self.pieces[start_y][start_x][0]

        self.pieces[dest_y][dest_x] = self.pieces[start_y][start_x]
        self.pieces[start_y][start_x] = 0

        self.graphics_piece_board[dest_y][dest_x].did_move()

    def check_valid_move(self):
        dest_x, dest_y = pygame.mouse.get_pos()
        dest_x = int((dest_x-dest_x%TILE_SIZE)/TILE_SIZE)
        dest_y = int((dest_y-dest_y%TILE_SIZE)/TILE_SIZE)
        attacked = self.move_board[dest_y][dest_x]
        swap = 0
        if attacked == 0:
            return
        if (dest_x == self.x and dest_y == self.y) or attacked[0] == self.move_board[self.y][self.x][0]:
            return
        if self.prev != 0:
            self.prev.ne()
            self.prev = 0
        if attacked[0] == "X":
            if self.graphics_piece_board[dest_y][dest_x] != 0:
                pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y][dest_x])
        
        self.move_pieces(self.y, self.x, dest_y, dest_x)

        if self.graphics_piece_board[dest_y][dest_x].type[1] == "K":
            self.color_pieces[f"{self.turn}K"] = (dest_x, dest_y)


        if attacked == "XO" or attacked == "XD":
            if attacked[1] == "O":
                swap = -1
                flip = 1
            else:
                swap = 1
                flip = -2
            
            self.move_pieces(dest_y, dest_x+flip, dest_y, dest_x+swap)
        
        if attacked == "XP":
            pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y-self.direction][dest_x])
            self.graphics_piece_board[dest_y-self.direction][dest_x] = 0
            self.pieces[dest_y-self.direction][dest_x] = 0
        
        if attacked == "XL":
            self.graphics_piece_board[dest_y][dest_x].en()
            self.prev = self.graphics_piece_board[dest_y][dest_x]

        if (self.graphics_piece_board[dest_y][dest_x].type[1] == "P") and (dest_y == 7 or dest_y == 0):
            self.promo_menu_bool = True
            while self.promo_menu_bool:
                self.handle_promo(dest_x, dest_y)

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
        self.screen.blit(self.promo_menu, self.promo_menu_rect)


    def pick_promo(self, dest_x, dest_y):
        if not pygame.mouse.get_pressed()[0]:
            return
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.promo_menu_rect, mouse_pos):
            x = (mouse_pos[0] - self.promo_menu_rect.topleft[0])//TILE_SIZE
            funny_dict = {0: "Q", 1: "B", 2: "H", 3: "R"}
            piece_type = funny_dict[x]
            
            self.color_pieces[self.turn].remove(self.graphics_piece_board[dest_y][dest_x])
            self.piece_group.remove(self.graphics_piece_board[dest_y][dest_x])
            pygame.sprite.Sprite.kill(self.graphics_piece_board[dest_y][dest_x])
            self.graphics_piece_board[dest_y][dest_x] = 0

            piece = IMPORT_PIECES.get(piece_type)(f"{self.turn}{piece_type}", (dest_x, dest_y))
            self.graphics_piece_board[dest_y][dest_x] = piece
            self.piece_group.add(piece)
            self.color_pieces[self.turn].append(piece)

            self.promo_menu_bool = False

    def handle_promo(self, dest_x, dest_y):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.gen_promo_menu()
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