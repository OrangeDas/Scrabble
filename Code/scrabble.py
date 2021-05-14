import pickle
from random import randint, shuffle
from joueur import Joueur
from plateau import Plateau, Jeton, Chevalet
from tkinter import Tk, Toplevel, filedialog, NSEW, N, E, W, Frame, Label, Entry, PhotoImage, Radiobutton, IntVar, StringVar, Button, messagebox
from tkinter.ttk import Combobox


class jetons_sur_plateau(Exception):
    def __init__(self, texte_action):
        messagebox.showinfo(title="Wait a minute...", message="At least one tocken is on the board, please resume before {}".format(texte_action) )


class mots_non_valides(Exception):
    def __init__(self):
        messagebox.showinfo(title="OUPSSS Bad shot !", message="At least one of the words formed is missing from the dictionary.\n\nTry again")


class positions_non_valides(Exception):
    def __init__(self, nombre_jeton):
        if nombre_jeton == 1:
            messagebox.showinfo(title="Will have to start again...", message="Your letter is wrongly positioned. ")
        else:
            messagebox.showinfo(title="Will have to start again...", message="Your letters are badly positioned. They must be on a single line or column and form only one word on this line or column. The first word must cover the central star.")


class Sauvegarde():
    """
    Class containing all the elements of a game to save it and load it later to resume a game.
    """

    def __init__(self, nb_joueurs, nb_joueurs_restants, cases, jetons_libres, joueurs, joueur_actif, mots_au_plateau, langue):
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
    Scrabble class that also implements part of the game logic.
    The attributes of a scrabble are:
    - dictionnaire: set, contains all the words that can be played on in this part.
    Basically to know if a word is allowed we will look in the dictionary.
    - plateau: The board is an item of the Trap class, where tackens are placed and it tells us the number of points won.
    - jetons_libres: Token list, the list of all the tockens in the bag, this is where each player can take tokens when he needs them.
    - joueurs: Player list, All players of the game.
    - joueur_actif: Player, the player who is playing the current turn. If no player then None.
    """

    
    def __init__(self, nb_joueurs, langue):
        """ 
        Given a number of players and a language. The builder creates a scrabble game.
        For a new scrabble game,
        - a new board object is created;
        - The list of players is created and each player is automatically named  Player 1, Player 2, ...
        JPlayer n where n is the number of players;
        - The joueur_actif is None.
        :param nb_joueurs: int, number of players in the game at least 2 at most 4.
        :param langue: str, FR for the French language, and EN for the English language. Depending on the language,
        you must open, read, load in memory the file "dictionnaire_francais.txt" or "dictionnaire_anglais.txt"
        Then it will be necessary to extract the words contained to build a set with the set keyword.
        Also, thanks to the language you must be able to create all the starting chips and put them in jetons_libres.
        To find out how many tokens created for each language you can look at:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
        *** In our scrabble, we will not use wildcards that do not contain any letters, so do not include them in free tokens ***
        :exception: Raise an exception with assert if the language is not fr, FR, en, or EN or if nb_joueur < 2 or > 4.
        """

        super().__init__( )

        if partie_a_charger == "":
            self.joueurs = [Joueur(("Player {}".format(i + 1))) for i in range(nb_joueurs)]
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
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 15, 1), ('A', 9, 1), ('I', 8, 1), ('N', 6, 1), ('O', 6, 1),
                    ('R', 6, 1), ('S', 6, 1), ('T', 6, 1), ('U', 6, 1), ('L', 5, 1),
                    ('D', 3, 2), ('M', 3, 2), ('G', 2, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 8), ('K', 1, 10), ('W', 1, 10), ('X', 1, 10), ('Y', 1, 10),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_francais.txt'
            
        # DICTIONAIRE ANGLAIS
        elif self.langue.upper() == 'AN':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('N', 6, 1), ('O', 8, 1),
                    ('R', 6, 1), ('S', 4, 1), ('T', 6, 1), ('U', 4, 1), ('L', 4, 1),
                    ('D', 4, 2), ('M', 2, 3), ('G', 3, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 10), ('K', 1, 5), ('W', 2, 4), ('X', 1, 8), ('Y', 2, 4),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_anglais.txt'
            
        # DICTIONAIRE ESPAGNOL
        elif self.langue.upper() == 'ES':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 12, 1), ('E', 12, 1), ('O', 9, 1), ('I', 6, 1), ('S', 6, 1),
                    ('N', 5, 1), ('R', 5, 1), ('U', 5, 1), ('L', 4, 1), ('T', 4, 1),
                    ('D', 5, 2), ('G', 2, 2), ('C', 4, 3), ('B', 2, 3), ('M', 2, 3),
                    ('P', 2, 3), ('H', 2, 4), ('F', 1, 4), ('V', 1, 4), ('Y', 1, 4),
                    ('CH', 1, 5), ('Q', 1, 5), ('J', 1, 8), ('LL', 1, 8), ('Ñ', 1, 8),
                    ('RR', 1, 8), ('X', 1, 8), ('Z', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_espagnol.txt'
            
        # DICTIONAIRE ITALIEN
        elif self.langue.upper() == 'IT':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('O', 15, 1), ('A', 14, 1), ('I', 12, 1), ('E', 11, 1), ('C', 6, 2),
                    ('R', 6, 2), ('S', 6, 2), ('T', 6, 2), ('L', 5, 3), ('M', 5, 3),
                    ('N', 5, 3), ('U', 5, 3), ('B', 3, 5), ('D', 3, 5), ('F', 3, 5),
                    ('P', 3, 5), ('V', 3, 5), ('G', 2, 8), ('H', 2, 8), ('Z', 2, 8),
                    ('Q', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_italien.txt'
            
        # DICTIONAIRE NORVEGIEN
        elif self.langue.upper() == 'NO':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 9, 1), ('A', 7, 1), ('N', 6, 1), ('R', 6, 1), ('S', 6, 1),
                    ('T', 6, 1), ('D', 5, 1), ('I', 5, 1), ('L', 5, 1), ('F', 4, 2),
                    ('G', 4, 2), ('K', 4, 2), ('O', 4, 2), ('M', 3, 2), ('H', 3, 3),
                    ('B', 3, 4), ('U', 3, 4), ('V', 3, 4), ('J', 2, 4), ('P', 2, 4),
                    ('Å', 2, 4), ('Ø', 2, 5), ('Y', 1, 6), ('Æ', 1, 6), ('W', 1, 8),
                    ('C', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_norvegien.txt'
            
        # DICTIONAIRE NÉERLANDAIS
        elif self.langue.upper() == 'NE':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 18, 1), ('N', 10, 1), ('A', 6, 1), ('O', 6, 1), ('I', 4, 1),
                    ('D', 5, 2), ('R', 5, 2), ('T', 5, 2), ('S', 4, 2), ('G', 3, 3),
                    ('K', 3, 3), ('L', 3, 3), ('M', 3, 3), ('B', 2, 3), ('P', 2, 3),
                    ('U', 3, 4), ('H', 2, 4), ('J', 2, 4), ('V', 2, 4), ('Z', 2, 4),
                    ('IJ', 2, 4), ('F', 1, 4), ('C', 2, 5), ('W', 2, 5), ('X', 1, 8),
                    ('Y', 1, 8), ('Q', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_neerlandais.txt'
            
        # DICTIONAIRE DANOIS
        elif self.langue.upper() == 'DA':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 9, 1), ('A', 7, 1), ('N', 6, 1), ('R', 6, 1), ('D', 5, 2),
                    ('L', 5, 2), ('O', 5, 2), ('S', 5, 2), ('T', 5, 2), ('B', 4, 3),
                    ('I', 4, 3), ('K', 4, 3), ('F', 3, 3), ('G', 3, 3), ('M', 3, 3),
                    ('U', 3, 3), ('V', 3, 3), ('H', 2, 4), ('J', 2, 4), ('P', 2, 4),
                    ('Y', 2, 4), ('Æ', 2, 4), ('Ø', 2, 4), ('Å', 2, 4), ('C', 2, 8),
                    ('X', 1, 8), ('Z', 1, 8)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_danois.txt'
        # DICTIONNAIRE BULGARE
        elif self.langue.upper() == 'BU':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 9, 1), ('O', 9, 1), ('E', 8, 1), ('И', 8, 1), ('T', 5, 1),
                    ('H', 4, 1), ('П', 4, 1), ('P', 4, 1), ('C', 4, 1), ('B', 4, 2),
                    ('M', 4, 2), ('Б', 3, 2), ('Д', 3, 2), ('К', 3, 2), ('Л', 3, 2),
                    ('Г', 3, 3), ('Ъ', 2, 3), ('Ж', 2, 4), ('З', 2, 4), ('У', 3, 5),
                    ('Ч', 2, 5), ('Я', 2, 5), ('Й', 1, 5), ('X', 1, 5), ('Ц', 1, 8),
                    ('Ш', 1, 8), ('Ю', 1, 8), ('Ф', 1, 10), ('Щ', 1, 10), ('Ь', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_bulgare.txt'
            
        # DICTIONNAIRE ESTONIEN
        elif self.langue.upper() == 'ET':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 10, 1), ('E', 9, 1), ('I', 9, 1), ('S', 8, 1), ('T', 7, 1),
                    ('K', 5, 1), ('L', 5, 1), ('O', 5, 1), ('U', 5, 1), ('D', 4, 2),
                    ('M', 4, 2), ('N', 4, 2), ('R', 2, 2), ('G', 2, 3), ('V', 2, 3),
                    ('B', 1, 4), ('H', 2, 4), ('J', 2, 4), ('Õ', 2, 4), ('P', 2, 4),
                    ('Ä', 2, 5), (' Ü', 2, 5), ('Ö', 2, 6), ('F', 1, 8), ('Š', 1, 10),
                    ('Z', 1, 10), ('Ž', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_estonien.txt'
        # DICTIONNAIRE GREC
        elif self.langue.upper() == 'GR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 12, 1), ('E', 8, 1), ('I', 8, 1), ('T', 7, 1), ('H', 7, 1),
                    ('Σ', 7, 1), ('N', 6, 1), ('O', 6, 1), ('K', 4, 2), ('Π', 4, 2),
                    ('P', 5, 2), ('Y', 4, 2), ('Λ', 3, 3), ('M', 3, 3), ('Ω', 3, 3),
                    ('Γ', 2, 4), ('Δ', 2, 4), ('B', 1, 8), ('Φ', 1, 8), ('X', 1, 8),
                    ('Z', 1, 10), ('Θ', 1, 10), ('Ξ', 1, 10), ('Ψ', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_grec.txt'
            
        # DICTIONNAIRE CROATE
        elif self.langue.upper() == 'CR':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 11, 1), ('I', 10, 1), ('E', 9, 1), ('O', 9, 1), ('N', 6, 1),
                    ('R', 5, 1), ('S', 5, 1), ('T', 5, 1), ('J', 4, 1), ('U', 4, 1),
                    ('K', 3, 2), ('M', 3, 2), ('P', 3, 2), ('V', 3, 2), ('D', 3, 3),
                    ('G', 2, 3), ('L', 2, 3), ('Z', 2, 3), ('B', 1, 3), ('Č', 1, 3),
                    ('C', 1, 4), ('H', 1, 4), ('LJ', 1, 4), ('NJ', 1, 4), ('Š', 1, 4),
                    ('Ž', 1, 4), ('Ć', 1, 5), ('F', 1, 8), ('DŽ', 1, 10), ('Đ', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_croate.txt'
            
        # DICTIONNAIRE HONGROIS
        elif self.langue.upper() == 'HO':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 6, 1), ('E', 6, 1), ('K', 6, 1), ('T', 5, 1), ('Á', 4, 1),
                    ('L', 4, 1), ('N', 4, 1), ('R', 4, 1), ('I', 3, 1), ('M', 3, 1),
                    ('O', 3, 1), ('S', 3, 1), ('B', 2, 3), ('D', 2, 3), ('G', 2, 3),
                    ('Ó', 2, 3), ('É', 3, 3), ('H', 2, 3), ('SZ', 2, 3), ('V', 2, 3),
                    ('F', 2, 4), ('GY', 2, 4), ('J', 2, 4), ('Ö ', 2, 4), ('P', 2, 4),
                    ('U', 2, 4), ('Ü', 2, 4), ('Z', 2, 4), ('C', 1, 5), ('Í', 1, 5),
                    ('NY', 1, 5), ('CS', 1, 7), ('Ő', 1, 7), ('Ú', 1, 7), ('Ű', 1, 7),
                    ('LY', 1, 8), ('ZS', 1, 8), ('TY', 1, 10), ]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_hongrois.txt'
            
        # DICTIONNAIRE LATIN
        elif self.langue.upper() == 'LA':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('V', 9, 2), ('S', 8, 1),
                    ('T', 8, 1), ('R', 7, 1), ('O', 5, 1), ('C', 4, 2), ('M', 4, 2),
                    ('N', 4, 2), ('D', 3, 2), ('L', 3, 2), ('Q', 3, 3), ('B', 2, 4),
                    ('G', 2, 4), ('P', 2, 4), ('X', 2, 4), ('F', 1, 8), ('H', 1, 8)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_latin.txt'
            
        # DICTIONNAIRE ISLANDAIS
        elif self.langue.upper() == 'IS':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 10, 1), ('I', 8, 1), ('N', 8, 1), ('R', 7, 1), ('E', 6, 1),
                    ('S', 6, 1), ('U', 6, 1), ('T', 5, 1), ('Ð', 5, 2), ('G', 4, 2),
                    ('K', 3, 2), ('L', 3, 2), ('M', 3, 2), ('F', 3, 3), ('O', 3, 3),
                    ('H', 2, 3), ('V', 2, 3), ('Á', 2, 4), ('D', 2, 4), ('Í ', 2, 4),
                    ('Þ', 1, 4), ('J', 1, 5), ('Æ', 1, 5), ('B', 1, 6), ('É ', 1, 6),
                    ('Ó', 1, 6), ('Ö ', 1, 7), ('Y', 1, 7), ('P', 1, 8), ('Ú ', 1, 8),
                    ('Ý', 1, 9), ('X', 1, 10)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_islandais.txt'
        # DICTIONAIRE PORTUGAIS ok
        elif langue.upper() == 'PO':
            # Information available on https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('A', 14, 1), ('I', 10, 1), ('O', 10, 1), ('S', 8, 1), ('U', 7, 1),
                    ('M', 6, 1), ('R', 6, 1), ('E', 5, 1), ('T', 5, 1), ('C', 4, 2),
                    ('P', 4, 2), ('D', 5, 2), ('L', 5, 2), ('N', 4, 3), ('B', 3, 3),
                    ('Ç', 2, 3), ('F', 2, 4), ('G', 2, 4), ('H', 2, 4), ('V', 2, 4),
                    ('J', 2, 5), ('Q', 1, 6), ('X', 1, 8), ('Z', 1, 8)]
            nom_fichier_dictionnaire = '../Dictionnaire/dictionnaire_portugais.txt'

        if partie_a_charger == "":
            self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for i in range(occurences)]
        else:
            self.jetons_libres = self.donnees_de_partie.jetons_libres
            self.liste_codes_position_a_valider = []

        with open(nom_fichier_dictionnaire, 'r', encoding="utf8") as f:
            self.dictionnaire = set([x[:-1].upper() for x in f.readlines() if len(x[:-1]) > 1])

        self.position_jeton_selectionne = None
        self.title("Scrabble: Isabelle Eysseric and Roger Gaudreault")
        self.geometry("1x1+0+0")

        if partie_a_charger == "":
            # Form to have the name and choice of image of the player before drawing the interface
            self.form_joueurs = Toplevel(self)
            self.form_joueurs.title("Who wants to play ?")
            self.form_joueurs.configure(bg="#445569")
            self.form_joueurs.geometry("500x700+200+0")

            fr_intro_joueur = Frame(self.form_joueurs, bg="#445569")
            fr_intro_joueur.grid(row=0, column=0)
            label_intro_joueur = Label(fr_intro_joueur, text="Each player must enter their name", padx=50, pady=50, font=("Impact", 20), bg="#445569", foreground='white')
            label_intro_joueur.grid(row=0, column=0)

            image_equipe = Frame(self.form_joueurs,  bg = "#445569")
            image_equipe.grid(row=1, column=0)
            image3 = PhotoImage(file= "../Images/equipe.png")
            label_image_equipe = Label(image_equipe, image = image3,  bg = "#445569")
            label_image_equipe.grid()

            fr_entry_joueur = Frame(self.form_joueurs, bg="#445569")
            fr_entry_joueur.grid(row=2, column=0)
            Label(fr_entry_joueur, text="Joueur 1 :", pady=10, font=("Helvetica", 15), bg='#445569', foreground='white').grid(row=0, column=0, sticky=W)
            Label(fr_entry_joueur, text="Joueur 2 :", pady=10, font=("Helvetica", 15), bg='#445569', foreground='white').grid(row=1, column=0, sticky=W)
            
            self.form_joueurs.jo1 = StringVar()
            self.form_joueurs.jo2 = StringVar()
            self.form_joueurs.jo1.set("Player 1")
            self.form_joueurs.jo2.set("Player 2")

            Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo1, bg='#FDF4C9', font=('courier new', 10, 'italic'), foreground='#445569').grid(row=0, column=1, sticky=E)
            Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo2, bg='#FDF4C9', font=('courier new', 10, 'italic'), foreground='#445569').grid(row=1, column=1, sticky=E)

            if self.nb_joueurs >= 3:
                Label(fr_entry_joueur, text="Joueur 3 :", pady=10, font=("Helvetica", 15), bg='#445569', foreground='white').grid(row=2, column=0, sticky=W)
                self.form_joueurs.jo3 = StringVar()
                self.form_joueurs.jo3.set("Joueur 3")
                Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo3, bg='#FDF4C9', font=('courier new', 10, 'italic'), foreground='#445569').grid(row=2, column=1, sticky=E)
            
            if self.nb_joueurs == 4:
                Label(fr_entry_joueur, text="Joueur 4 :", pady=10, font=("Helvetica", 15), bg='#445569', foreground='white').grid(row=3, column=0, sticky=W)
                self.form_joueurs.jo4 = StringVar()
                self.form_joueurs.jo4.set("Joueur 4")
                Entry(fr_entry_joueur, textvariable=self.form_joueurs.jo4, bg='#FDF4C9', font=('courier new', 10, 'italic'), foreground='#445569').grid(row=3, column=1, sticky=E)
            
            bouton_valider_joueurs = Button(self.form_joueurs, text="We are ready to start", command=self.comm_bouton_valider_joueurs, font=('Impact', 15), bg='#FDF4C9', foreground="#445569").grid(row=10, column=0, pady=10)
            self.wait_window(self.form_joueurs)

        self.geometry(str(int(self.winfo_screenwidth() * 0.95)) + "x" + str(int(self.winfo_screenheight()) - 100) + "+0+0")
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

        Label(self, text='OUR SUPER TRAY OF SCRABBLE', font='Impact', bg='#FDF4C9').grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        Label(self, text='THE PLAYERS', font='Impact', bg='#FDF4C9').grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        # FRAME NEXT TO THE BOARD:
        self.frame_a_cote_plateau = Frame(self, bg="#445569", bd=20, width=(Plateau.PIXELS_PAR_CASE * Plateau.DIMENSION), height=Plateau.PIXELS_PAR_CASE * Plateau.DIMENSION)
        self.frame_a_cote_plateau.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

        # FRAME FOR PLAYERS:
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
        self.label_joueur_actif = Label(self.fr_label_joueur_actif, textvariable=self.text_label_joueur_actif, foreground='white', bg='#445569', font=("Helvetica", 20))
        self.label_joueur_actif.grid(row=0, column=0)
        self.width_button = 16

        # FRAME IN BESIDE THE TRAY WITH THE BOX:
        la_boite = Frame(self.frame_a_cote_plateau, bg='#445569')
        la_boite.grid(row=4, column=0, padx=10, pady=10)
        
        button_changer_lettres = Button(la_boite, text='Exchanging letters', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_changer_lettres.grid(row=0, column=0, padx=10, pady=10)
        button_changer_lettres.bind("<Button-1>", self.call_changer_lettres)

        button_melanger = Button(la_boite, text='Mix my tockens', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_melanger.grid(row=0, column=1, padx=10, pady=10)
        button_melanger.bind("<Button-1>", self.call_melanger_jetons)

        button_passer = Button(la_boite, text='Pass my turn', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_passer.grid(row=0, column=2, padx=10, pady=10)
        button_passer.bind("<Button-1>", self.call_joueur_suivant)

        button_valider = Button(la_boite, text='Validate my turn', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_valider.grid(row=1, column=0, padx=10, pady=10)
        button_valider.bind("<Button-1>", self.call_valider_tour)

        button_reprise_jetons = Button(la_boite, text='Take back my tockens', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_reprise_jetons.grid(row=1, column=1, padx=10, pady=10)
        button_reprise_jetons.bind("<Button-1>", self.call_reprendre_jetons)

        button_nouvelle_partie = Button(la_boite, text='New part', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_nouvelle_partie.grid(row=1, column=2, padx=10, pady=10)
        button_nouvelle_partie.bind("<Button-1>", self.call_nouvelle_partie)

        button_enregistrer_partie = Button(la_boite, text='Save part', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_enregistrer_partie.grid(row=2, column=0, padx=10, pady=10)
        button_enregistrer_partie.bind("<Button-1>", self.call_sauvegarde)

        button_liste_mot = Button(la_boite, text='Words from the board', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_liste_mot.grid(row=2, column=1, padx=10, pady=10)
        button_liste_mot.bind("<Button-1>", self.call_liste_mots_au_plateau)

        button_abandonner = Button(la_boite, text='To abandon', font='Impact', width=self.width_button, bg='#FDF4C9', foreground="#445569")
        button_abandonner.grid(row=2, column=2, padx=10, pady=10)
        button_abandonner.bind("<Button-1>", self.call_joueur_abandonne)

        if partie_a_charger == "":
            self.joueur_suivant()
        else:
            self.joueur_actif = self.donnees_de_partie.joueur_actif
            self.plateau.dessiner_plateau()
            for i in range(self.nb_joueurs_restants):
                self.joueur_suivant()
            messagebox.showinfo(title="You're back !", message="Let's continue the part where we left it...")   
            
        self.protocol("WM_DELETE_WINDOW", self.demande_sauvegarde_avant_quitter)

        
    def demande_sauvegarde_avant_quitter(self):
        x = messagebox.askyesnocancel(title="The window wants to close...", message="Do you want to save the game before leaving ?" )
        if x is True:
            self.sauvegarde()
        if x is False:
            self.destroy()
        if x is None:
            pass

        
    def call_nouvelle_partie(self, event):
        x = messagebox.askyesnocancel(title="Start from scratch...", message="A new game will start with the same players.\n\nDo you want to save the game before leaving ?" )
        if x is True:
            self.sauvegarde_sans_quitter()
        if x is True or x is False:
            self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for i in range(occurences)]
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
            messagebox.showinfo("It starts again...", message="The new game will begin.\n\nGood luck !")
            self.joueur_actif = None
            self.joueur_suivant()
            messagebox.showinfo(title="It's chance that decides ...", message="The first player will be: {}.".format(self.joueur_actif.nom))
            self.mots_au_plateau = []

            
    def redimensionner(self, event):
        self.largeur_app = event.width

        
    def call_sauvegarde(self, event):
        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("back up.")
        else:
            self.sauvegarde()

            
    def sauvegarde(self):
        partie = Sauvegarde(self.nb_joueurs, self.nb_joueurs_restants, self.plateau.cases, self.jetons_libres, self.joueurs, self.joueur_actif, self.mots_au_plateau, self.langue)
        valide = False
        while not valide:
            nom_fichier = filedialog.asksaveasfilename()
            with open(nom_fichier, "wb") as f:
                pickle.dump(partie, f)
            valide = True
            continuer = messagebox.askyesno(title="Saved game....", message="The game is saved, do you want to keep playing ?")
            if continuer is False:
                messagebox._show(title="He left!", message="Goodbye!")
                self.destroy()

                
    def sauvegarde_sans_quitter(self):
        partie = Sauvegarde(self.nb_joueurs, self.nb_joueurs_restants, self.plateau.cases, self.jetons_libres, self.joueurs, self.joueur_actif, self.mots_au_plateau, self.langue)
        valide = False
        while not valide:
            nom_fichier = filedialog.asksaveasfilename()
            with open(nom_fichier, "wb") as f:
                pickle.dump(partie, f)
            valide = True
            messagebox.showinfo(
                title="The game is saved"
            )

                                
    def dessiner_joueurs(self):                               
        if self.joueur_actif == self.joueurs[0]:
            joueur1 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red", highlightthickness=10)
        else:
            joueur1 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9", highlightthickness=10)
        
        joueur1.grid(row=1, column=0, padx=10, pady=10)
        self.label_score_joueur1 = Label(joueur1, text="Score: {}".format(self.joueurs[0].points), font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
        self.label_score_joueur1.grid(row=3, column=0)
        self.label_nom1 = Label(joueur1, text=self.joueurs[0].nom, font=("Impact", 20), bg='#FDF4C9', width=21)
        self.label_nom1.grid(row=0, column=0, sticky=N)
        chevalet1 = Frame(joueur1)
        chevalet1.grid(row=4, column=0)

        # Frame in Players with Player 1:
        if self.joueurs[0].a_abandonne is True:
            self.abandonne1 = PhotoImage(file='../Images/abandonne.png')
            self.abandonne1_label1 = Label(chevalet1, image=self.abandonne1, bg='#FDF4C9')
            self.abandonne1_label1.grid(row=1, column=0, sticky=NSEW)
        else:
            self.label_lettre1_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(0)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre1_joueur1.grid(row=0, column=0)
            self.label_lettre2_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(1)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre2_joueur1.grid(row=0, column=1)
            self.label_lettre3_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(2)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre3_joueur1.grid(row=0, column=2)
            self.label_lettre4_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(3)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre4_joueur1.grid(row=0, column=3)
            self.label_lettre5_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(4)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre5_joueur1.grid(row=0, column=4)
            self.label_lettre6_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(5)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre6_joueur1.grid(row=0, column=5)
            self.label_lettre7_joueur1 = Label(chevalet1, text="{}".format(self.joueurs[0].obtenir_jeton(6)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre7_joueur1.grid(row=0, column=6)

        # Frame in Players with Player 2:
        if self.joueur_actif == self.joueurs[1]:
            joueur2 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",highlightthickness=10)
        else:
            joueur2 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",highlightthickness=10)
        
        joueur2.grid(row=1, column=1, padx=10, pady=10)
        self.label_score_joueur2 = Label(joueur2, text="Score: {}".format(self.joueurs[1].points),font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
        self.label_score_joueur2.grid(row=3, column=0)
        self.label_nom2 = Label(joueur2, text=self.joueurs[1].nom, font=("Impact", 20), bg='#FDF4C9')
        self.label_nom2.grid(row=0, column=0, sticky=N)
        chevalet2 = Frame(joueur2)
        chevalet2.grid(row=4, column=0)

        if self.joueurs[1].a_abandonne is True:
            self.abandonne2 = PhotoImage(file='../Images/abandonne.png')
            self.abandonne2_label1 = Label(chevalet2, image=self.abandonne2, bg='#FDF4C9')
            self.abandonne2_label1.grid(row=1, column=0, sticky=NSEW)
        else:
            self.label_lettre1_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(0)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre1_joueur2.grid(row=0, column=0)
            self.label_lettre2_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(1)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre2_joueur2.grid(row=0, column=1)
            self.label_lettre3_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(2)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre3_joueur2.grid(row=0, column=2)
            self.label_lettre4_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(3)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre4_joueur2.grid(row=0, column=3)
            self.label_lettre5_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(4)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre5_joueur2.grid(row=0, column=4)
            self.label_lettre6_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(5)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre6_joueur2.grid(row=0, column=5)
            self.label_lettre7_joueur2 = Label(chevalet2, text="{}".format(self.joueurs[1].obtenir_jeton(6)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
            self.label_lettre7_joueur2.grid(row=0, column=6)

        # Frame in Players with Player 3:
        if nb_joueurs >= 3:
            if self.joueur_actif == self.joueurs[2]:
                joueur3 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",highlightthickness=10)
            else:
                joueur3 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",highlightthickness=10)
            
            joueur3.grid(row=2, column=0, padx=10, pady=10)
            self.label_score_joueur3 = Label(joueur3, text="Score: {}".format(self.joueurs[2].points),font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
            self.label_score_joueur3.grid(row=3, column=0)
            self.label_nom3 = Label(joueur3, text=self.joueurs[2].nom, font=("Impact", 20), bg='#FDF4C9')
            self.label_nom3.grid(row=0, column=0, sticky=N)
            chevalet3 = Frame(joueur3)
            chevalet3.grid(row=4, column=0)

            if self.joueurs[2].a_abandonne is True:
                self.abandonne3 = PhotoImage(file='../Images/abandonne.png')
                self.abandonne3_label1 = Label(chevalet3, image=self.abandonne3, bg='#FDF4C9')
                self.abandonne3_label1.grid(row=1, column=0, sticky=NSEW)
            else:
                self.label_lettre1_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(0)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre1_joueur3.grid(row=0, column=0)
                self.label_lettre2_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(1)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre2_joueur3.grid(row=0, column=1)
                self.label_lettre3_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(2)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre3_joueur3.grid(row=0, column=2)
                self.label_lettre4_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(3)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre4_joueur3.grid(row=0, column=3)
                self.label_lettre5_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(4)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre5_joueur3.grid(row=0, column=4)
                self.label_lettre6_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(5)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre6_joueur3.grid(row=0, column=5)
                self.label_lettre7_joueur3 = Label(chevalet3, text="{}".format(self.joueurs[2].obtenir_jeton(6)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre7_joueur3.grid(row=0, column=6)

        # Frame in Players with Player 4:
        if nb_joueurs == 4:
            if self.joueur_actif == self.joueurs[3]:
                joueur4 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="red", highlightcolor="red",highlightthickness=10)
            else:
                joueur4 = Frame(self.mes_joueurs, bg='#FDF4C9', highlightbackground="#FDF4C9", highlightcolor="#FDF4C9",highlightthickness=10)
            
            joueur4.grid(row=2, column=1, padx=10, pady=10)
            self.label_score_joueur4 = Label(joueur4, text="Score: {}".format(self.joueurs[3].points),font=("Helvetica", 16), bg='#FDF4C9', width=23)  # sticky=NE
            self.label_score_joueur4.grid(row=3, column=0)
            self.label_nom4 = Label(joueur4, text=self.joueurs[3].nom, font=("Impact", 20), bg='#FDF4C9')
            self.label_nom4.grid(row=0, column=0, sticky=N)
            chevalet4 = Frame(joueur4)
            chevalet4.grid(row=4, column=0)

            if self.joueurs[3].a_abandonne is True:
                self.abandonne4 = PhotoImage(file='../Images/abandonne.png')
                self.abandonne4_label1 = Label(chevalet4, image=self.abandonne4, bg='#FDF4C9')
                self.abandonne4_label1.grid(row=1, column=0, sticky=NSEW)
            else:
                self.label_lettre1_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(0)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre1_joueur4.grid(row=0, column=0)
                self.label_lettre2_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(1)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre2_joueur4.grid(row=0, column=1)
                self.label_lettre3_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(2)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre3_joueur4.grid(row=0, column=2)
                self.label_lettre4_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(3)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre4_joueur4.grid(row=0, column=3)
                self.label_lettre5_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(4)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre5_joueur4.grid(row=0, column=4)
                self.label_lettre6_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(5)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
                self.label_lettre6_joueur4.grid(row=0, column=5)
                self.label_lettre7_joueur4 = Label(chevalet4, text="{}".format(self.joueurs[3].obtenir_jeton(6)),font=("Helvetica", 16), bg='#FDF4C9')  # sticky=NE
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
            raise jetons_sur_plateau("to give up the game.")
        else:
            self.confirmation_abandon = False
            if messagebox.askyesno(title="It's getting too complicated ?",message="{}, Do you really want to give up ?".format(self.joueur_actif.nom)):
                self.joueur_actif.a_abandonne = True
                self.nb_joueurs_restants -= 1
                self.joueur_suivant()
                if self.partie_terminee():
                    messagebox.showinfo(title="Oh! As we had fun!", message="Game over !\n\n{} Won the game because he is the only remaining player.\n\n He wins with a score of {} points.\n\n".format(self.joueur_actif.nom, self.joueur_actif.points))
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
            messagebox.showinfo(title="Rien ne se passe...", message="At least one letter must be placed in order to validate.")
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
                    messagebox.showinfo(title="Good shot!", message="Well done {}\n\nWord(s) formed(s):\n{}".format(self.joueur_actif.nom, "\n".join(mots) + "\nScore obtained:" + str(score)) )
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
            Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne)
        self.liste_lettre_a_valider = []
        self.liste_codes_position_a_valider = []

                                
    def call_joueur_suivant(self, event):
        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("to pass your turn !")
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
        str = """The words on the board are:\n{}""".format("\n".join(self.mots_au_plateau))
        messagebox.showinfo(title="In a word, here are the words", message=str)

                                
    def call_changer_lettres(self, event):
        if self.liste_codes_position_a_valider != []:
            raise jetons_sur_plateau("to change letters.")
        else:
            self.liste_positions_lettres_a_changer = []
            # Prevent clicking root while toplevel is open
            self.form_changer_lettres = Toplevel(self)
            self.form_changer_lettres.grab_set()
            self.form_changer_lettres.title("Exchange the letters")
            self.form_changer_lettres.configure(bg="#445569")
            fr_intro = Frame(self.form_changer_lettres)
            fr_intro.grid(row=0, column=0)  
            label_intro = Label(fr_intro, text="Please select in blue the letters you wish to exchange then press OK.\n\n Your letters will be changed, but you will lose your turn", padx=50, pady=20, foreground='white', bg='#445569', font=("Helvetica", 20))                             
            label_intro.grid(row=0, column=0)
            fr_chevalet = Frame(self.form_changer_lettres)
            fr_chevalet.grid(row=1, column=0)
            self.chevalet = Chevalet(self.form_changer_lettres)
            self.chevalet.grid(row=2, column=0, padx=50, pady=20)
                                
            for i in range(Chevalet.DIMENSION):
                Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne )
            
            self.chevalet.bind("<Button-1>", self.gerer_click_jeton_chevalet_a_changer)         
            self.form_changer_lettres.protocol("WM_DELETE_WINDOW", self.form_changer_lettres_close)           
            self.valider_change_lettres = Button(self.form_changer_lettres, text='Exchange the letters', font='Impact',width=self.width_button, bg='#FDF4C9', foreground="#445569")
            self.valider_change_lettres.grid(padx=10, pady=20)
            self.valider_change_lettres.bind("<Button-1>", self.call_valider_change_lettres)           
            self.annule_change_lettres = Button(self.form_changer_lettres, text='Cancel, I do not want to lose my turn', font='Impact', width=50, bg='#FDF4C9', foreground="#445569")
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
                Chevalet.dessiner_jeton_chevalet(self.chevalet,self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne)
            else:
                Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i), i, i)

                                
    def form_changer_lettres_close(self):
        self.form_changer_lettres.destroy()

                                
    def affiche_chevalet_joueur_actif(self):
        self.chevalet.delete(self)
        self.chevalet = Chevalet(self.frame_a_cote_plateau)
        self.chevalet.grid(row=1, column=0)
        for i in range(Chevalet.DIMENSION):
            Chevalet.dessiner_jeton_chevalet(self.chevalet,self.joueur_actif.obtenir_jeton(i), i, self.position_jeton_selectionne)
        if len(self.jetons_libres) == 0:
            messagebox.showinfo( title="Game over!", message="All the tockens have been distributed, the game is now over.\n\nThe winning player is {0} with {1} points.\n\nCongratulations {0}!!\n\nThe program will now close, goodbye!".format(self.determiner_gagnant().nom, self.determiner_gagnant().points) )
            global quitter
            quitter = True
            self.destroy()
        self.chevalet.bind("<Button-1>", self.gerer_click_jeton_chevalet)

                                
    def mot_permis(self, mot):
        """
        Lets know if a word is allowed in the game or not by looking in the dictionary.
        :param mot: str, word to check.
        :return: bool, if the word is in the dictionary, False otherwise.
        """
        
        # return True if word is in the dict, False otherwise ...
        # upper because the read converts the dictionary to upper
        return mot.upper() in self.dictionnaire

                                
    def determiner_gagnant(self):
        """
        Determine the winning player, if there is one. To determine if a player is the winner,
        he must have the highest score of all.
        :return: Player, one of the winning players, i.e if several are tied we take one at random.
        """
        
        # We return the last element of the list of players sorted in ascending order according to 
        # the number of points of the players
        return sorted(self.joueurs, key=lambda joueur: joueur.points)[-1]

                                
    def partie_terminee(self):
        """
        Check if the game is over. A game is over if there are no more free chips or there are 
        less than two (2) players left. This is the rule we have chosen to use for this job, 
        so try to neglect others you know or have read on the Internet.
        Returns:
            bool: True if the game is over, and False otherwise.
        """
        
        return self.jetons_libres == [] or self.nb_joueurs_restants == 1

                                
    def joueur_suivant(self):
        """
        Change the active player.
        The new active player is the one at the index of (current player + 1)% nb_joueurs.
        The new active player is the one at the index of (current player + 1)%
        """
        
        # Players are re-evaluated in case one of the original players leaves
        self.nb_joueurs = len(self.joueurs)

        # A random player is determined if no active player
        if self.joueur_actif is None:
            self.joueur_actif = self.joueurs[randint(0, nb_joueurs - 1)]

        # We move on to the next
        index_courant = self.joueurs.index(self.joueur_actif)
        self.joueur_actif = self.joueurs[(index_courant + 1) % self.nb_joueurs]
        self.text_label_joueur_actif.set("{}, it's your turn to play.".format(self.joueur_actif.nom))
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
        Simulates the draw of n tokens of the coin bag and returns them.
        It's a question of randomly taking tokens in self.jetons_libres and returning them.
         Remember to use the shuffle function of the random module.
        :param n: the number of tokens to shoot.
        :return: Token list, the list of chips drawn.
        :exception: raise an exception with assert if n does not respect the condition 0 <= n <= 7.
        """
                                
        assert 0 <= n <= 7, "The number of tokens to draw is invalid"
        shuffle(self.jetons_libres)                     # We mix the tokens
        jeton_liste = self.jetons_libres[:n]            # We create a list of tokens we draw
        self.jetons_libres = self.jetons_libres[n:]     # Free tokens now exclude those drawn
        return jeton_liste                              # We return the list of tockens drawn

                                
    def jouer_un_tour(self):
        """ 
        Play one of the players around until he places a valid word on the board.
        To do this
        1 - Show the board then the player;
        2 - Ask for positions to play;
        3 - Remove the chips from the bridge;
        4 - Validate if the positions are valid for an addition on the board;
        5 - If yes, place the tocken on the board, otherwise go back to 1;
        6 - If all the words formed are in the dictionary, then add the points to the active player;
        7 - Otherwise remove the tockens from the board and put them back on the player's bridge, then start again at 1;
        8 - Show the board.
        :return: Do not return anything.
        """

        self.chevalet = Chevalet(self.frame_a_cote_plateau)
        self.chevalet.grid(row=1, column=0)
        for i in range(Chevalet.DIMENSION):
            Chevalet.dessiner_jeton_chevalet(self.chevalet, self.joueur_actif.obtenir_jeton(i),i)
        self.update()
        valide = False

                                
    def changer_jetons(self, pos_chevalet):
        """
        Have the active player change his tockens.The method must ask the player to enter 
        positions to change one after the other separated by a space.
        If a position is invalid (use Joueur.position_est_valide) then ask again.
        As soon as all valid positions remove them from the player's bridge and give him again.
        Finally, tockens are given at the player's place among the free tockens.
        :return: Do not return anything.
        """

        liste_jetons_retires = []
        # A list of drawn tokens is created, a number equal to the list of entered positions.
        liste_jetons_tires = self.tirer_jetons(len(pos_chevalet))

        # Remove the token, (None position in the bridge) add this token to the removed token list. 
        # The first element of the list of tokens drawn is added to the bridge and this token is 
        # removed from this list.
        for i in pos_chevalet:
            liste_jetons_retires.append(self.joueur_actif.retirer_jeton(i))
            self.joueur_actif.ajouter_jeton(liste_jetons_tires[0])
            liste_jetons_tires = liste_jetons_tires[1:]

        # We return the removed tokens in the list of free tokens
        self.jetons_libres = self.jetons_libres + liste_jetons_retires

                                
    def jouer(self):
        """
        This function allows you to play the game.
        As long as the game is not over, we play a trick.
        At each turn:
            - We change the active player and we show him it's his turn. eg Player 2's turn.
            - We show him his options so that he chooses what to do:
              "Enter (j) to play, (p) to pass your turn, (c) to change some chips, (s) to save or (q) to quit"
            Note that if the player just saves you must not move to the next player but in all other cases 
            you must move to the next player. If he leaves the game, he is removed from the list of players.
        Once the game is over, congratulate the winning player!
        :return Do not return anything!
        """
                                
        abandon = False
        changer_joueur = False
        while not self.partie_terminee() and not abandon:
            if partie_a_charger == "":
                self.joueur_suivant()
                messagebox.showinfo(title="It's chance that decides...", message="The first player will be: {}.".format(self.joueur_actif.nom))
            self.plateau.dessiner_plateau()
            self.wait_window()  # Prevent clicking root while messagebox is open

                                
    @staticmethod
    def charger_partie(nom_fichier):
        """
        Static method to create a scrabble object by reading the file in which the object was previously saved. 
        Remember to use the load function of the pickle module.
        :param nom_fichier: The name of the file that contains a scrabble object.
        :return: Scrabble, the object loaded into memory.
        """
                                
        with open(nom_fichier, "rb") as f:
            objet = pickle.load(f)
        return objet


def accueil_close():
    if (messagebox.askyesno(title="Are you leaving so soon ?", message="Are you sure you want to leave the game ?")):
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
                                
        # Home window with config questions: language, number of players and name of each player.
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
        image1 = PhotoImage(file="../Images/image_scrabble-ConvertImage.png")
        label_acc = Label(premiere_frame, image=image1, bg="#445569")
        label_acc.grid()
        autre_fr_acceuil = Frame(acceuil, bg="#445569")
        autre_fr_acceuil.grid(row=0, column=1, sticky='NW')                              
        premiere_frame_autre = Frame(autre_fr_acceuil, bg="#445569")
        premiere_frame_autre.grid(row=0, column=1, sticky='N')                             
        image2 = PhotoImage(file="../Images/regle_du_jeu-ConvertImage.png")
        label_image_jeu = Label(premiere_frame_autre, image=image2, bg="#445569")
        label_image_jeu.grid()
        deuxieme_frame_autre = Frame(autre_fr_acceuil, bg="#445569")
                                
        label_texte_jeu = Label(deuxieme_frame_autre,
                                text="The game of Scrabble is a very popular puzzle game that's why we put it to you\n" 
                                     "in 15 different languages.\n"
                                     "\nThe goal of the game is to have as many points as possible to beat his opponent.\n"
                                     "\nEach player draws 7 letters in the bag (here, the game draws them at random) and\n"
                                     "must form a word.\n"
                                     "\nDepending on the letters he uses, the player will have a certain number of points.\n"
                                     "If on top of that, he puts his word on a special box of the board, his points will\n"
                                     "increase.\n"
                                     "The different values of the special boxes on the board:\n"
                                     "- Sky Blue Case: Double Count Letter\n"
                                     "- Dark blue case: Letter count triple\n"
                                     "- Pink Case: Word Count Double\n"
                                     "- Red box: Word count triple"
                                , justify='left', foreground='white', font=("Impact", 13), bg="#445569")
        label_texte_jeu.grid()
                                
        deuxieme_frame_autre.grid(row=1, column=1, sticky='NW')
        # text="The game of Scrabble is a very popular puzzle game that's why we offer it in 15 different languages."
        #       "The goal of the game is to have as many points as possible to beat his opponent.\n"
        #       "Each player draws 7 letters in the bag (here, the game draws them at random) and must form a word.\n" 
        #       "Depending on the letters he uses, the player will have a certain number of points.\n"
        #       "If on top of that, he puts his word on a special box of the board, his points will increase.")"
        deuxieme_frame = Frame(fr_acceuil, bg="#445569")
        deuxieme_frame.grid(row=1, column=0, sticky='N')
                                
        fr_choix = Frame(deuxieme_frame, bg="#445569")
        Label(fr_choix,text="Welcome / Bienvenue\n Please choose the number of players and the language of play.\n", bg="#445569", font=("Impact", 15), foreground='white').grid()
        fr_choix.grid(row=1, column=0, sticky='N')
        fr_nb_joueurs = Frame(deuxieme_frame, bg="#445569")
        nb_joueurs = 2
                                
        var = IntVar()
        var.set(4)
        Radiobutton(fr_nb_joueurs, text="2 joueurs", variable=var, value=2, padx=15, font=("Impact", 15),foreground="#445569", bg="white").grid(row=0, column=0)
        Radiobutton(fr_nb_joueurs, text="3 joueurs", variable=var, value=3, padx=15, font=("Impact", 15),foreground="#445569", bg="white").grid(row=0, column=1)
        Radiobutton(fr_nb_joueurs, text="4 joueurs", variable=var, value=4, padx=15, font=("Impact", 15),foreground="#445569", bg="white").grid(row=0, column=2)
        fr_nb_joueurs.grid()
        nb_joueurs = var.get()

        fr_langue = Frame(deuxieme_frame, bg="#445569")
        var_lang = StringVar()
        global index_code_langue
        global langue
        langue_selectionnee = StringVar()
        liste_langues = (' French', ' English', ' Bulgarian', ' Croatian', ' Danish', ' Spanish', ' Estonian', ' Greek',
                         ' Hungarian', ' Icelandic', ' Italian', ' Latin', ' Dutch', ' Norwegian', ' Portuguese')  # edit
        liste_codes_langues = ('FR', 'AN', 'BU', 'CR', 'DA', 'ES', 'ET', 'GR', 'HO', 'IS','IT', 'LA', 'NE', 'NO','PO')
        langue_choisie = Combobox(fr_langue, textvariable=var_lang, values=liste_langues, state='readonly',font=("Impact", 15), height=15, foreground="#445569")
        langue_choisie.current(newindex=0)
        Label(fr_langue, text="\n", bg="#445569").grid()
        Label(fr_langue, text="We want to play: ", foreground='white', font=("Impact", 15), bg="#445569").grid(row=1, column=0)
        langue_choisie.grid(row=1, column=1)
        index_code_langue = langue_choisie.current()
        Label(fr_langue, text="\n", bg="#445569").grid()
        fr_langue.grid()

        # bouton valider
        fr_valide = Frame(deuxieme_frame, pady=10, bg="#445569")
        charger = Button(fr_valide, text="Load an existing part", command=bouton_charger_partie, padx=10,font=("Impact", 15), bg='white', foreground="#445569")
        charger.grid(row=0, column=0)
        valide = Button(fr_valide, text="Start a new game !", command=bouton_accueil_commencer, padx=10,font=("Impact", 15), bg='white', foreground="#445569")
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
