import pickle
from random import randint, shuffle
from joueur import Joueur
from plateau import Plateau, Jeton, Chevalet
from tkinter import Tk, Toplevel, filedialog, NSEW, N, E, W, Frame, Label, Entry, PhotoImage, \
    Radiobutton, IntVar, StringVar, Button, messagebox
from tkinter.ttk import Combobox


class jetons_sur_plateau(Exception):
    def __init__(self, texte_action):
        messagebox.showinfo(title="Minute papillon...",
                            message="Au moins un jeton est sur le plateau, veuillez le(s) reprendre avant {}".format(
                                texte_action))


class mots_non_valides(Exception):
    def __init__(self):
        messagebox.showinfo(title="OUPSSS  Mauvais coup !",
                            message="Au moins l'un des mots formés est absent du dictionnaire.\n\nVeuillez réessayer.")


class positions_non_valides(Exception):
    def __init__(self, nombre_jeton):
        if nombre_jeton == 1:
            messagebox.showinfo(title="Faudra recommencer...",
                                message="Votre lettre est mal positionnée. ")
        else:
            messagebox.showinfo(title="Faudra recommencer...",
                                message="Vos lettres sont mal positionnées. "
                                        "Elles doivent être sur une seule ligne ou colonne et "
                                        "ne former qu'une seul mot sur cette ligne ou colonne."
                                        "Le premier mot doit couvrir l'étoile centrale.")


class Sauvegarde():
    """
    Classe comportant tout les éléments d'une partie
    pour la sauvegarder et le charger par la suite afin de reprendre une partie entammée.
    """

    def __init__(self, nb_joueurs, nb_joueurs_restants, cases, jetons_libres, joueurs, joueur_actif, mots_au_plateau,
                 langue):
        self.nb_joueurs = nb_joueurs  # ok
        self.nb_joueurs_restants = nb_joueurs_restants  # ok
        self.cases = cases  # ok
        self.jetons_libres = jetons_libres  # ok
        self.joueurs = joueurs  # ok
        self.joueur_actif = joueur_actif
        self.mots_au_plateau = mots_au_plateau  # ok
        self.langue = langue  # ok


class Scrabble(Tk):
    """
    Classe Scrabble qui implémente aussi une partie de la logique de jeu.

    Les attributs d'un scrabble sont:
    - dictionnaire: set, contient tous les mots qui peuvent être joués sur dans cette partie.
    En gros pour savoir si un mot est permis on va regarder dans le dictionnaire.
    - plateau: Plateau, un objet de la classe Plateau on y place des jetons et il nous dit le nombre de points gagnés.
    - jetons_libres: Jeton list, la liste de tous les jetons dans le sac, c'est là que chaque joueur
                    peut prendre des jetons quand il en a besoin.
    - joueurs: Joueur list,  L'ensemble des joueurs de la partie.
    - joueur_actif: Joueur, le joueur qui est entrain de jouer le tour en cours. Si aucun joueur alors None.
    """

    def __init__(self, nb_joueurs, langue):
        """ *** Vous n'avez pas à coder cette méthode ***
        Étant donnés un nombre de joueurs et une langue. Le constructeur crée une partie de scrabble.
        Pour une nouvelle partie de scrabble,
        - un nouvel objet Plateau est créé;
        - La liste des joueurs est créée et chaque joueur porte automatiquement le nom Joueur 1, Joueur 2, ...
        Joueur n où n est le nombre de joueurs;
        - Le joueur_actif est None.
        :param nb_joueurs: int, nombre de joueurs de la partie au minimun 2 au maximum 4.
        :param langue: str, FR pour la langue française, et EN pour la langue anglaise. Dépendamment de la langue,
        vous devez ouvrir, lire, charger en mémoire le fichier "dictionnaire_francais.txt" ou "dictionnaire_anglais.txt"
         ensuite il faudra ensuite extraire les mots contenus pour construire un set avec le mot clé set.
        Aussi, grâce à la langue vous devez être capable de créer tous les jetons de départ et les mettre
        dans jetons_libres.
        Pour savoir combien de jetons créés pour chaque langue vous pouvez regarder à l'adresse:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
        *** Dans notre scrabble, nous n'utiliserons pas les jetons jokers qui ne contienent aucune lettre donc ne les
         incluez pas dans les jetons libres ***
        :exception: Levez une exception avec assert si la langue n'est ni fr, FR, en, ou EN ou si nb_joueur < 2 ou > 4.
        """




        super().__init__( )

        if partie_a_charger == "":
            self.joueurs = [Joueur(("Joueur {}".format(i + 1))) for i in range(nb_joueurs)]
            self.nb_joueurs = nb_joueurs
            self.nb_joueurs_restants = self.nb_joueurs
            self.mots_au_plateau = []
            self.langue = langue

        else:
            self.donnees_de_partie = self.charger_partie(partie_a_charger)
            self.joueurs = self.donnees_de_partie.joueurs
            self.nb_joueurs = self.donnees_de_partie.nb_joueurs
            self.nb_joueurs_restants = self.donnees_de_partie.nb_joueurs_restants
            self.mots_au_plateau = self.donnees_de_partie.mots_au_plateau
            self.langue = self.donnees_de_partie.langue

        global data
        # DICTIONAIRE FRANCAIS
        if self.langue.upper() == 'FR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 15, 1), ('A', 9, 1), ('I', 8, 1), ('N', 6, 1), ('O', 6, 1),
                    ('R', 6, 1), ('S', 6, 1), ('T', 6, 1), ('U', 6, 1), ('L', 5, 1),
                    ('D', 3, 2), ('M', 3, 2), ('G', 2, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 8), ('K', 1, 10), ('W', 1, 10), ('X', 1, 10), ('Y', 1, 10),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_francais.txt'
        # DICTIONAIRE ANGLAIS
        elif self.langue.upper() == 'AN':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('N', 6, 1), ('O', 8, 1),
                    ('R', 6, 1), ('S', 4, 1), ('T', 6, 1), ('U', 4, 1), ('L', 4, 1),
                    ('D', 4, 2), ('M', 2, 3), ('G', 3, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 10), ('K', 1, 5), ('W', 2, 4), ('X', 1, 8), ('Y', 2, 4),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_anglais.txt'
        # DICTIONAIRE ESPAGNOL
        elif self.langue.upper() == 'ES':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 12, 1), ('E', 12, 1), ('O', 9, 1), ('I', 6, 1), ('S', 6, 1),
                    ('N', 5, 1), ('R', 5, 1), ('U', 5, 1), ('L', 4, 1), ('T', 4, 1),
                    ('D', 5, 2), ('G', 2, 2), ('C', 4, 3), ('B', 2, 3), ('M', 2, 3),
                    ('P', 2, 3), ('H', 2, 4), ('F', 1, 4), ('V', 1, 4), ('Y', 1, 4),
                    ('CH', 1, 5), ('Q', 1, 5), ('J', 1, 8), ('LL', 1, 8), ('Ñ', 1, 8),
                    ('RR', 1, 8), ('X', 1, 8), ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_espagnol.txt'
        # DICTIONAIRE ITALIEN
        elif self.langue.upper() == 'IT':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('O', 15, 1), ('A', 14, 1), ('I', 12, 1), ('E', 11, 1), ('C', 6, 2),
                    ('R', 6, 2), ('S', 6, 2), ('T', 6, 2), ('L', 5, 3), ('M', 5, 3),
                    ('N', 5, 3), ('U', 5, 3), ('B', 3, 5), ('D', 3, 5), ('F', 3, 5),
                    ('P', 3, 5), ('V', 3, 5), ('G', 2, 8), ('H', 2, 8), ('Z', 2, 8),
                    ('Q', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_italien.txt'
        # DICTIONAIRE NORVEGIEN
        elif self.langue.upper() == 'NO':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 9, 1), ('A', 7, 1), ('N', 6, 1), ('R', 6, 1), ('S', 6, 1),
                    ('T', 6, 1), ('D', 5, 1), ('I', 5, 1), ('L', 5, 1), ('F', 4, 2),
                    ('G', 4, 2), ('K', 4, 2), ('O', 4, 2), ('M', 3, 2), ('H', 3, 3),
                    ('B', 3, 4), ('U', 3, 4), ('V', 3, 4), ('J', 2, 4), ('P', 2, 4),
                    ('Å', 2, 4), ('Ø', 2, 5), ('Y', 1, 6), ('Æ', 1, 6), ('W', 1, 8),
                    ('C', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_norvegien.txt'
        # DICTIONAIRE NÉERLANDAIS
        elif self.langue.upper() == 'NE':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 18, 1), ('N', 10, 1), ('A', 6, 1), ('O', 6, 1), ('I', 4, 1),
                    ('D', 5, 2), ('R', 5, 2), ('T', 5, 2), ('S', 4, 2), ('G', 3, 3),
                    ('K', 3, 3), ('L', 3, 3), ('M', 3, 3), ('B', 2, 3), ('P', 2, 3),
                    ('U', 3, 4), ('H', 2, 4), ('J', 2, 4), ('V', 2, 4), ('Z', 2, 4),
                    ('IJ', 2, 4), ('F', 1, 4), ('C', 2, 5), ('W', 2, 5), ('X', 1, 8),
                    ('Y', 1, 8), ('Q', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_neerlandais.txt'
        # DICTIONAIRE DANOIS
        elif self.langue.upper() == 'DA':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 9, 1), ('A', 7, 1), ('N', 6, 1), ('R', 6, 1), ('D', 5, 2),
                    ('L', 5, 2), ('O', 5, 2), ('S', 5, 2), ('T', 5, 2), ('B', 4, 3),
                    ('I', 4, 3), ('K', 4, 3), ('F', 3, 3), ('G', 3, 3), ('M', 3, 3),
                    ('U', 3, 3), ('V', 3, 3), ('H', 2, 4), ('J', 2, 4), ('P', 2, 4),
                    ('Y', 2, 4), ('Æ', 2, 4), ('Ø', 2, 4), ('Å', 2, 4), ('C', 2, 8),
                    ('X', 1, 8), ('Z', 1, 8)]
            nom_fichier_dictionnaire = 'dictionnaire_danois.txt'
        # DICTIONNAIRE BULGARE
        elif self.langue.upper() == 'BU':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 9, 1), ('O', 9, 1), ('E', 8, 1), ('И', 8, 1), ('T', 5, 1),
                    ('H', 4, 1), ('П', 4, 1), ('P', 4, 1), ('C', 4, 1), ('B', 4, 2),
                    ('M', 4, 2), ('Б', 3, 2), ('Д', 3, 2), ('К', 3, 2), ('Л', 3, 2),
                    ('Г', 3, 3), ('Ъ', 2, 3), ('Ж', 2, 4), ('З', 2, 4), ('У', 3, 5),
                    ('Ч', 2, 5), ('Я', 2, 5), ('Й', 1, 5), ('X', 1, 5), ('Ц', 1, 8),
                    ('Ш', 1, 8), ('Ю', 1, 8), ('Ф', 1, 10), ('Щ', 1, 10), ('Ь', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_bulgare.txt'
        # DICTIONNAIRE ESTONIEN
        elif self.langue.upper() == 'ET':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 10, 1), ('E', 9, 1), ('I', 9, 1), ('S', 8, 1), ('T', 7, 1),
                    ('K', 5, 1), ('L', 5, 1), ('O', 5, 1), ('U', 5, 1), ('D', 4, 2),
                    ('M', 4, 2), ('N', 4, 2), ('R', 2, 2), ('G', 2, 3), ('V', 2, 3),
                    ('B', 1, 4), ('H', 2, 4), ('J', 2, 4), ('Õ', 2, 4), ('P', 2, 4),
                    ('Ä', 2, 5), (' Ü', 2, 5), ('Ö', 2, 6), ('F', 1, 8), ('Š', 1, 10),
                    ('Z', 1, 10), ('Ž', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_estonien.txt'
        # DICTIONNAIRE GREC
        elif self.langue.upper() == 'GR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 12, 1), ('E', 8, 1), ('I', 8, 1), ('T', 7, 1), ('H', 7, 1),
                    ('Σ', 7, 1), ('N', 6, 1), ('O', 6, 1), ('K', 4, 2), ('Π', 4, 2),
                    ('P', 5, 2), ('Y', 4, 2), ('Λ', 3, 3), ('M', 3, 3), ('Ω', 3, 3),
                    ('Γ', 2, 4), ('Δ', 2, 4), ('B', 1, 8), ('Φ', 1, 8), ('X', 1, 8),
                    ('Z', 1, 10), ('Θ', 1, 10), ('Ξ', 1, 10), ('Ψ', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_grec.txt'
        # DICTIONNAIRE CROATE
        elif self.langue.upper() == 'CR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 11, 1), ('I', 10, 1), ('E', 9, 1), ('O', 9, 1), ('N', 6, 1),
                    ('R', 5, 1), ('S', 5, 1), ('T', 5, 1), ('J', 4, 1), ('U', 4, 1),
                    ('K', 3, 2), ('M', 3, 2), ('P', 3, 2), ('V', 3, 2), ('D', 3, 3),
                    ('G', 2, 3), ('L', 2, 3), ('Z', 2, 3), ('B', 1, 3), ('Č', 1, 3),
                    ('C', 1, 4), ('H', 1, 4), ('LJ', 1, 4), ('NJ', 1, 4), ('Š', 1, 4),
                    ('Ž', 1, 4), ('Ć', 1, 5), ('F', 1, 8), ('DŽ', 1, 10), ('Đ', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_croate.txt'
        # DICTIONNAIRE HONGROIS
        elif self.langue.upper() == 'HO':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 6, 1), ('E', 6, 1), ('K', 6, 1), ('T', 5, 1), ('Á', 4, 1),
                    ('L', 4, 1), ('N', 4, 1), ('R', 4, 1), ('I', 3, 1), ('M', 3, 1),
                    ('O', 3, 1), ('S', 3, 1), ('B', 2, 3), ('D', 2, 3), ('G', 2, 3),
                    ('Ó', 2, 3), ('É', 3, 3), ('H', 2, 3), ('SZ', 2, 3), ('V', 2, 3),
                    ('F', 2, 4), ('GY', 2, 4), ('J', 2, 4), ('Ö ', 2, 4), ('P', 2, 4),
                    ('U', 2, 4), ('Ü', 2, 4), ('Z', 2, 4), ('C', 1, 5), ('Í', 1, 5),
                    ('NY', 1, 5), ('CS', 1, 7), ('Ő', 1, 7), ('Ú', 1, 7), ('Ű', 1, 7),
                    ('LY', 1, 8), ('ZS', 1, 8), ('TY', 1, 10), ]
            nom_fichier_dictionnaire = 'dictionnaire_hongrois.txt'
        # DICTIONNAIRE LATIN
        elif self.langue.upper() == 'LA':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('V', 9, 2), ('S', 8, 1),
                    ('T', 8, 1), ('R', 7, 1), ('O', 5, 1), ('C', 4, 2), ('M', 4, 2),
                    ('N', 4, 2), ('D', 3, 2), ('L', 3, 2), ('Q', 3, 3), ('B', 2, 4),
                    ('G', 2, 4), ('P', 2, 4), ('X', 2, 4), ('F', 1, 8), ('H', 1, 8)]
            nom_fichier_dictionnaire = 'dictionnaire_latin.txt'
        # DICTIONNAIRE ISLANDAIS
        elif self.langue.upper() == 'IS':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 10, 1), ('I', 8, 1), ('N', 8, 1), ('R', 7, 1), ('E', 6, 1),
                    ('S', 6, 1), ('U', 6, 1), ('T', 5, 1), ('Ð', 5, 2), ('G', 4, 2),
                    ('K', 3, 2), ('L', 3, 2), ('M', 3, 2), ('F', 3, 3), ('O', 3, 3),
                    ('H', 2, 3), ('V', 2, 3), ('Á', 2, 4), ('D', 2, 4), ('Í ', 2, 4),
                    ('Þ', 1, 4), ('J', 1, 5), ('Æ', 1, 5), ('B', 1, 6), ('É ', 1, 6),
                    ('Ó', 1, 6), ('Ö ', 1, 7), ('Y', 1, 7), ('P', 1, 8), ('Ú ', 1, 8),
                    ('Ý', 1, 9), ('X', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_islandais.txt'
        # DICTIONAIRE PORTUGAIS ok
        elif langue.upper() == 'PO':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 14, 1), ('I', 10, 1), ('O', 10, 1), ('S', 8, 1), ('U', 7, 1),
                    ('M', 6, 1), ('R', 6, 1), ('E', 5, 1), ('T', 5, 1), ('C', 4, 2),
                    ('P', 4, 2), ('D', 5, 2), ('L', 5, 2), ('N', 4, 3), ('B', 3, 3),
                    ('Ç', 2, 3), ('F', 2, 4), ('G', 2, 4), ('H', 2, 4), ('V', 2, 4),
                    ('J', 2, 5), ('Q', 1, 6), ('X', 1, 8), ('Z', 1, 8)]
            nom_fichier_dictionnaire = 'dictionnaire_portugais.txt'

        if partie_a_charger == "":
            self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for i in
                                  range(occurences)]
        else:
            self.jetons_libres = self.donnees_de_partie.jetons_libres
            self.liste_codes_position_a_valider = []

        with open(nom_fichier_dictionnaire, 'r', encoding="utf8") as f:
            self.dictionnaire = set([x[:-1].upper() for x in f.readlines() if len(x[:-1]) > 1])

        self.position_jeton_selectionne = None

        self.title("Scrabble TP4 Isabelle Eysseric et Roger Gaudreault")
        self.geometry("1x1+0+0")

        if partie_a_charger == "":
            # Form pour avoir le nom et le choix d'image du joueur avant de dessiner l'interface
            self.form_joueurs = Toplevel(self)
            self.form_joueurs.title("Qui veut jouer ?")
            self.form_joueurs.configure(bg="#445569")
            self.form_joueurs.geometry("500x700+200+0")

            fr_intro_joueur = Frame(self.form_joueurs, bg="#445569")
            fr_intro_joueur.grid(row=0, column=0)
            label_intro_joueur = Label(fr_intro_joueur, text="Chaque joueur doit entrer son nom",
                                       padx=50, pady=50, font=("Impact", 20), bg="#445569", foreground='white')
            label_intro_joueur.grid(row=0, column=0)

            image_equipe = Frame(self.form_joueurs,  bg = "#445569")
            image_equipe.grid(row=1, column=0)
            image3 = PhotoImage(file= "equipe.png")
            label_image_equipe = Label(image_equipe, image = image3,  bg = "#445569")
            label_image_equipe.grid()

            fr_entry_joueur = Frame(self.form_joueurs, bg="#445569")
            fr_entry_joueur.grid(row=2, column=0)
            Label(fr_entry_joueur, text="Joueur 1 :", pady=10, font=("Helvetica", 15), bg='#445569',
                  foreground='white').grid(row=0, column=0, sticky=W)
            Label(fr_entry_joueur, text="Joueur 2 :", pady=10, font=("Helvetica", 15), bg='#445569',
                  foreground='white').grid(row=1, column=0, sticky=W)
            self.form_joueurs.jo1 = StringVar()
            self.form_joueurs.jo2 = StringVar()

            self.form_joueurs.jo1.set("Joueur 1")
            self.form_joueurs.jo2.set("Joueur 2")

            Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo1, bg='#FDF4C9',
                  font=('courier new', 10, 'italic'), foreground='#445569').grid(row=0, column=1, sticky=E)
            Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo2, bg='#FDF4C9',
                  font=('courier new', 10, 'italic'), foreground='#445569').grid(row=1, column=1, sticky=E)

            if self.nb_joueurs >= 3:
                Label(fr_entry_joueur, text="Joueur 3 :", pady=10, font=("Helvetica", 15),
                      bg='#445569', foreground='white').grid(row=2, column=0, sticky=W)
                self.form_joueurs.jo3 = StringVar()
                self.form_joueurs.jo3.set("Joueur 3")
                Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo3, bg='#FDF4C9',
                      font=('courier new', 10, 'italic'), foreground='#445569').grid(row=2, column=1, sticky=E)
            if self.nb_joueurs == 4:
                Label(fr_entry_joueur, text="Joueur 4 :", pady=10, font=("Helvetica", 15), bg='#445569',
                      foreground='white').grid(row=3, column=0, sticky=W)
                self.form_joueurs.jo4 = StringVar()
                self.form_joueurs.jo4.set("Joueur 4")
                Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo4, bg='#FDF4C9',
                      font=('courier new', 10, 'italic'), foreground='#445569').grid(row=3, column=1, sticky=E)
            bouton_valider_joueurs = Button(self.form_joueurs, text="Nous sommes prêts à commencer",
                                            command=self.comm_bouton_valider_joueurs, font=('Impact', 15), bg='#FDF4C9',
                                            foreground="#445569").grid(row=10, column=0, pady=10)

            self.wait_window(self.form_joueurs)

        self.geometry(
            str(int(self.winfo_screenwidth() * 0.95)) + "x" + str(int(self.winfo_screenheight()) - 100) + "+0+0")
        self.frame_du_plateau = Frame(self, bg="#445569", bd=20)
        self.frame_du_plateau.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        self.plateau = Plateau(self.frame_du_plateau)

        if partie_a_charger != "":
            self.plateau.cases = self.donnees_de_partie.cases

        self.plateau.grid(row=1, column=0)
        self.plateau.bind("<Button-1>", self.gerer_click_plateau)
        self.plateau.bind("<Double-Button-1>", self.call_reprendre_jetons)

        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.joueur_actif = None

        Label(self, text='NOTRE SUPER PLATEAU DE SCRABBLE', font='Impact', bg='#FDF4C9').grid(row=0, column=0, padx=10,
                                                                                              pady=10, sticky=NSEW)
        Label(self, text='LES JOUEURS', font='Impact', bg='#FDF4C9').grid(row=0, column=1, padx=10, pady=10,
                                                                          sticky=NSEW)

        # Frame à côté du plateau:
        self.frame_a_cote_plateau = Frame(self, bg="#445569", bd=20,
                                          width=(Plateau.PIXELS_PAR_CASE * Plateau.DIMENSION),
                                          height=Plateau.PIXELS_PAR_CASE * Plateau.DIMENSION)
        self.frame_a_cote_plateau.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

        # FRAME POUR LES JOUEURS:
        self.mes_joueurs = Frame(self.frame_a_cote_plateau, bg="#445569")
        self.mes_joueurs.grid(row=3, column=0, padx=10, pady=10)

        self.frame_chevalet = Frame(self.frame_a_cote_plateau, bg="#445569")
        self.frame_chevalet.text = "ABS"
        self.frame_chevalet.grid(row=1, column=0)
        self.chevalet = Chevalet(self.frame_chevalet)
        self.chevalet.bind("<Button-1>", self.gerer_click_jeton_chevalet)
        self.chevalet.grid(row=1, column=0)
        self.fr_label_joueur_actif = Frame(self.frame_a_cote_plateau, bg='#445569', padx=100, pady=15)
        self.text_label_joueur_actif = StringVar()

        # self.text_label_joueur_actif.set(Scrabble.traduction_langue)
        self.fr_label_joueur_actif.grid(row=2, column=0)
        self.label_joueur_actif = Label(self.fr_label_joueur_actif, textvariable=self.text_label_joueur_actif,
                                        foreground='white', bg='#445569', font=("Helvetica", 20))
        self.label_joueur_actif.grid(row=0, column=0)

        self.width_button = 16

        # Frame dans à côté du plateau avec la boite :
        la_boite = Frame(self.frame_a_cote_plateau, bg='#445569')
        la_boite.grid(row=4, column=0, padx=10, pady=10)
        button_changer_lettres = Button(la_boite, text='Échanger des lettres', font='Impact', width=self.width_button,
                                        bg='#FDF4C9', foreground="#445569")
        button_changer_lettres.grid(row=0, column=0, padx=10, pady=10)
        button_changer_lettres.bind("<Button-1>", self.call_changer_lettres)

        button_melanger = Button(la_boite, text='Mélange mes jetons', font='Impact', width=self.width_button,
                                 bg='#FDF4C9', foreground="#445569")
        button_melanger.grid(row=0, column=1, padx=10, pady=10)
        button_melanger.bind("<Button-1>", self.call_melanger_jetons)

        button_passer = Button(la_boite, text='Passer mon tour', font='Impact', width=self.width_button, bg='#FDF4C9',
                               foreground="#445569")
        button_passer.grid(row=0, column=2, padx=10, pady=10)
        button_passer.bind("<Button-1>", self.call_joueur_suivant)

        button_valider = Button(la_boite, text='Valider tour', font='Impact', width=self.width_button, bg='#FDF4C9',
                                foreground="#445569")
        button_valider.grid(row=1, column=0, padx=10, pady=10)
        button_valider.bind("<Button-1>", self.call_valider_tour)

        button_reprise_jetons = Button(la_boite, text='Reprendre jetons', font='Impact', width=self.width_button,
                                       bg='#FDF4C9', foreground="#445569")
        button_reprise_jetons.grid(row=1, column=1, padx=10, pady=10)
        button_reprise_jetons.bind("<Button-1>", self.call_reprendre_jetons)

        button_nouvelle_partie = Button(la_boite, text='Nouvelle partie', font='Impact', width=self.width_button,
                                        bg='#FDF4C9', foreground="#445569")
        button_nouvelle_partie.grid(row=1, column=2, padx=10, pady=10)
        button_nouvelle_partie.bind("<Button-1>", self.call_nouvelle_partie)

        button_enregistrer_partie = Button(la_boite, text='Enregistrer partie', font='Impact', width=self.width_button,
                                           bg='#FDF4C9', foreground="#445569")
        button_enregistrer_partie.grid(row=2, column=0, padx=10, pady=10)
        button_enregistrer_partie.bind("<Button-1>", self.call_sauvegarde)

        button_liste_mot = Button(la_boite, text='Mots du plateau', font='Impact', width=self.width_button,
                                  bg='#FDF4C9', foreground="#445569")
        button_liste_mot.grid(row=2, column=1, padx=10, pady=10)
        button_liste_mot.bind("<Button-1>", self.call_liste_mots_au_plateau)

        button_abandonner = Button(la_boite, text='Abandonner', font='Impact', width=self.width_button, bg='#FDF4C9',
                                   foreground="#445569")
        button_abandonner.grid(row=2, column=2, padx=10, pady=10)
        button_abandonner.bind("<Button-1>", self.call_joueur_abandonne)

        if partie_a_charger == "":
            self.joueur_suivant()
        else:
            self.joueur_actif = self.donnees_de_partie.joueur_actif
            self.plateau.dessiner_plateau()
            for i in range(self.nb_joueurs_restants):
                self.joueur_suivant()
            messagebox.showinfo(title="Vous revoilà !", message="Continuons la partie où nous l'avions laissée...")
        self.protocol("WM_DELETE_WINDOW", self.demande_sauvegarde_avant_quitter)

    def demande_sauvegarde_avant_quitter(self):
        x = messagebox.askyesnocancel(title="La fenêtre veut fermer...",
                                      message="Voulez-vous sauvegarder la partie avant de quitter ?")
        if x is True:
            self.sauvegarde()
        if x is False:
            self.destroy()
        if x is None:
            pass

    def call_nouvelle_partie(self, event):
        x = messagebox.askyesnocancel(title="Repartir à zéro...", message="Une nouvelle partie va commencer avec"
                                                                          " les mêmes joueurs.\n\nVoulez-vous sauvegarder la partie avant de quitter ?")
        if x is True:
            self.sauvegarde_sans_quitter()

        if x is True or x is False:
            self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for i in
                                  range(occurences)]
            for i in range(Plateau.DIMENSION):
                for j in range(Plateau.DIMENSION):
                    self.plateau.cases[i][j].jeton_occupant = None
            self.plateau.dessiner_plateau()
            for joueurs in self.joueurs:
                joueurs.repartir_points_a_0()
                for i in range(Joueur.TAILLE_CHEVALET):
                    joueurs.retirer_jeton(i)
            self.dessiner_joueurs()
            for j in range(7):
                Chevalet.dessiner_jeton_chevalet(self.chevalet, None, j)
            messagebox.showinfo("Ça recommence...", message="La nouvelle partie va commencer.\n\nBonne chance !")
            self.joueur_actif = None
            self.joueur_suivant()
            messagebox.showinfo(title="C'est le hasard qui décide...",
                                message="Le premier joueur sera: {}.".format(self.joueur_actif.nom))
            self.mots_au_plateau = []

    def redimensionner(self, event):

        self.largeur_app = event.width

    def call_sauvegarde(self, event):
        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("de sauvegarder.")
        else:
            self.sauvegarde()

    def sauvegarde(self):
        partie = Sauvegarde(self.nb_joueurs, self.nb_joueurs_restants,
                            self.plateau.cases, self.jetons_libres, self.joueurs, self.joueur_actif,
                            self.mots_au_plateau, self.langue)
        valide = False
        while not valide:
            nom_fichier = filedialog.asksaveasfilename()
            with open(nom_fichier, "wb") as f:
                pickle.dump(partie, f)
            valide = True
            continuer = messagebox.askyesno(title="Partie sauvegardée...",
                                            message="La partie est sauvegardée, voulez-vous continuer à jouer ?")

            if continuer is False:
                messagebox._show(title="Il est parti!", message="Au revoir!")
                self.destroy()

    def sauvegarde_sans_quitter(self):
        partie = Sauvegarde(self.nb_joueurs, self.nb_joueurs_restants,
                            self.plateau.cases, self.jetons_libres, self.joueurs, self.joueur_actif,
                            self.mots_au_plateau, self.langue)
        valide = False
        while not valide:
            nom_fichier = filedialog.asksaveasfilename()
            with open(nom_fichier, "wb") as f:
                pickle.dump(partie, f)
            valide = True
            messagebox.showinfo(title="Partie sauvegardée...", message="La partie est sauvegardée")

    def dessiner_joueurs(self):
        if self.joueur_actif == self.joueurs[0]:
            joueur1 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",
                            highlightthickness=10)
        else:
            joueur1 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",
                            highlightthickness=10)
        joueur1.grid(row=1, column=0, padx=10, pady=10)
        self.label_score_joueur1 = Label(joueur1, text="Score: {}".format(self.joueurs[0].points),
                                         font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
        self.label_score_joueur1.grid(row=3, column=0)
        self.label_nom1 = Label(joueur1, text=self.joueurs[0].nom, font=("Impact", 20), bg='#FDF4C9', width=21)
        self.label_nom1.grid(row=0, column=0, sticky=N)

        chevalet1 = Frame(joueur1)
        chevalet1.grid(row=4, column=0)

        if self.joueurs[0].a_abandonne is True:
            self.abandonne1 = PhotoImage(file='abandonne.png')
            self.abandonne1_label1 = Label(chevalet1, image=self.abandonne1, bg='#FDF4C9')
            self.abandonne1_label1.grid(row=1, column=0, sticky=NSEW)

        else:
            self.label_lettre1_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(0)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre1_joueur1.grid(row=0, column=0)
            self.label_lettre2_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(1)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre2_joueur1.grid(row=0, column=1)
            self.label_lettre3_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(2)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre3_joueur1.grid(row=0, column=2)
            self.label_lettre4_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(3)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre4_joueur1.grid(row=0, column=3)
            self.label_lettre5_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(4)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre5_joueur1.grid(row=0, column=4)
            self.label_lettre6_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(5)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre6_joueur1.grid(row=0, column=5)
            self.label_lettre7_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(6)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre7_joueur1.grid(row=0, column=6)

        # Frame dans les joueurs avec Joueur 2 :
        if self.joueur_actif == self.joueurs[1]:
            joueur2 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",
                            highlightthickness=10)
        else:
            joueur2 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",
                            highlightthickness=10)
        joueur2.grid(row=1, column=1, padx=10, pady=10)
        self.label_score_joueur2 = Label(joueur2, text="Score: {}".format(self.joueurs[1].points),
                                         font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
        self.label_score_joueur2.grid(row=3, column=0)
        self.label_nom2 = Label(joueur2, text=self.joueurs[1].nom, font=("Impact", 20), bg='#FDF4C9')
        self.label_nom2.grid(row=0, column=0, sticky=N)
        chevalet2 = Frame(joueur2)
        chevalet2.grid(row=4, column=0)

        if self.joueurs[1].a_abandonne is True:
            self.abandonne2 = PhotoImage(file='abandonne.png')
            self.abandonne2_label1 = Label(chevalet2, image=self.abandonne2, bg='#FDF4C9')
            self.abandonne2_label1.grid(row=1, column=0, sticky=NSEW)

        else:
            self.label_lettre1_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(0)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre1_joueur2.grid(row=0, column=0)
            self.label_lettre2_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(1)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre2_joueur2.grid(row=0, column=1)
            self.label_lettre3_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(2)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre3_joueur2.grid(row=0, column=2)
            self.label_lettre4_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(3)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre4_joueur2.grid(row=0, column=3)
            self.label_lettre5_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(4)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre5_joueur2.grid(row=0, column=4)
            self.label_lettre6_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(5)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre6_joueur2.grid(row=0, column=5)
            self.label_lettre7_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(6)),
                                               font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre7_joueur2.grid(row=0, column=6)

        # Frame dans les joueurs avec Joueur 3 :
        if nb_joueurs >= 3:
            if self.joueur_actif == self.joueurs[2]:
                joueur3 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",
                                highlightthickness=10)
            else:
                joueur3 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",
                                highlightthickness=10)
            joueur3.grid(row=2, column=0, padx=10, pady=10)

            self.label_score_joueur3 = Label(joueur3, text="Score: {}".format(self.joueurs[2].points),
                                             font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
            self.label_score_joueur3.grid(row=3, column=0)
            self.label_nom3 = Label(joueur3, text=self.joueurs[2].nom, font=("Impact", 20), bg='#FDF4C9')
            self.label_nom3.grid(row=0, column=0, sticky=N)
            chevalet3 = Frame(joueur3)
            chevalet3.grid(row=4, column=0)

            if self.joueurs[2].a_abandonne is True:
                self.abandonne3 = PhotoImage(file='abandonne.png')
                self.abandonne3_label1 = Label(chevalet3, image=self.abandonne3, bg='#FDF4C9')
                self.abandonne3_label1.grid(row=1, column=0, sticky=NSEW)

            else:
                self.label_lettre1_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(0)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre1_joueur3.grid(row=0, column=0)
                self.label_lettre2_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(1)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre2_joueur3.grid(row=0, column=1)
                self.label_lettre3_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(2)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre3_joueur3.grid(row=0, column=2)
                self.label_lettre4_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(3)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre4_joueur3.grid(row=0, column=3)
                self.label_lettre5_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(4)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre5_joueur3.grid(row=0, column=4)
                self.label_lettre6_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(5)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre6_joueur3.grid(row=0, column=5)
                self.label_lettre7_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(6)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre7_joueur3.grid(row=0, column=6)

        # Frame dans les joueurs avec Joueur 4 :
        if nb_joueurs == 4:
            if self.joueur_actif == self.joueurs[3]:
                joueur4 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",
                                highlightthickness=10)
            else:
                joueur4 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",
                                highlightthickness=10)
            joueur4.grid(row=2, column=1, padx=10, pady=10)
            self.label_score_joueur4 = Label(joueur4, text="Score: {}".format(self.joueurs[3].points),
                                             font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
            self.label_score_joueur4.grid(row=3, column=0)
            self.label_nom4 = Label(joueur4, text=self.joueurs[3].nom, font=("Impact", 20), bg='#FDF4C9')
            self.label_nom4.grid(row=0, column=0, sticky=N)
            chevalet4 = Frame(joueur4)
            chevalet4.grid(row=4, column=0)

            if self.joueurs[3].a_abandonne is True:
                self.abandonne4 = PhotoImage(file='abandonne.png')
                self.abandonne4_label1 = Label(chevalet4, image=self.abandonne4, bg='#FDF4C9')
                self.abandonne4_label1.grid(row=1, column=0, sticky=NSEW)
            else:
                self.label_lettre1_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(0)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre1_joueur4.grid(row=0, column=0)
                self.label_lettre2_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(1)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre2_joueur4.grid(row=0, column=1)
                self.label_lettre3_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(2)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre3_joueur4.grid(row=0, column=2)
                self.label_lettre4_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(3)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre4_joueur4.grid(row=0, column=3)
                self.label_lettre5_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(4)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre5_joueur4.grid(row=0, column=4)
                self.label_lettre6_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(5)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre6_joueur4.grid(row=0, column=5)
                self.label_lettre7_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(6)),
                                                   font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre7_joueur4.grid(row=0, column=6)

    def gerer_click_jeton_chevalet(self, event):
        pos = int(event.x // Chevalet.PIXELS_PAR_CASE)
        if self.position_jeton_selectionne is None:
            self.position_jeton_selectionne = pos
            self.affiche_chevalet_joueur_actif()

        else:
            if pos == self.position_jeton_selectionne:
                self.position_jeton_selectionne = None
                self.affiche_chevalet_joueur_actif()
            else:

                self.joueur_actif.permuter_jetons(pos, self.position_jeton_selectionne)
                self.dessiner_joueurs()
                self.position_jeton_selectionne = None
                self.affiche_chevalet_joueur_actif()

    def gerer_click_plateau(self, event):
        index_ligne = (event.y // Plateau.PIXELS_PAR_CASE)
        index_colonne = event.x // Plateau.PIXELS_PAR_CASE
        code_ligne = chr(65 + index_ligne)
        code_position = code_ligne + str(index_colonne + 1)
        # self.meilleur_mot()

        if self.plateau.cases[index_ligne][index_colonne].est_vide():
            if self.position_jeton_selectionne is not None:
                jeton = self.joueur_actif.retirer_jeton(self.position_jeton_selectionne)
                self.plateau.ajouter_jeton(jeton, code_position)
                self.plateau.dessiner_jeton(jeton, index_ligne, index_colonne, Plateau.PIXELS_PAR_CASE)
                self.dessiner_joueurs()
                self.position_jeton_selectionne = None
                self.affiche_chevalet_joueur_actif()


                self.liste_codes_position_a_valider += [ code_position]
                self.liste_lettre_a_valider += [jeton]

        else:
            if code_position in self.liste_codes_position_a_valider:
                jeton = self.plateau.retirer_jeton(code_position)
                index_dans_liste_du_jeton_retire = self.liste_codes_position_a_valider.index(code_position)
                del self.liste_codes_position_a_valider[index_dans_liste_du_jeton_retire]
                del self.liste_lettre_a_valider[index_dans_liste_du_jeton_retire]
                self.joueur_actif.ajouter_jeton(jeton)
                self.affiche_chevalet_joueur_actif()
                self.plateau.dessiner_plateau()

            self.position_jeton_selectionne = None
            self.affiche_chevalet_joueur_actif()

    def call_joueur_abandonne(self,event):

        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("d'abandonner la partie.")
        else:
            self.confirmation_abandon = False
            if messagebox.askyesno(title="Ça devient trop compliqué ?",
                                   message="{}, voulez-vous vraiment abandonner ?".format(self.joueur_actif.nom)):
                self.joueur_actif.a_abandonne = True
                self.nb_joueurs_restants -= 1
                self.joueur_suivant()
                if self.partie_terminee():
                    messagebox.showinfo(title="Oh! Comme nous avons eu du plaisir !",
                                        message="Partie terminée !\n\n{} a remporté la partie car il est le seul joueur"
                                                " restant.\n\n Il remporte avec un score de {} points."
                                                "\n\n".format(self.joueur_actif.nom, self.joueur_actif.points))
                    self.destroy()

                self.dessiner_joueurs()

    def comm_bouton_valider_joueurs(self):
        self.joueurs[0].nom = self.form_joueurs.jo1.get()
        self.joueurs[1].nom = self.form_joueurs.jo2.get()
        if self.nb_joueurs >= 3:
            self.joueurs[2].nom = self.form_joueurs.jo3.get()
        if self.nb_joueurs == 4:
            self.joueurs[3].nom = self.form_joueurs.jo4.get()
        self.form_joueurs.destroy()

    def valider_positions_jetons(self):
        if self.plateau.valider_positions_avant_ajout(self.liste_codes_position_a_valider) is not True:
            try:
                raise positions_non_valides(len(self.liste_codes_position_a_valider))
            finally:
                self.reprendre_jetons()
            return False
        return True

    def call_valider_tour(self, event):

        if self.liste_codes_position_a_valider == []:
            self.grab_set()  # Prevent clicking root while messagebox is open
            messagebox.showinfo(title="Rien ne se passe...",
                                message="Il faut placer au moins une lettre pour pouvoir valider. ")
            self.wait_window()  # Prevent clicking root while messagebox is open

        else:
            if self.valider_positions_jetons():
                mots, score = self.plateau.placer_mots(self.liste_lettre_a_valider, self.liste_codes_position_a_valider)
                if any([not self.mot_permis(m) for m in mots]):
                    try:
                        raise mots_non_valides()
                    finally:
                        self.reprendre_jetons()

                else:
                    messagebox.showinfo(title="Bon coup !", message="Bravo {}\n\nMot(s) formé(s):\n{}".
                                        format(self.joueur_actif.nom, "\n".join(mots) + "\nScore obtenu:" + str(score)))

                    self.joueur_actif.ajouter_points(score)
                    self.mots_au_plateau += mots
                    valide = True
                    self.joueur_suivant()

    def call_reprendre_jetons(self, event):
        self.reprendre_jetons()

    def reprendre_jetons(self):
        for pos in self.liste_codes_position_a_valider:
            jeton = self.plateau.retirer_jeton(pos)
            self.joueur_actif.ajouter_jeton(jeton)
        self.dessiner_joueurs()
        self.plateau.dessiner_plateau()
        for i in range(Chevalet.DIMENSION):
            Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i,
                                             self.position_jeton_selectionne)
        self.liste_lettre_a_valider = []
        self.liste_codes_position_a_valider = []

    def call_joueur_suivant(self, event):

        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("de passer votre tour !")

        else:
            self.position_jeton_selectionne = None
            self.joueur_suivant()
            self.affiche_chevalet_joueur_actif()

    def call_melanger_jetons(self, event):
        self.position_jeton_selectionne = None
        self.joueur_actif.melanger_jetons()
        self.affiche_chevalet_joueur_actif()
        self.dessiner_joueurs()
        self.affiche_chevalet_joueur_actif()

    def call_liste_mots_au_plateau(self, event):
        str = """Les mots au plateau sont:\n{}""".format("\n".join(self.mots_au_plateau))
        messagebox.showinfo(title="En un mot, voici les mots",
                            message=str)

    def call_changer_lettres(self, event):
        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("de changer des lettres.")
        else:
            self.liste_positions_lettres_a_changer = []
            # Prevent clicking root while toplevel is open
            self.form_changer_lettres = Toplevel(self)
            self.form_changer_lettres.grab_set()
            self.form_changer_lettres.title("Échangeons des lettres")
            self.form_changer_lettres.configure(bg="#445569")

            fr_intro = Frame(self.form_changer_lettres)
            fr_intro.grid(row=0, column=0)
            label_intro = Label(fr_intro,
                                text="Veuillez sélectionner en bleu les lettres que vous désirez échanger puis appuyer sur VALIDER.\n\n Vos lettres seront changées, mais vous perdrez votre tour.",
                                padx=50, pady=20, foreground='white', bg='#445569', font=("Helvetica", 20))
            label_intro.grid(row=0, column=0)

            fr_chevalet = Frame(self.form_changer_lettres)
            fr_chevalet.grid(row=1, column=0)

            self.chevalet = Chevalet(self.form_changer_lettres)
            self.chevalet.grid(row=2, column=0, padx=50, pady=20)
            for i in range(Chevalet.DIMENSION):
                Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i,
                                                 self.position_jeton_selectionne)
            self.chevalet.bind("<Button-1>", self.gerer_click_jeton_chevalet_a_changer)
            self.form_changer_lettres.protocol("WM_DELETE_WINDOW", self.form_changer_lettres_close)

            self.valider_change_lettres = Button(self.form_changer_lettres, text='Échanger les lettres', font='Impact',
                                                 width=self.width_button, bg='#FDF4C9', foreground="#445569")
            self.valider_change_lettres.grid(padx=10, pady=20)
            self.valider_change_lettres.bind("<Button-1>", self.call_valider_change_lettres)
            self.annule_change_lettres = Button(self.form_changer_lettres,
                                                text='Annuler, je ne veux pas perdre mon tour', font='Impact', width=50,
                                                bg='#FDF4C9', foreground="#445569")
            self.annule_change_lettres.grid(padx=10, pady=20)
            self.annule_change_lettres.bind("<Button-1>", self.call_annule_change_lettres)
            self.wait_window()  # Prevent clicking root while toplevel is open

    def call_valider_change_lettres(self, event):
        self.changer_jetons(self.liste_positions_lettres_a_changer)
        self.joueur_suivant()
        self.form_changer_lettres_close()

    def call_annule_change_lettres(self, event):
        self.form_changer_lettres.destroy()

    def gerer_click_jeton_chevalet_a_changer(self, event):
        pos = int(event.x // Chevalet.PIXELS_PAR_CASE)
        if pos not in self.liste_positions_lettres_a_changer:
            self.liste_positions_lettres_a_changer.append(pos)
        else:
            self.liste_positions_lettres_a_changer.remove(pos)
        for i in range(Chevalet.DIMENSION):
            if i not in self.liste_positions_lettres_a_changer:
                Chevalet.dessiner_jeton_chevalet(self.chevalet,
                                                 self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne)
            else:
                Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i, i)

    def form_changer_lettres_close(self):
        self.form_changer_lettres.destroy()

    def affiche_chevalet_joueur_actif(self):
        self.chevalet.delete(self)
        self.chevalet = Chevalet(self.frame_a_cote_plateau)
        self.chevalet.grid(row=1, column=0)
        for i in range(Chevalet.DIMENSION):
            Chevalet.dessiner_jeton_chevalet(self.chevalet,
                                             self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne)
        if len(self.jetons_libres) == 0:
            messagebox.showinfo(title="Partie terminée!",
                                message="Tous les jetons ont été distribués, la partie est maintenant terminée.\n\n"
                                        "Le joueur gagnant est {0} avec {1} points.\n\n"
                                        "Félicitations {0}!!\n\nLe programme va maintenant"
                                        " se fermer, au revoir!".format(self.determiner_gagnant().
                                                                        nom, self.determiner_gagnant().points))
            global quitter
            quitter = True
            self.destroy()
        self.chevalet.bind("<Button-1>", self.gerer_click_jeton_chevalet)

    def mot_permis(self, mot):
        """
        Permet de savoir si un mot est permis dans la partie ou pas en regardant dans le dictionnaire.
        :param mot: str, mot à vérifier.
        :return: bool, True si le mot est dans le dictionnaire, False sinon.
        """
        # retourne True si mot est dans le dict, False sinon...
        # upper car le read converti le dictionnaire en upper
        return mot.upper() in self.dictionnaire

    def determiner_gagnant(self):
        """
        Détermine le joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        il doit avoir le pointage le plus élevé de tous.
        :return: Joueur, un des joueurs gagnants, i.e si plusieurs sont à égalité on prend un au hasard.
        """
        # On retourne le dernier élément de la liste de joueurs triée en ordre croissant selon
        # le nombre de points des joueurs
        return sorted(self.joueurs, key=lambda joueur: joueur.points)[-1]

    def partie_terminee(self):
        """
        Vérifie si la partie est terminée. Une partie est terminée si il
        n'existe plus de jetons libres ou il reste moins de deux (2) joueurs. C'est la règle que nous avons choisi
        d'utiliser pour ce travail, donc essayez de
        négliger les autres que vous connaissez ou avez lu sur Internet.
        Returns:
            bool: True si la partie est terminée, et False autrement.
        """
        return self.jetons_libres == [] or self.nb_joueurs_restants == 1

    def joueur_suivant(self):
        """
        Change le joueur actif.
        Le nouveau joueur actif est celui à l'index du (joueur courant + 1)% nb_joueurs.
        Si on n'a aucun joueur actif, on détermine au harsard le suivant.
        """
        # On réévalue nb_joueurs en cas qu'un des joueurs originaux ait quitté
        self.nb_joueurs = len(self.joueurs)

        # On détermine un joueur au hasard si aucun joueur actif
        if self.joueur_actif is None:
            self.joueur_actif = self.joueurs[randint(0, nb_joueurs - 1)]

        # On passe au suivant
        index_courant = self.joueurs.index(self.joueur_actif)
        self.joueur_actif = self.joueurs[(index_courant + 1) % self.nb_joueurs]
        self.text_label_joueur_actif.set("{}, c'est à ton tour de jouer.".format(self.joueur_actif.nom))
        if self.joueur_actif.a_abandonne:
            self.joueur_suivant()
        for i in range(len(self.joueurs)):
            for jeton in self.tirer_jetons(self.joueurs[i].nb_a_tirer):
                self.joueurs[i].ajouter_jeton(jeton)
            for j in range(7):
                Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueurs[i].obtenir_jeton(j), j)

        self.dessiner_joueurs()
        self.affiche_chevalet_joueur_actif()
        self.liste_codes_position_a_valider = []
        self.liste_lettre_a_valider = []
        self.liste_positions_lettres_a_changer = []

    def tirer_jetons(self, n):
        """
        Simule le tirage de n jetons du sac à jetons et renvoie ceux-ci.
        Il s'agit de prendre au hasard des jetons dans self.jetons_libres et de les retourner.
        Pensez à utiliser la fonction shuffle du module random.
        :param n: le nombre de jetons à tirer.
        :return: Jeton list, la liste des jetons tirés.
        :exception: Levez une exception avec assert si n ne respecte pas la condition 0 <= n <= 7.
        """
        assert 0 <= n <= 7, "Le nombre de jetons à tirer au sort est invalide"
        shuffle(self.jetons_libres)  # On mélange les jetons
        jeton_liste = self.jetons_libres[:n]  # On crée une liste des jetons qu'on tire
        self.jetons_libres = self.jetons_libres[n:]  # Les jetons libres excluent maintenant ceux tirés
        return jeton_liste  # On retourne la liste des jetons tirés

    def jouer_un_tour(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Faire jouer à un des joueurs son tour entier jusqu'à ce qu'il place un mot valide sur le
        plateau.
        Pour ce faire
        1 - Afficher le plateau puis le joueur;
        2 - Demander les positions à jouer;
        3 - Retirer les jetons du chevalet;
        4 - Valider si les positions sont valides pour un ajout sur le plateau;
        5 - Si oui, placer les jetons sur le plateau, sinon retourner en 1;
        6 - Si tous les mots formés sont dans le dictionnaire, alors ajouter les points au joueur actif;
        7 - Sinon retirer les jetons du plateau et les remettre sur le chevalet du joueur, puis repartir en 1;
        8 - Afficher le plateau.

        :return: Ne retourne rien.
        """

        self.chevalet = Chevalet(self.frame_a_cote_plateau)
        self.chevalet.grid(row=1, column=0)
        for i in range(Chevalet.DIMENSION):
            Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i),i)

        self.update()
        valide = False

    def changer_jetons(self, pos_chevalet):
        """
        Faire changer au joueur actif ses jetons. La méthode doit demander au joueur de saisir les positions à
        changer les unes après les autres séparés par un espace.
        Si une position est invalide (utilisez Joueur.position_est_valide) alors redemander.
        Dès que toutes les positions valides les retirer du chevalier du joueur et lui en donner de nouveau.
        Enfin, on remet des jetons pris chez le joueur parmi les jetons libres.
        :return: Ne retourne rien.
        """

        liste_jetons_retires = []
        # On crée une liste de jetons tirés, nombre égale à la liste des positions entrées
        liste_jetons_tires = self.tirer_jetons(len(pos_chevalet))

        # retire le jeton,(position à None dans le chevalet) on ajoute ce jeton à la liste des jetons retiré
        # on ajoute au chevalet le premier élément de la liste de jetons tirés et on retire ce jeton de cette liste
        for i in pos_chevalet:
            liste_jetons_retires.append(self.joueur_actif.retirer_jeton(i))
            self.joueur_actif.ajouter_jeton(liste_jetons_tires[0])
            liste_jetons_tires = liste_jetons_tires[1:]

        # On retourne les jetons retirés dans la liste des jetons libres
        self.jetons_libres = self.jetons_libres + liste_jetons_retires

    def jouer(self):
        """
        Cette fonction permet de jouer la partie.
        Tant que la partie n'est pas terminée, on joue un tour.
        À chaque tour :
            - On change le joueur actif et on lui affiche que c'est son tour. ex: Tour du joueur 2.
            - On lui affiche ses options pour qu'il choisisse quoi faire:
                "Entrez (j) pour jouer, (p) pour passer votre tour, (c) pour changer certains jetons,
                (s) pour sauvegarder ou (q) pour quitter"
            Notez que si le joueur fait juste sauvegarder on ne doit pas passer au joueur suivant mais dans tous
             les autres cas on doit passer au joueur suivant. S'il quitte la partie on l'enlève de la liste des joueurs.
        Une fois la partie terminée, on félicite le joueur gagnant!

        :return Ne retourne rien.
        """
        abandon = False
        changer_joueur = False

        while not self.partie_terminee() and not abandon:

            if partie_a_charger == "":
                self.joueur_suivant()
                messagebox.showinfo(title="C'est le hasard qui décide...",
                                    message="Le premier joueur sera: {}.".format(self.joueur_actif.nom))
            self.plateau.dessiner_plateau()
            self.wait_window()  # Prevent clicking root while messagebox is open

    @staticmethod
    def charger_partie(nom_fichier):
        """ *** Vous n'avez pas à coder cette méthode ***
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment. Pensez à utiliser la fonction load du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: Scrabble, l'objet chargé en mémoire.
        """
        with open(nom_fichier, "rb") as f:
            objet = pickle.load(f)
        return objet


def accueil_close():
    if (messagebox.askyesno(title="Vous quittez si tôt ?", message="Voulez-vous vraiment quitter le jeu ?")):
        exit()


def bouton_accueil_commencer():
    acceuil.destroy()


def bouton_charger_partie():
    global partie_a_charger
    partie_a_charger = filedialog.askopenfilename()
    acceuil.destroy()


def quitter():
    global quitter
    quitter = True


if __name__ == '__main__':
    quitter = False
    while quitter is False:
        # fenêtre d'accueil avec questions de config: langue, nombre de joueurs et nom de chaque joueur
        partie_a_charger = ""
        acceuil = Tk()
        acceuil.configure(bg="#445569")
        acceuil.geometry('1200x700+0+0')
        acceuil.title = ("Écran d'accueil")
        acceuil.protocol("WM_DELETE_WINDOW", accueil_close)

        fr_acceuil = Frame(acceuil, bg="#445569")
        fr_acceuil.grid(row=0, column=0, sticky='NW')
        premiere_frame = Frame(fr_acceuil, bg="#445569")
        premiere_frame.grid(row=0, column=0, sticky='N')
        image1 = PhotoImage(file="image_scrabble-ConvertImage.png")
        label_acc = Label(premiere_frame, image=image1, bg="#445569")
        label_acc.grid()

        autre_fr_acceuil = Frame(acceuil, bg="#445569")
        autre_fr_acceuil.grid(row=0, column=1, sticky='NW')
        premiere_frame_autre = Frame(autre_fr_acceuil, bg="#445569")
        premiere_frame_autre.grid(row=0, column=1, sticky='N')
        image2 = PhotoImage(file="regle_du_jeu-ConvertImage.png")
        label_image_jeu = Label(premiere_frame_autre, image=image2, bg="#445569")
        label_image_jeu.grid()

        deuxieme_frame_autre = Frame(autre_fr_acceuil, bg="#445569")
        label_texte_jeu = Label(deuxieme_frame_autre,
                                text="Le jeu de Scrabble est un jeu de réflexion très populaire c'est "
                                     "pourquoi nous vous le \nproposons dans 15 langues différentes."
                                     "\n\nLe but du jeu est d’avoir le plus de points possible pour "
                                     "battre son adversaire. Chaque \njoueur pioche 7 lettres dans le "
                                     "sac (ici, le jeu vous les pioche au hasard) et doit former\nun "
                                     "mot. \n\nSuivant les lettres qu'il utilise, le joueur aura un "
                                     "certain nombre de points. Si en plus\nde ça, il pose son mot "
                                     "sur une case spéciale du plateau, ses points vont augmenter."
                                     "\n\nLes différentes valeurs des cases spéciales du plateau :"
                                     "\n- Case bleu ciel :  Lettre compte double\n- Case bleu foncé :  "
                                     "Lettre compte triple"
                                     "\n- Case rose :  Mot compte double\n- Case rouge :  Mot compte triple"
                                , justify='left', foreground='white', font=("Impact", 13), bg="#445569")
        label_texte_jeu.grid()
        deuxieme_frame_autre.grid(row=1, column=1, sticky='NW')
        # text="Le jeu de Scrabble est un jeu de réflexion très populaire\nc'est pourquoi nous vous le proposons dans 15 langues différentes. \nLe but du jeu est d’avoir le plus de points possible pour battre son adversaire. \nChaque joueur pioche 7 lettres dans le sac (ici, le jeu vous les pioche au hasard) \net doit former un mot. Suivant les lettres qu'il utilise, le joueur aura un certain nombre de points. \nSi en plus de ça, il pose son mot sur une case spéciale du plateau, ses points vont augmenter.")

        deuxieme_frame = Frame(fr_acceuil, bg="#445569")
        deuxieme_frame.grid(row=1, column=0, sticky='N')
        fr_choix = Frame(deuxieme_frame, bg="#445569")
        Label(fr_choix,
              text="Bienvenue / Welcome\n Veuillez choisir le nombre de joueurs ainsi que la langue de jeu.\n",
              bg="#445569", font=("Impact", 15), foreground='white').grid()
        fr_choix.grid(row=1, column=0, sticky='N')
        fr_nb_joueurs = Frame(deuxieme_frame, bg="#445569")
        nb_joueurs = 2

        var = IntVar()
        var.set(4)
        Radiobutton(fr_nb_joueurs, text="2 joueurs", variable=var, value=2, padx=15, font=("Impact", 15),
                    foreground="#445569", bg="white").grid(row=0, column=0)
        Radiobutton(fr_nb_joueurs, text="3 joueurs", variable=var, value=3, padx=15, font=("Impact", 15),
                    foreground="#445569", bg="white").grid(row=0, column=1)
        Radiobutton(fr_nb_joueurs, text="4 joueurs", variable=var, value=4, padx=15, font=("Impact", 15),
                    foreground="#445569", bg="white").grid(row=0, column=2)
        fr_nb_joueurs.grid()
        nb_joueurs = var.get()

        fr_langue = Frame(deuxieme_frame, bg="#445569")
        var_lang = StringVar()
        global index_code_langue
        global langue
        langue_selectionnee = StringVar()
        liste_langues = (' Français', ' Anglais', ' Bulgare', ' Croate', ' Danois', ' Espagnol', ' Estonien', ' Grec',
                         ' Hongrois', ' Islandais', ' Italien', ' Latin', ' Néerlandais', ' Norvégien', ' Portugais')  # modifié
        liste_codes_langues = ('FR', 'AN', 'BU', 'CR', 'DA', 'ES', 'ET', 'GR', 'HO', 'IS','IT', 'LA', 'NE', 'NO','PO')
        langue_choisie = Combobox(fr_langue, textvariable=var_lang, values=liste_langues, state='readonly',
                                  font=("Impact", 15), height=15, foreground="#445569")
        langue_choisie.current(newindex=0)
        Label(fr_langue, text="\n", bg="#445569").grid()
        Label(fr_langue, text="Nous désirons jouer en :  ", foreground='white', font=("Impact", 15), bg="#445569").grid(
            row=1, column=0)
        langue_choisie.grid(row=1, column=1)
        index_code_langue = langue_choisie.current()
        Label(fr_langue, text="\n", bg="#445569").grid()
        fr_langue.grid()

        # bouton valider
        fr_valide = Frame(deuxieme_frame, pady=10, bg="#445569")
        charger = Button(fr_valide, text="Charger une partie existante", command=bouton_charger_partie, padx=10,
                         font=("Impact", 15), bg='white', foreground="#445569")
        charger.grid(row=0, column=0)
        valide = Button(fr_valide, text="Commencer une nouvelle partie!", command=bouton_accueil_commencer, padx=10,
                        font=("Impact", 15), bg='white', foreground="#445569")
        valide.grid(row=0, column=1)
        fr_valide.grid()

        acceuil.mainloop()

        nb_joueurs = var.get()
        langue = var_lang.get()

        index_code_langue = liste_langues.index(langue)
        langue = ('FR', 'AN', 'BU', 'CR', 'DA', 'ES', 'ET', 'GR', 'HO', 'IS', 'IT', 'LA', 'NE', 'NO','PO')[index_code_langue]
        gui = Scrabble(nb_joueurs, langue)
        gui.configure(bg="#445569")  # 6885105
        Scrabble.jouer(gui)
