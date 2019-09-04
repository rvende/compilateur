class arbre:

    def __init__(self, type, valeur=0):
        self.type = type
        self.valeur = valeur
        self.fils = []

    def ajouterFils(self, arbre):
        self.fils.append(arbre)

    def afficher(self, niveau = 1):
        res = ""
        for i in range(niveau):
            print("\t")
        print(self.type)
        for elem in self.fils:
            res += elem.afficher(niveau + 1)
        return res
