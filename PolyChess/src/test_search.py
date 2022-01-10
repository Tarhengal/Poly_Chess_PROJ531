import chess

from game import Game
from engine import Engine

if __name__ == "__main__":
    game = Game("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
    engine = Engine()
    engine.search(game.board, 1)
    print(engine.num_positions)