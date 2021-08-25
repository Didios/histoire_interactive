# programme permettant de créer, écouter et jouer à des histoires intéractives

# fait par Didier Mathias

import tkinter as tk
from tkinter import messagebox
from modules import module_lecture_fichier as read
"""
ajouter un menu d'aide et d'option
"""

def choix(dossier, root = None):
    """
    fonction qui affiche la liste des choix possibles dans un dossier
    parametres:
        dossier, une chaine de caracteres avec le nom du dossier
        root, optionnel, à mentionner si on ne souhaite pas changer de fenetre
    renvoie une fenetre tkinter avec la liste des choix possibles
    """
    liste = read.lister_fichier(dossier)

    if root == None:
        root = tk.Tk()
    else:
        # on nettoie la fenetre
        for c in root.winfo_children():
            c.destroy()

    root.title("Listes des Histoires")
    root.config(bg = "#87CEEB")

    zoneMenu = tk.Frame(root, borderwidth=3, bg='darkblue')
    zoneMenu.grid(row = 0, column = 0, columnspan = len(liste), sticky="NSEW")

    voix = tk.BooleanVar()
    ChoixVoix = tk.Checkbutton(zoneMenu, text='Voix', width='10', borderwidth=2, bg='gray', activebackground='darkorange', relief = "raised",variable = voix, onvalue = True, offvalue = False)
    ChoixVoix.grid(row=0, column=0, sticky="NSEW")

    Ajout = tk.Button(zoneMenu, text = 'Ajout', width='10', borderwidth=2, bg='gray', relief = "raised", command = lambda x=[root, dossier] : ajout(x[0], x[1]))
    Ajout.grid(row=0, column=1, sticky="NSEW")

    """
    ajouter un menu pour changer le font des textes : voir font dans histoire
    changer grid(zoneMenu)
    """

    for i_titre in range(len(liste)):
        # on ouvre un pack.png avec une image a afficher en row 1 column i_titre
        tk.Button(root, height = 5, width = 20, text = liste[i_titre], command = lambda x=[liste[i_titre], voix] : histoire(root, dossier + "/" + x[0], x[1].get())).grid(row = 2, column = i_titre, sticky="NSEW")

    grid(root, 3, len(liste))
    grid(zoneMenu, 1, 2)

    root.mainloop()

def histoire(root, dossier, voix = False):
    """
    fonction qui permet de raconter une histoire au format tkinter
    parametres:
        root, le fenetre tkinter dans laquelle se déroule l'histoire
        dossier, une chaine de caracteres avec le nom du dossier
        voix, optionnel, permet de d'activer la voix synthétique, par défaut False
    """
    root.title(dossier)

    # on nettoie la fenetre
    for c in root.winfo_children():
        c.destroy()

    narration = read.lire_fichier(dossier + "/narration.md")

    def detail_etapes(narration):
        etapes = {}
        i_ligne = 0
        while i_ligne < len(narration):

            if narration[i_ligne][0] == "#":
                numero = narration[i_ligne].split("\r")[0]

                etapes[numero] = []
                i_ligne += 1
                if ":" in narration[i_ligne]:
                    image = narration[i_ligne].split(" : ")[1]
                else:
                    image = ""
                etapes[numero] += [image]
                i_ligne += 1

                texte = ""
                while narration[i_ligne][0] not in ["/", "!"]:
                    texte += narration[i_ligne]
                    i_ligne += 1

                etapes[numero] += [texte]

                choix = []
                while narration[i_ligne][0] != "!":
                    separation = narration[i_ligne][1:].split("/")
                    texte = separation[0]

                    nbr = separation[1].split("\r")[0]
                    choix += [[texte, nbr]]
                    i_ligne += 1

                etapes[numero] += [choix]

            i_ligne += 1
        return etapes

    etapes = detail_etapes(narration)

    i = tk.StringVar()
    i.set("#0")
    forme = [("Comic Sans MS", 15, "bold"), ("Comic Sans MS", 10, "bold")]

    while True:
        nbr = i.get()
        for c in root.winfo_children():
            c.destroy()

        etape = etapes[nbr]
        nbr_column = len(etape[2])

        """
        image en 0-nbr_column 0
        """
        titre = tk.Label(root, text = etape[1], font = forme[0], bg = "#87CEEB")

        if voix:
            parole = ""
            for j in etape[1].split("\r"):
                parole += j + " "
            parler(parole)

            parole_fin = {}
            for j in etape[2]:
                parole_fin[j[1]] = j[0]


        if nbr_column > 0:
            titre.grid(row = 1, column = 0, columnspan = nbr_column, sticky="NSEW")
        else:
            titre.grid(row = 1, column = 0, sticky="NSEW")

        if nbr_column == 0:
            break

        else:
            taille =  "%dp" % (titre.winfo_reqwidth() // nbr_column)
            for i_choix in range(nbr_column):
                tk.Button(root,text = etape[2][i_choix][0], wraplength = taille, font = forme[1], command = lambda x=etape[2][i_choix][1] : i.set(x), bg = "#87CEEB", activebackground = "#87CEEB").grid(row = 2, column = i_choix, sticky="NSEW")

        """
        grid() ne fonctionne pas :
            peut-être taille fenetre : modifier la taille de la fenetre à chaque fois
            grille déjà grande avant : créer une frame le contenu de la fenetre et on le supprime à la place d'enlever chaque élément / changer les zones de création et les suppressions et les grid(root)
        """
        grid(root, 1, nbr_column)

        root.wait_variable(i)
        if voix:
            parole = parole_fin[i.get()]
            parler(parole)

    # FIN
    if voix:
        parler("   FIN")

    tk.Button(root, text = "Fin", font = forme[1], command = lambda x=[dossier, root] : choix(x[0].split("/")[0], x[1]), bg = "#87CEEB", activebackground = "#87CEEB").grid(row = 2, column = 0, sticky="NSEW")

def ajout(root, dossier):
    """
    fonction permettant d'ajouter une histoire
    parametres:
        root, une fenetre tkinter
    """
    def plus():
        """
        sous-fonction qui permet d'ajouter un morceau à l'histoire
        """
        lettres = caracteres(texte.get("1.0", "end"))

        dif_choix = [i.split("/") for i in choice.get("1.0", "end").split("\n")][:-1]
        faire = []
        good = True
        if not fin.get():
            for i in dif_choix:
                if len(i) != 2: # trouver pour éviter qu'il n'y ait pas de reference
                    good = False

        if numero.get() == "":
            messagebox.showerror("Erreur numéro", "Mauvais numéro")
            """
            si checkbox image, vérifier qu'une image a été mise
            """
        elif len(lettres) < 2 and (" " in lettres or "\n" in lettres):
            messagebox.showerror("Erreur texte", "Il faut un texte")
        elif not good:
            messagebox.showerror("Erreur choix", 'Un choix par ligne avec le choix et le numero séparés par "/"')
        elif numero.get() in etapes.keys():
            if messagebox.askyesno("Changement", "Voulez-vous modifier ce numéro ?"):
                etapes[numero.get()] = [texte.get("1.0", "end"), choice.get("1.0", "end")]
        else:
            tk.Button(schema, text=numero.get(), command = lambda x="%s" % numero.get() : restaurer(x, etapes[x][0], etapes[x][1])).grid(row=ligne.get(), column=0, sticky="NSEW")
            grid(schema,ligne.get() ,0)
            ligne.set(ligne.get() + 1)
            if fin.get():
                etapes[numero.get()] = [texte.get("1.0", "end"), False]
            else:
                etapes[numero.get()] = [texte.get("1.0", "end"), choice.get("1.0", "end")]
            """
            si image, la mettre en 3
            """

    def restaurer(N, T, C):
        """
        sous-fonction qui permet d'afficher un morceau dans la fenetre
        parametres:
            N, la référence
            T, le texte
            C, les choix
        """
        numero.set(N)
        texte.delete("1.0", "end")
        if C == False:
            choice.configure(state = "normal")
            choice.delete("1.0", "end")
            choice.configure(state = "disabled")
            fin.set(True)
            f.select()
        else:
            fin.set(False)
            f.deselect()
            choice.configure(state = "normal")
            choice.delete("1.0", "end")
            choice.insert("1.0", C)

        texte.insert("1.0", T)
        """
        restaurez image
        """

    def valider():
        """
        sous-fonction qui permet de construire le dossier qui contiendrat l'histoire
        """
        if not "0" in etapes.keys():
            messagebox.showerror("Pas de début", "Il manque le début d'indice 0")
            """
            vérifier si tous peut fonctionner :
                les references dites existe dans etapes sinon erreur
                les images sont ouvrables
                # il y a une fin
            """
        else:
            titre = str(input("Quel est le titre de votre histoire ?"))
            while read.fichier_existe(dossier + "/" + titre):
                titre = str(input("Ce titre existe déjà, choissisez-en un autre."))
            """
            demander image de l'histoire
            """
            chemin = dossier + "/" + titre
            read.add_repertoire(dossier, titre)

            read.add_repertoire(chemin, "images")

            """
            mettres les images enregistrées
            """

            # changer etapes en 1 fichier
            narration = ""

            for reference, contenu in etapes.items():
                narration += "#" + reference + "\r"
                narration += "False"
                """
                remplacer "False" par "image" si checkbox image
                """
                for L in contenu[0].split("\n"):
                    if L != "":
                        narration += "\r" + L

                if contenu[1] != False:
                    for C in [i.split("/") for i in contenu[1].split("\n")][:-1]:
                        if C != ['']:
                            narration += "\r/ " + C[0] + " /#" + C[1]

                narration += "\r!\r\r"

            read.add_fichier(chemin, "narration.md", narration)
            choix(dossier.split("/")[0], root)

    def vue():
        if fin.get():
            choice.configure(state = "normal")
            fin.set(False)
        else:
            choice.configure(state = "disabled")
            fin.set(True)


    etapes = {}
    root.title("Ajout")

    # on nettoie la fenetre
    for c in root.winfo_children():
        c.destroy()

    """
    schema visuel a  implementer
    schema sous forme de Canvas
    """
    schema = tk.Frame(root, bg = "#87CEEB", borderwidth=3)
    ligne = tk.IntVar()
    ligne.set(0)

    schema.grid(row = 0, rowspan = 6, column = 1, sticky='NSEW')

    # numero
    tk.Label(root, text = "Numéro :", bg = "#87CEEB").grid(row = 0, column = 0, sticky="w")
    numero = tk.StringVar()
    tk.Entry(root, textvariable = numero, width = 40).grid(row = 1, column = 0, sticky='NSEW')

    """
    mettre checkbox image
    si cocher, il faut ouvrir une image
    sinon case désactiver

    on ouvre l'image avec un ouvrir puis on parcours les fichiers
    """

    # texte
    label_texte = tk.Label(root, text = "Texte :", bg = "#87CEEB").grid(row = 2, column = 0, sticky="w")
    texte = tk.Text(root, height = 10, width = 30)
    texte.grid(row = 3, column = 0, sticky='NSEW')

    # choix
    fin = tk.BooleanVar()
    fin.set(False)
    f = tk.Checkbutton(root, text='Choix possible :', width='10', borderwidth=2, bg='#87CEEB', command = lambda x=fin : vue())
    f.grid(row=4, column=0, sticky="w")

    tk.Label(root, text="texte_choix / reference", bg = "#87CEEB").grid(row = 4, column = 0, sticky="e")

    choice = tk.Text(root, height = 10, width = 30)
    choice.grid(row = 5, column = 0, sticky='NSEW')

    # plus
    tk.Button(root, text="+", bg = "#87CEEB", command=plus).grid(row=6, column=0, sticky="NSEW")

    # validation
    tk.Button(root, text="Valider", bg = "#87CEEB", command=valider).grid(row=6, column=1, sticky="NSEW")

    grid(root, 6, 2)
    root.minsize(width=700, height=600)

def grid(root, R, C):
    for i in range(R):
        root.grid_rowconfigure(i, weight=1)
    for i in range(C):
        root.grid_columnconfigure(i, weight=1)

def parler(texte):
    """
    fonction permettant de dire un texte --> Text-to-Speech
    parametres:
        texte, une chaine de caracteres à dire
    """
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # mettre rate à 150 permet d'avoir un débit raisonnable

    engine.say(texte)
    engine.runAndWait()

def caracteres(texte):
    """
    fonction permettant d'obtenir une liste de tous les caracteres distinct présent dans une chaine de caracteres
    parametres:
        texte, une chaine de caracteres
    renvoie une liste de caracteres
    """
    lettres = []

    for caractere in texte:
        if caractere not in lettres:
            lettres += [caractere]

    return lettres


if __name__ == '__main__':
    choix("histoires")