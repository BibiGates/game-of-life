from random import randint

class Jeu:
    """Représente une grille du jeu de la vie.
    """

    def __init__(self, tx, ty):
        """Jeu, int, int -> Jeu
        Initialise les attributs de la classe.abs"""
        
        self.__tx = tx
        self.__ty = ty

        self.__grille = []
        for i in range(tx):
            ligne = []
            for j in range(ty):
                ligne.append(False)
            self.__grille.append(ligne)

        self.__nb_viv = 0
        self.__gen = 0
        self.__stable = True
    
    def nb_viv(self):
        """Jeu -> int
        Renvoie le nombre de cellules vivantes."""

        return self.__nb_viv

    def tx(self):
        """Jeu -> int
        Renvoie le nombre de lignes."""

        return self.__tx

    def ty(self):
        """Jeu -> int
        Renvoie le nombre de colonnes."""

        return self.__ty

    def gen(self):
        """Jeu -> int
        Renvoie le numéro de la génération actuelle."""

        return self.__gen

    def resetGen(self):
        """Jeu (modif), int -> None
        """

        self.__gen = 0

    def etat(self, x, y):
        """Jeu, int, int -> bool
        Indique si la cellule en (x, y) est vivante ou non."""

        return self.__grille[x][y]
    
    def stable(self):
        """Jeu -> bool
        indique si la grille est stable."""

        return self.__stable

    def changeEtat(self, x, y, val):
        """Jeu (modif), bool -> None
        Attribut l'état donné à la cellule."""

        self.__grille[x][y] = val
        if val == True:
            self.__nb_viv += 1
        else:
            self.__nb_viv -= 1

    def afficherGrille(self):
        """Jeu -> None
        Affiche la grille."""

        ch = "\t"
        for i in range(self.__ty):
            ch += " " + str(i) + " "
        ch += "\n" * 3

        for i in range(self.__tx):
            ch += str(i) + "\t"
            for j in range(self.__ty):
                if self.__grille[i][j]:
                    ch += " * "
                else:
                    ch += " - "
            ch += "\n"

        print(ch)

    def coords_valides(self, x, y):
        """Jeu, int, int -> bool
        Indique si (x, y) sont des coordonnées valides."""

        return 0 <= x < self.__tx and 0 <= y < self.__ty

    def getAdj(self, x, y):
        """Jeu, int, int -> List((int, int))
        Renvoie la liste des coordonnées des cellules vivantes voisines."""

        assert self.coords_valides(x, y)

        cpt = 0

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.coords_valides(x + i, y + j) and self.__grille[x + i][y + j]:
                    cpt += 1

        if self.__grille[x][y]:
            return cpt - 1

        return cpt

    def etapeSuivante(self):
        """Jeu (modif) -> None
        Passe à la génération suivante."""

        self.__stable = True

        actuel = self.__grille
        courant = []

        for x in range(self.__tx):
            ligne = []
            for y in range(self.__ty):
                adj = self.getAdj(x, y)
                if actuel[x][y]:
                    if adj < 2 or adj > 3:
                        ligne += [False]
                        self.__nb_viv -= 1
                        self.__stable = False
                    else:
                        ligne += [True]
                else:
                    if adj == 3:
                        ligne += [True]
                        self.__nb_viv += 1
                        self.__stable = False
                    else:
                        ligne += [False]
            courant.append(ligne)

        self.__grille = courant
        self.__gen += 1

    def coords_non_vivants(self):
        """Jeu -> list((int, int))
        Renvoie la liste des coordonnées des cellules mortes."""

        coords = []

        for i in range(self.__tx):
            for j in range(self.__ty):
                if not self.__grille[i][j]:
                    coords.append((i, j))

        return coords

    def placeVCelsRandom(self, n):
        """Jeu (modif), int -> None
        Place n cellules vivantes à des coordonnées aléatoires."""

        coords = self.coords_non_vivants()
        for i in range(n):
            ind = randint(0, len(coords) - 1)
            c = coords[ind]
            self.changeEtat(c[0], c[1], True)
            del coords[ind]

        self.__nb_viv = n

# Fin de classe Jeu

def modele_alea():
    """None -> bool
    Indique si l'utilisateur souhaite un modèle aléatoire."""

    entree = ""
    while len(entree) != 1 or entree not in "yYnN":
        entree = input("Voulez-vous un modèle généré aléatoirement ? [y/n] : ")

    return entree in "Yy"

def est_entier(ch):
    """str -> bool
    Indique si la chaine est convertible en entier."""

    if (ch == ''):
        return False

    for c in ch:
        if c not in "0123456789":
            return False

    return True

def demande_nombre(mi, ma):
    """int, int -> int
    Demande à l'utilisateur d'entrer un entier compris entre deux valeurs incluses."""

    entree = mi - 1
    while not mi <= entree <= ma:
        entree = int(input())

    return entree

def main():
    """None -> None
    Fonction principale."""

    print("Entrez le nombre de lignes : ")
    m = demande_nombre(1, 100)
    print("Entrez le nombre de colonnes : ")
    n = demande_nombre(1, 100)

    # Demande si aléatoire ou non
    alea = modele_alea()

    jeu = Jeu(m, n)

    if alea:
        print("Entrez le nombre de cellules : ")
        nbCell = demande_nombre(0, m * n)
        jeu.placeVCelsRandom(nbCell)

        print("\n\t===  Grille de départ  ===\n")
        jeu.afficherGrille()
        input("Appuyez sur ENTRER.\n")

        continuer = True
        while jeu.nb_viv() > 0 and continuer:
            jeu.etapeSuivante()
            jeu.afficherGrille()
            
            continuer = input("Prochaine génération [y]") == "y"

if __name__ == "__main__":
    main()
