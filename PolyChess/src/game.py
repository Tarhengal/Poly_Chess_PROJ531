from joueur import Joueur
from random import randint

class Game:
    MODE_VS_IA = 0
    MODE_VS_JOUEUR = 1
    COULEUR_BLANC = 'BLANC'
    COULEUR_NOIR = 'NOIR' 

    def __init__(self):
        self.joueur_1 = Joueur()
        self.joueur_2 = Joueur()
        self.timer = 0
        
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
        choix = input('Limite de temps : (nombre de minutes/0) : ')
        while not choix.isnumeric():
            print('Erreur.')
            choix = input('Limite de temps : (nombre de minutes/0) : ')
        self.timer = choix

            
