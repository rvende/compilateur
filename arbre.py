class arbre:

    def __init__(self, type, valeur=0):
        self.type = type
        self.valeur = valeur
        self.fils = []

    def ajouterFils(self, arbre):
        self.fils.append(arbre)

    def afficher(self, niveau = 0):
        for i in range(niveau):
            print("\t", end = '')
        print(self.type + ": " + str(self.valeur))
        for elem in self.fils:
            elem.afficher(niveau + 1)
