import chess

class Engine:
    def __init__(self):
        self.num_positions = 0

    def search(self, board, depth):

        if depth == 0:
            return 1

        for move in board.legal_moves:
            board.push(move)
            self.search(board, depth - 1)

            #update num_positions
            self.num_positions += 1
            if depth > 1:
                self.num_positions -= 1
            board.pop()

    def evaluate(self, board):
        pass