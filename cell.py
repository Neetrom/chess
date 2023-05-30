class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.no_pieces_here = True
        self.under_attacked = False
    
    def place_piece(self):
        self.no_pieces_here = False
    
    def empty(self):
        return self.no_pieces_here
    
    def remove_piece(self):
        self.no_pieces_here = True
    
    def attacked(self):
        self.attacked = True
    
    def stop_attacking(self):
        self.attacked = False
    
    def is_attacked(self):
        return self.under_attacked