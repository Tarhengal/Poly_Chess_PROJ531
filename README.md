# Poly_Chess_PROJ531

PolyChess est un moteur d'échecs développé par les étudiants d'IDU de Polytech Annecy. Il permet de joueur aux échecs en ligne de dans avec un affichage graphique dans une fenêtre ipython (avec l'IDE Spyder ou dans un jupyter notebook) contre un autre joueur ou bien contre notre moteur d'échecs personnalisé.

# Features

- Affichage graphique
- Mode JcJ
    - Choix couleur
- Mode vs IA, sont pris en compte :
    - Avantage matériel
    - Pions passés
    - Pions doublés
    - Pions isolés
    - Pions bloqués
    - Tables de positions de pièces
    - Mobilité
- Documentation

# Installation 
Avec git, dans le repertoire de votre choix : 

```
git clone https://github.com/Tarhengal/Poly_Chess_PROJ531.git
```

puis installer les modules nécessaires : 

```
pip install IPython
``` 

```
pip install chess
``` 


# Utilisation

Ouvrir le projet avec spyder ou un jupyter notebook pour le bon fonctionnement de l'affichage graphique.

L'organisations du projet est la suivante :
- **data** : données nécessaires au fonctionnement du moteur (bibliothèque d'ouverture)
- **docs** : documentation au format html
- **src** : code source
- **tests** : fichiers de tests

Pour lancer une partie, éxécuter `src/main.py`.

# Glossaire

Quelques termes du sujet qui se rapportent à la programmation de moteur d'échecs :

#### **Bibliothèque d'ouverture** :
Document contenant un grand nombre de suites de coups et de réponses possibles réparties en ouvertures.

#### **Fonction d'évaluation** :
Fonction permettant d'associer un score à une position de l'échéquier celon des critères à determiner.

#### **Negamax** :
Implémentation simplifiée de l'agorithme MinMax

#### **AlphaBeta** :
Algorithme d'optimisation de parcours d'arbre de recherche 

#### **FEN** : 
format de notation d'un échéquier sous forme d'une string

#### **SAN** :
notation algébrique d'un coup

#### **UCI** : 
notation d'un coup sous la forme case de départ -> case d'arrivée (e.g : a2a3)



