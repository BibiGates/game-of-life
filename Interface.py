import tkinter as tk
from Jeu import Jeu, est_entier

TX, TY = 30, 30 # Taille par défaut
TIME = 50
BUTWIDTH = 6

#####################################################################################################

class Modele:
    """[TKINTER] Gère l'interface d'une instance de Jeu.
    """

    def __init__(self):
        """Modele -> Modele
        Initialise l'interface et la loop du programme."""

        self.__master = tk.Tk()
        self.__master.title("Le jeu de la vie")
        self.__master.resizable(width=False, height=False)
        
        self.__jeu = Jeu(TX, TY)
        self.__time = TIME

        # UI
        fUI = tk.Frame()

        self.__lGen = tk.Label(fUI, text="GEN : 0", font=("Arial", 15))
        self.__lGen.pack()

        # Inputs
        fInputs = tk.Frame(fUI, bd=3, relief="sunken")

        self.__eNbCells = tk.Entry(fInputs, width="10", justify="center")
        self.__eNbCells.pack(pady=5)

        self.__bAlea = tk.Button(fInputs, text="Générer", width=BUTWIDTH,
                command=self.genAlea)
        self.__bAlea.pack(pady=5)

        fSep = tk.Frame(fInputs, bd=1, height=2, relief="sunken")
        fSep.pack(pady=10, fill="x")

        lLignes = tk.Label(fInputs, text="Lignes :")
        lLignes.pack()

        self.__eLignes = tk.Entry(fInputs, width=10, justify="center")
        self.__eLignes.pack()

        lLignes = tk.Label(fInputs, text="Colonnes :")
        lLignes.pack()

        self.__eColonnes = tk.Entry(fInputs, width=10, justify="center")
        self.__eColonnes.pack()

        self.__bReinit = tk.Button(fInputs, text="Modifier", width=BUTWIDTH,
                command=self.reinit)
        self.__bReinit.pack(pady=5)

        fInputs.pack(pady=5)
        # # #

        self.__lStable = tk.Label(fUI, text="N/A", padx=5, font=("Arial", 12), fg="orange")
        self.__lStable.pack(pady=15)


        # Timer
        fTimer = tk.Frame(fUI, bd=3, relief="sunken")

        self.__bSuiv = tk.Button(fTimer, text="Suivant", width=BUTWIDTH, command=self.suivant)
        self.__bSuiv.pack(pady=5)

        lTimer = tk.Label(fTimer, text="Timer :\n[5 ; 5000]")
        lTimer.pack()

        self.__eTimer = tk.Entry(fTimer, width=10, justify="center")
        self.__eTimer.pack()

        bTimer = tk.Button(fTimer, text="Changer", width=BUTWIDTH,
                command=self.changeTimer)
        bTimer.pack(pady=5)

        fTimer.pack(pady=5)
        # # #

        fUI.grid(row=1, column=0, rowspan=2)
        # # #

        # Start, Stop, Clear

        fButtons = tk.Frame(bd=2, relief="sunken")

        self.__bStart = tk.Button(fButtons, text="Start", width=BUTWIDTH,
                command=self.start)
        self.__bStart.grid(row=0, column=1, padx=5, pady=3)

        self.__bStop = tk.Button(fButtons, text="Stop", width=BUTWIDTH, state="disabled",
                command=self.stop)
        self.__bStop.grid(row=0, column=2, padx=5, pady=3)

        self.__bClear = tk.Button(fButtons, text="Clear", width=BUTWIDTH, command=self.clear)
        self.__bClear.grid(row=0, column=3, padx=5, pady=3)

        fButtons.grid(row=0, column=1, pady=5)
        # # #

        # Cases
        self.__fCases = tk.Frame(bd=3, bg="white", relief="sunken")
        self.__cases = self.createGrille(TX, TY)
        self.__fCases.grid(row=1, column=1, padx=10, pady=10)
        # # #

        self.__master.mainloop()

    def controllerClickCase(self, x, y):
        """Modele (modif), int, int -> function
        Renvoie la fonction 'clickCase' pour les coordonnées (x, y)."""

        def clickCase():
            """None -> None
            Change l'état de la cellule (x, y)."""

            color = ""
            if self.__jeu.etat(x, y) == False:
                self.__jeu.changeEtat(x, y, True)
                color = "black"
            else:
                self.__jeu.changeEtat(x, y, False)
                color = "white"
            
            self.__cases[x][y].configure(bg=color)
            
            self.reinitLabels()
            self.stopState()

        return clickCase

    def metAJour(self):
        """Modele (modif) -> None
        Met à jour l'interface."""

        for i in range(self.__jeu.tx()):
            for j in range(self.__jeu.ty()):
                if self.__jeu.etat(i, j):
                    self.__cases[i][j].configure(bg="black")
                else:
                    self.__cases[i][j].configure(bg="white")

    def clear(self):
        """Modele (modif) -> None
        Tue toutes les cellules."""

        if self.__jeu.nb_viv() != 0:
            for i in range(self.__jeu.tx()):
                for j in range(self.__jeu.ty()):
                    self.__jeu.changeEtat(i, j, False)
                    self.__cases[i][j].configure(bg="white")

            self.clearState()

    def suivant(self):
        """Modele (modif) -> None
        Passe à la génération suivante."""

        self.__jeu.etapeSuivante()
        
        if (self.__jeu.stable()):
            self.__lStable.configure(text="STABLE", fg="green")
            self.__lGen.configure(fg="green")
            self.__bSuiv.configure(state="disabled")
            self.__bReinit.configure(state="normal")
            self.__start = False

            if self.__jeu.nb_viv() != 0:
                self.__bStart.configure(state="disabled")
                self.__bStop.configure(state="disabled")
                self.__bClear.configure(state="normal")

            self.disableButtons(False)
        else:
            self.__lStable.configure(text="PAS STABLE", fg="red")
            self.__lGen.configure(text="GEN : " + str(self.__jeu.gen()), fg="red")

        self.metAJour()

        if (self.__start):
            self.__master.after(self.__time, self.suivant)

    def createGrille(self, tx, ty):
        """Modele, int, int -> list(list(Button))
        Renvoie une grille de bouttons."""

        cases = []
        for i in range(tx):
            ligne = []
            for j in range(ty):
                btn = tk.Button(self.__fCases, bg="white", relief="flat", bd=0,
                        command=self.controllerClickCase(i, j))
                btn.grid(row=i, column=j)
                ligne.append(btn)
            cases.append(ligne)
        
        return cases

    def reinit(self):
        """Modele (modif)-> None
        Change la grille du jeu avec les nouveau paramètres."""

        x, y = self.__eLignes.get(), self.__eColonnes.get()

        if est_entier(x) and est_entier(y):
            self.__fCases.destroy()
            x, y = int(x), int(y)
            self.__jeu = Jeu(x, y)

            self.__fCases = tk.Frame(bd=3, bg="white", relief="sunken")
            self.__cases = self.createGrille(x, y)
            self.__fCases.grid(row=1, column=1, padx=10, pady=10)

            self.reinitLabels()
        else:
            self.__eLignes.delete(0, "end")
            self.__eColonnes.delete(0, "end")

    def start(self):
        """Modele -> None
        Lance l'éxecution du jeu."""

        self.__start = True
        self.__bSuiv.invoke()

        if not self.__jeu.stable():
            self.startState()

    def stop(self):
        """Modele -> None
        Arrête l'éxecution du jeu."""
        
        self.__start = False
        self.stopState()
       
    def startState(self):
        """Modele (modif) -> None
        Affecte un état adapté aux boutons lorsque le jeu est en éxecution."""

        self.__bSuiv.configure(state="disabled")
        self.__bClear.configure(state="disabled")
        self.__bStart.configure(state="disabled")
        self.__bReinit.configure(state="disabled")
        self.__bStop.configure(state="normal")
        self.__bAlea.configure(state="disabled")
        self.disableButtons(True)

    def stopState(self):
        """Modele (modif) -> None
        Affecte un état adapté aux boutons lorsque le jeu n'est plus en éxecution."""

        self.__bStop.configure(state="disabled")
        self.__bSuiv.configure(state="normal")
        self.__bStart.configure(state="normal")
        self.__bClear.configure(state="normal")
        self.__bReinit.configure(state="normal")
        self.__bAlea.configure(state="normal")
        self.disableButtons(False)

    def clearState(self):
        """Modele (modif) -> None
        Affecte un état adapté aux boutons lorsque le jeu n'est plus en éxecution."""

        self.__lStable.configure(text="N/A", fg="orange")
        self.__lGen.configure(text="GEN : 0", fg="black")
        self.__bStart.configure(state="normal")
        self.__bStop.configure(state="disabled")
        self.__bSuiv.configure(state="normal")
        self.__bReinit.configure(state="normal")
        self.__bAlea.configure(state="normal")

    def reinitLabels(self):
        """Modele (modif) -> None
        Réinitialise le texte des labels."""

        self.__jeu.resetGen()
        self.__lGen.configure(text="GEN : 0", fg="black")
        self.__lStable.configure(text="N/A", fg="orange")

    def disableButtons(self, val):
        """Modele (modif), bool -> None
        Change l'état des bouttons."""

        s = "disabled"
        if (not val):
            s = "normal"

        for i in range(self.__jeu.tx()):
            for j in range(self.__jeu.ty()):
                self.__cases[i][j].configure(state=s)

    def changeTimer(self):
        """Modele -> None
        Change la valeur du timer."""

        t = self.__eTimer.get()
        if (est_entier(t) and 5 <= int(t) <= 5000):
            self.__time = int(t)
        else:
            self.__eTimer.delete(0, "end")

    def genAlea(self):
        """Modele (modif) -> None
        Génère aléatoirement un ensemble de cellules vivantes."""

        n = self.__eNbCells.get()
        if est_entier(n) and 1 <= int(n) <= (self.__jeu.tx() * self.__jeu.ty()) - self.__jeu.nb_viv():
            self.__jeu.placeVCelsRandom(int(n))
            self.metAJour()
            self.reinitLabels()
        else:
            self.__eNbCells.delete(0, "end")

#####################################################################################################

def main():
    """None -> None
    Fonction principale."""
    m = Modele()

if __name__ == "__main__":
    main()
