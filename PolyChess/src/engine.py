import chess
import chess.polyglot
import math
import random

class Engine:
    """
    Moteur de jeu

    Attributes
    ----------
    num_positions : int
        nombre de positions évaluées
    """
        
    def __init__(self):
        self.num_positions = 0

    #TO DO QUIESCENCE

    def select_move(self, board, depth):
        """
        A partir du board actuel, effectue une recherche du meilleur coup

        Parameters:
        -----------
        board : chess.Board
            le board actuel
        depth : int
            profondeur de recherche en ply

        Returns:
        --------
        best_move : str
            Le meilleur coup trouvé au format UCI

        """
        best_move = chess.Move.null()
        best_eval = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in board.legal_moves:
            board.push(move)
            evaluation = -self.alphaBeta(board, -beta, -alpha, depth-1)
            board.pop()
            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
            if(evaluation > alpha):
                alpha = best_eval
        return best_move

    def alphaBeta(self, board, alpha, beta, depth):
        """
        A partir du board actuel, évalue les différentes positions possibles
        pour la profondeur donnée à l'aide de l'algorithme alpha beta pruning
        et negamax.

        Parameters:
        -----------
        board : chess.Board
            le board actuel
        alpha : int
            doit être initialisé à - l'infini
        beta : int
            doit être initialisé à + l'infini
        depth : int
            profondeur de recherche en ply

        Returns:
        --------
        alpha : int
            La meilleure évalutation

        """
        if depth == 0:
            return self.evaluate(board)

        if board.legal_moves.count() == 0:
            if board.is_checkmate():
                return - math.inf
            return 0

        for move in board.legal_moves:
            board.push(move)
            evaluation = - self.alphaBeta(board, -beta, -alpha, depth - 1)
            board.pop()
            if evaluation >= beta:
                return beta
            if evaluation > alpha:
                alpha = evaluation
            #update num_positions
            self.num_positions += 1
            if depth > 1:
                self.num_positions -= 1
            
        return alpha 

    def search_simplified(self, board, depth):
        """
        A partir du board actuel, évalue les différentes positions possibles
        pour la profondeur donnée. N'est pas optimisée.

        Parameters:
        -----------
        board : chess.Board
            le board actuel
        depth : int
            profondeur de recherche en ply

        Returns:
        --------
        best_move : str
            Le meilleur coup trouvé au format UCI

        """
        if depth == 0:
            return self.evaluate(board)
        if board.legal_moves.count() == 0:
            if board.is_checkmate():
                return - math.inf
            return 0
        best_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            evaluation = - self.search_simplified(board, depth - 1)
            if evaluation > best_eval:
                best_eval = evaluation
            #update num_positions
            self.num_positions += 1
            if depth > 1:
                self.num_positions -= 1
            board.pop()
        return best_eval 

    def evaluate(self, board):
        """
        Attribue un score à une position en fonction
        de différents facteurs.

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
      
        Returns:
        --------
        score : float
            Le score de la position

        """
        
        malus_weight = 0.5
        mobility_weight = 0.1
        colour = board.turn
        
        #TO DO : Mobility weight, pion passé
        score = self.get_material_score(board) \
            - malus_weight * self.get_isolated_pawns(board, colour) \
            - malus_weight * self.get_doubled_pawns(board, colour)  \
            - malus_weight * self.get_passed_pawns(board, colour)   \
            +  mobility_weight * self.get_mobility_score(board)     \
            + 0.5 * self.get_position_score(board)
       
        return score

        
    def get_material_score(self, board):
        """
        Attribue un score à une position en fonction
        du nombre de pièces.

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
      
        Returns:
        --------
        materiel_score : float
            Le score matériel de la position

        """
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        wk = len(board.pieces(chess.KING, chess.WHITE))
        bk = len(board.pieces(chess.KING, chess.BLACK))

        king_wt = 20000
        queen_wt = 900
        rook_wt = 500
        knight_wt = 330
        bishop_wt = 320
        pawn_wt = 100

        materiel_score = 0

        if board.turn == chess.WHITE:
            materiel_score = king_wt    * ( wk - bk )  \
                        + queen_wt  * ( wq - bq )  \
                        + rook_wt   * ( wr - br )  \
                        + knight_wt * ( wn - bn )  \
                        + bishop_wt * ( wb - bb )  \
                        + pawn_wt   * ( wp - bp )
        else:
            materiel_score = king_wt    * ( bk - wk )  \
                        + queen_wt  * ( bq - wq )  \
                        + rook_wt   * ( br - wr )  \
                        + knight_wt * ( bn - wn )  \
                        + bishop_wt * ( bb - wb )  \
                        + pawn_wt   * ( bp - wp )

          

        return materiel_score

    def get_position_score(self, board):
        """
        Attribue un score à une position en fonction
        de la position des pièces.

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
      
        Returns:
        --------
        position_score : float
            Le score de la position

        """

        pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        knights_table = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        bishops_table = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        rooks_table = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        queens_table = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        kings_table = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

        pawnsq = sum([pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-pawn_table[chess.square_mirror(i)]
                            for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knights_table[chess.square_mirror(i)]
                                for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishops_table[chess.square_mirror(i)]
                                for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rooks_table[chess.square_mirror(i)]
                            for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queens_table[chess.square_mirror(i)]
                                for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kings_table[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kings_table[chess.square_mirror(i)]
                            for i in board.pieces(chess.KING, chess.BLACK)])

        position_score = pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        if board.turn:
            return position_score
        return - position_score

    
    def get_doubled_pawns(self, board, colour):
        """
        Retourne le nombre de pions doublés

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
        colour :
            Le coté pour lequel on veut connaitre les pions
      
        Returns:
        --------
        num_doubled_pawns : int
            nombre de pions doublés

        """
        files = []
        for file_index in range(8):
            files.append( [] )
            for rank_index in range(8):
                files[file_index].append(chess.square(file_index, rank_index)) 

        num_doubled_pawns = 0

        for f in files:
            file_pawns = 0
            for square in f:
                if board.piece_type_at(square) == chess.PAWN and board.color_at(square) == colour:
                    file_pawns += 1
            if file_pawns >= 2:
                num_doubled_pawns += (file_pawns - 1)

        return num_doubled_pawns

    def get_isolated_pawns(self, board, colour):
        """
        Retourne le nombre de pions isolés

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
        colour :
            Le coté pour lequel on veut connaitre les pions
      
        Returns:
        --------
        num_isolated_pawns : int
            nombre de pions isolés

        """
        files = []
        for file_index in range(8):
            files.append( [] )
            for rank_index in range(8):
                files[file_index].append(chess.square(file_index, rank_index))

        num_isolated_pawns = 0
        has_pawns = []

        for i in range(len(files)):
            has_pawns.append(False)
            for square in files[i]:
                if board.piece_type_at(square) == chess.PAWN and board.color_at(square) == colour:
                    has_pawns[i] = True
        
        for i in range(len(has_pawns)):
            if i > 0 and i < 7:
                if has_pawns[i - 1] == False and has_pawns[i + 1] == False:
                    num_isolated_pawns += 1
            elif i == 0 and has_pawns[i + 1] == False:
                    num_isolated_pawns += 1
            elif i == 7 and has_pawns[i - 1] == False:
                    num_isolated_pawns += 1

        return num_isolated_pawns

    def get_blocked_pawns(self, board, colour):
        """
        Retourne le nombre de pions bloqués

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
        colour :
            Le coté pour lequel on veut connaitre les pions
      
        Returns:
        --------
        num_blocked_pawns : int
            nombre de pions bloqués

        """
        num_blocked_pawns = 0

        for file_index in range(8):
            for rank_index in range(8):
                square = chess.square(file_index, rank_index)
                if board.piece_type_at(square) == chess.PAWN and board.color_at(square) == colour:
                    targets = []
                    if colour == chess.WHITE:
                        targets.append(square + 8)
                    else:
                        targets.append(square - 8)
                    if chess.square_file(square) > 0:
                        if colour == chess.WHITE:
                            targets.append(square + 7)
                        else:
                            targets.append(square - 9)
                    if chess.square_file(square) < 7:
                        if colour == chess.WHITE:
                            targets.append(square + 9)
                        else:
                            targets.append(square - 7)
                    is_blocked = True
                    for target in targets:
                        if target <= 63:
                            promotions = ["q", "r", "b", "n", ""]
                            for p in promotions: 
                                move = chess.square_name(square) + chess.square_name(target) + p
                                if len(move) <= 5:
                                    if chess.Move.from_uci(move) in board.legal_moves:
                                        is_blocked = False
                    if is_blocked:
                        num_blocked_pawns += 1

        return num_blocked_pawns

    def get_passed_pawns(self, board, colour):
        """
        Retourne le nombre de pions passés

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
        colour :
            Le coté pour lequel on veut connaitre les pions
      
        Returns:
        --------
        num_passed_pawns : int
            nombre de pions passés

        """
        files = []
        for file_index in range(8):
            files.append( [] )
            for rank_index in range(8):
                files[file_index].append(chess.square(file_index, rank_index))

        num_passed_pawns = 0

        for file_index in range(8):
            for square in files[file_index]:
                if board.piece_type_at(square) == chess.PAWN and board.color_at(square) == colour:
                    is_passed = True
                    if file_index > 0:
                        if not self.check_passed_pawns(board, square, file_index - 1, files, colour):
                            is_passed = False
                    if file_index < 7: 
                        if not self.check_passed_pawns(board, square, file_index + 1, files, colour):
                            is_passed = False
                    if not self.check_passed_pawns(board, square, file_index, files, colour):
                        is_passed = False
                    if is_passed:
                        num_passed_pawns += 1
        
        return num_passed_pawns

                    

    def check_passed_pawns(self,board, square, file_index, files, colour):
        is_passed = True
        for sqr in files[file_index]:
            if board.piece_type_at(sqr) == chess.PAWN and board.color_at(sqr) == (not colour):
                #print(f"{chess.square_rank(square)} / {chess.square_rank(sqr)}")
                if colour == chess.WHITE and chess.square_rank(sqr) > chess.square_rank(square):
                    is_passed = False
                elif colour == chess.BLACK and chess.square_rank(sqr) < chess.square_rank(square):
                    is_passed = False
        return is_passed
            
        
    def get_mobility_score(self, board):
        """
        Retourne le score de mobilité d'une position (nombre de coups
        possibles )

        Parameters:
        -----------
        board : chess.Board
            la position à évaluer
      
        Returns:
        --------
        mobility_score : int
            score de mobilité

        """
        num_legal_moves = board.legal_moves.count()
        board_copy = board.copy()
        board_copy.turn = not board_copy.turn
        num_legal_moves_opp = board_copy.legal_moves.count()
        
        return num_legal_moves - num_legal_moves_opp
    
    
    def play(self, board):
        """
        Joue les coups d'une bibliothèque d'ouverture pendant le début
        de partie (i.e : jusqu'à la fin de l'ouverture ou coup incohérent
        de l'adversaire), puis joue le meilleur coup trouvé.

        Parameters:
        -----------
        board : chess.Board
            le board actuel

        """
               
        with chess.polyglot.open_reader('../data/performance.bin') as reader:
                           
            entries = []
            
            for entry in reader.find_all(board):
                entries.append(entry.move)
            
            
            if entries:                          
                entry = random.randint(0, len(entries) - 1)
                coup = entries[entry]
                board.push(chess.Move.from_uci(str(coup)))
            else:  
                               
                coup = self.select_move(board, 1)
                
                if coup:                                         
                    board.push(chess.Move.from_uci(str(coup)))
                     
            

                

                






        
