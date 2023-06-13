from copy import deepcopy, copy

class Piece:
    def __init__(self, piece_type, pos):
        self.pos = pos

        self.type = piece_type
        self.points = 0
        self.valid_attack = False

        self.directions = []

        self.moved = False

    def update_pos(self,pos):
        self.pos = pos

    def did_it_move(self):
        return self.moved

    def can_be_attacked(self):
        return self.valid_attack

    def attacked(self):
        self.valid_attack = True
    
    def all_available(self, board, enemy, piece_dict, rek):
        if not rek:
            b_copy = deepcopy(board)
        for direction in self.directions:
            check = [copy(self.pos[1]), copy(self.pos[0])]
            while True:
                check[0] += direction[0]
                check[1] += direction[1]
                if check[0] == 8 or check[0] == -1 or check[1] == 8 or check[1] == -1:
                    break
                attacking = board[check[0]][check[1]]
                if not attacking.is_empty():
                    if attacking.color() != self.color():
                        if not rek:
                            if not self.illegal_move(deepcopy(b_copy), enemy, piece_dict, check):
                                attacking.attacked()
                        else:
                            attacking.attacked()
                    break
                if not rek:
                    if not self.illegal_move(deepcopy(b_copy), enemy, piece_dict, check):
                        attacking.attacked()
                else:
                    attacking.attacked()
        return board
    
    def illegal_move(self, board, enemy, piece_dict, dest):
        board = self.board_after_temporary_move_of_this_piece(board, dest)
        king = piece_dict[f"{self.color()}K"]
        for piece in piece_dict[enemy]:
            if (dest[1], dest[0]) == piece.pos:
                continue
            piece.all_available(board, enemy, piece_dict, True)
            if board[king.y][king.x].can_be_attacked():
                return True
        return False

    def board_after_temporary_move_of_this_piece(self, board, destination):
        board[destination[0]][destination[1]] = copy(board[self.pos[1]][self.pos[0]])
        board[self.pos[1]][self.pos[0]] = Piece("00", (self.pos))
        return board
    
    def __str__(self):
        return f"{self.type}"

    def did_move(self):
        self.moved = True

    def is_empty(self):
        if self.full_type() == "00":
            return True
        else:
            return False
    
    def full_type(self):
        return self.type
    
    def color(self):
        return self.type[0]

    def figure(self):
        return self.type[1]
