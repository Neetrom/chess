from logic.game import Game

if __name__ == "__main__":
    game = Game()
    while game.game_active:
        game.run()