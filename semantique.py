from arbre import *


class Analyse_semantique(object):
    """docstring forAnalyse_semantique."""
    def __init__(self):
        self.nbVariable = 0
        self.pile = []

    def debut_bloc(self):
        self.pile.append({})

    def fin_bloc(self):
        self.pile.pop()

    def declarer(self,nom_ident):
        if nom_ident in self.pile[-1].keys():
            raise RedefinedException("Erreur: Variable déjà déclarée")
        else:
            self.pile[-1][nom_ident] = {"id": nom_ident}
            return self.pile[-1][nom_ident]

    def chercher(self,nom_ident):
        i = -1
        taille = -len(self.pile)
        while(i >= taille):
            if nom_ident in self.pile[i].keys():
                return self.pile[i].get(nom_ident)
            else:
                i -= 1
        raise UndefinedException("Erreur: Variable non déclarée")

    def analyse(self, noeud):
        print(noeud.type)
        if noeud.type == "noeud_bloc":
            self.debut_bloc()
            for enfant in noeud.fils:
                self.analyse(enfant)
            self.fin_bloc()
        elif noeud.type == "noeud_declaration":
            S = self.declarer(noeud.valeur)
            S['type'] = "variable"
            S['slot'] = self.nbVariable
            self.nbVariable += 1
        elif noeud.type == "noeud_variable":
            S = self.chercher(noeud.valeur)
            if(S['type'] != "variable"):
                raise UnexpectedException("Erreur: Variable atttendu")
            noeud.slot = S.slot
            print("HEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEE"+str(S.slot))

class RedefinedException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)

class UndefinedException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)

class UnexpectedException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
