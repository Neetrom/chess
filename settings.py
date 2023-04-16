BOARD_TILES = [[0,1,0,1,0,1,0,1],
               [1,0,1,0,1,0,1,0],
               [0,1,0,1,0,1,0,1],
               [1,0,1,0,1,0,1,0],
               [0,1,0,1,0,1,0,1],
               [1,0,1,0,1,0,1,0],
               [0,1,0,1,0,1,0,1],
               [1,0,1,0,1,0,1,0]]

PIECES = [["BR", "BH", "BB", "BQ", "BK", "BB", "BH", "BR"],
          ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
          ["00", "00", "00", "00", "00", "00", "00", "00"],
          ["00", "00", "00", "00", "00", "00", "00", "00"],
          ["00", "00", "00", "00", "00", "00", "00", "00"],
          ["00", "00", "00", "00", "00", "00", "00", "00"],
          ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
          ["WR", "WH", "WB", "WQ", "WK", "WB", "WH", "WR"]]

BOARD_SIZE = (800,800)
TILE_SIZE = BOARD_SIZE[0]//8

ROOK_DIR = [[1, 0], [-1, 0], [0, 1], [0, -1]]
BISH_DIR = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

QUEEN_DIR = [[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]]

HORSE_DIR = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [-2, 1], [2, -1], [-2, -1]]

NO_DIR = []

PROMO = ["Q", "B", "H", "R"]