import chess
import time

from game import Game
from engine import Engine
import math

if __name__ == "__main__":
    #rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8 
    game = Game("2B2n2/6n1/1K1p1PP1/2Pp2p1/3P2R1/pp6/rk6/8 w - - 0 1")
    engine = Engine()
    #engine.search(game.board, 1)
    # print("passé : " + str(engine.get_passed_pawns(game.board, chess.BLACK)))
    # print("bloqué : " + str(engine.get_blocked_pawns(game.board, chess.BLACK)))
    # print("isolés : " + str(engine.get_isolated_pawns(game.board, chess.BLACK)))
    # print("doublés : " + str(engine.get_doubled_pawns(game.board, chess.BLACK)))
    #print(engine.evaluate(game.board))
    start_time = time.time()
    results = engine.select_move(game.board, 4)
    #results = engine.search_simplified(game.board, 2)
    print("Best evaluation :")
    print(results)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(engine.num_positions)