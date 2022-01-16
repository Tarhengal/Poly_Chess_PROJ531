
class Joueur:
    """
    Classe représentant un joueur avec sa couleur

    Attributes
    ----------
    couleur : chess.COLOR
    """
    def __init__(self, couleur = None):
        self.couleur = couleur

    def set_couleur(self, couleur):
        """
        Setter de couleur

        """
        self.couleur = couleur
        
    def get_couleur(self):
        """
        Getter de couleur

        """
        return self.couleur