from joueur import Joueur
from random import randint
import chess
import sys

class Game:
    MODE_VS_IA = 0
    MODE_VS_JOUEUR = 1
    COULEUR_BLANC = chess.WHITE
    COULEUR_NOIR = chess.BLACK 

    def __init__(self, fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 4"):
        self.joueur_1 = Joueur()
        self.joueur_2 = Joueur()
        self.timer = 0 
        self.to_play = Game.COULEUR_BLANC
        self.board = chess.Board(fen)
        
    def init_config(self):
        self.choix_mode()
        self.choix_temps()
        self.choix_couleur()
        
    def choix_mode(self):
        print("============ MODE ============")
        choix = input('Choisir mode de jeu (ia/joueur) : ')
        while choix != 'ia' and choix != 'joueur':
            print('Erreur.')
            choix = input('Choisir mode de jeu (ia/joueur) : ')
        if choix == 'ia':
            self.mode = Game.MODE_VS_IA
        elif choix == 'joueur':
            self.mode = Game.MODE_VS_JOUEUR

    def choix_couleur(self):
        print("============ COULEUR ============")
        choix = input('Choisir couleur ou au hasard ? (c/h) : ')
        while choix != 'c' and choix != 'h':
            print('Erreur.')
            choix = input('Choisir couleur ou au hasard ? (c/h) : ')
        if choix == 'c':
            choix = input('Joueur 1, blanc ou noir ? (b/n) : ')
            while choix != 'b' and choix != 'n':
                print('Erreur.')
                choix = input('Joueur 1, blanc ou noir ? (b/n) : ')
            if choix == 'b':
                print("Joueur 1 -> Blanc \nJoueur 2 -> Noir")
                self.joueur_1.set_couleur(Game.COULEUR_BLANC)
                self.joueur_2.set_couleur(Game.COULEUR_NOIR)
            elif choix == 'n':
                print("Joueur 1 -> Noir \nJoueur 2 -> Blanc")
                self.joueur_1.set_couleur(Game.COULEUR_NOIR)
                self.joueur_2.set_couleur(Game.COULEUR_BLANC)
        elif choix == 'h':
            r = randint(0,1)
            if r == 0:
                print("Joueur 1 -> Blanc \nJoueur 2 -> Noir")
                self.joueur_1.set_couleur(Game.COULEUR_BLANC)
                self.joueur_2.set_couleur(Game.COULEUR_NOIR)
            else:
                print("Joueur 1 -> Noir \nJoueur 2 -> Blanc")
                self.joueur_1.set_couleur(Game.COULEUR_NOIR)
                self.joueur_2.set_couleur(Game.COULEUR_BLANC)

    def choix_temps(self):
        print("============ TEMPS ============")
        choix = input('Limite de temps : (nombre de minutes/0)  ')
        while not choix.isnumeric():
            print('Erreur.')
            choix = input('Limite de temps : (nombre de minutes/0)  ')
        self.timer = choix

            
    def play(self):
        if self.mode == Game.MODE_VS_JOUEUR:
            self.play_vs_joueur()
        elif self.mode == Game.MODE_VS_IA:
            self.play_vs_ia()

    def play_vs_ia(self):
        pass

    def play_vs_joueur(self):
        play = True
        print(self.board)
        while play:
            print(self.get_to_play())

            coup = input('Jouez un coup \n')
            while not self.is_legal(coup):
                print('Coup invalide ou illégale.')
                coup = input('Jouez un coup \n')
            
            self.board.push(chess.Move.from_uci(coup))
            print(self.board)

            self.to_play = not self.to_play
            if self.has_ended():
                print(self.get_result())
                play = False
        self.rejouer()
        
    def rejouer(self):
        choix = input('Rejouer ? (o/n) : ')
        while choix != 'o' and choix != 'n':
            print('Erreur.')
            choix = input('Rejouer ? (o/n) : ')
        if choix == 'o':
            self.init_config()
            self.play()
        else:
            sys.exit()

    def is_legal(self, coup) :
        try:
            move = chess.Move.from_uci(coup)
                    
            if move in self.board.legal_moves:
                return True
            else:
                return False
            
        except ValueError:
            return False

    def has_ended(self): 
        if self.board.outcome(claim_draw = True) != None:
            return True
        return False

    def get_result(self):
        outcome = self.board.outcome(claim_draw = True)
        if outcome.winner != None:
            if outcome.winner == Game.COULEUR_BLANC:
                return "Victoire des blancs"
            else:
                return "Victoire des noirs"
        else:
            return 'Match nul'


    def get_to_play(self):
        if self.to_play == Game.COULEUR_BLANC:
            return '\nTour des blancs'
        else:
            return "\nTour des noirs"
