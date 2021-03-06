class arbre:

    def __init__(self, type, valeur=0, slot=0,args=0):
        """
        Contructeur
        attribut: type: C'est le nom du noeud
                  valeur:  C'est la valeur associé à une constante (0 par défaut)
        """
        self.type = type
        self.valeur = valeur
        self.fils = []
        self.slot = slot
        self.nargs = args

    def ajouterFils(self, arbre):
        """
        Permet d'ajouter une feuille à un arbre.
        Paramètre: arbre de type Arbre
        """
        self.fils.append(arbre)

    def afficher(self, niveau = 0):
        """
        Permet d'afficher dans le terminal l'arbre.
        """
        for i in range(niveau):
            print("\t", end = '')
        print(self.type + ": " + str(self.valeur))
        for elem in self.fils:
            elem.afficher(niveau + 1)

    def toString(self, niveau = 0):
        """
        Permet d'afficher les informations d'un objet arbre.
        """
        res = ""
        for i in range(niveau):
            res += "\t"
        res += self.type + ": " + str(self.valeur) + "\n"
        for elem in self.fils:
            res += elem.toString(niveau + 1)
        return res
