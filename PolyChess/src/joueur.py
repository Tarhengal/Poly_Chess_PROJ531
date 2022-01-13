class Joueur:
    def __init__(self, couleur = None):
        self.couleur = couleur

    def set_couleur(self, couleur):
        self.couleur = couleur
        
    def get_couleur(self):
        return self.couleur