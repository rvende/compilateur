from arbre import *
from syntax import *

class GenerationCode(object):
    """docstring forGenerationCode."""
    def __init__(self, syntax, semantique):
        self.cpt = 0
        self.loop = []
        self.syntax = syntax
        self.semantique = semantique
        self.fichier = open("genCode", "w")
        self.fichier.write(".start\n")
        self.fichier.write("resn "+str(self.semantique.nbVariable)+"\n")

    def lancementGenerationCode(self, noeud):
        self.genCode(noeud)
        self.fichier.write("dbg\n")
        self.fichier.write("halt\n")
        self.fichier.close()

    def genCode(self, noeud):
        # Constante
        if noeud.type == "noeud_constante":
            self.fichier.write("push "+str(noeud.valeur)+"\n")

        # Opérateur binaire
        if noeud.type in self.syntax.op_binaire.keys():
            self.genCode(noeud.fils[0])
            self.genCode(noeud.fils[1])
            self.fichier.write(self.syntax.op_binaire[noeud.type]+"\n")

        # Opérateur unaire
        if noeud.type in self.syntax.op_unaire.keys():
            self.fichier.write("push 0\n")
            self.genCode(noeud.fils[0])
            self.fichier.write(self.syntax.op_unaire[noeud.type]+"\n")

        # Autre
        if noeud.type == "noeud_puissance":
            raise GenCodeException("Erreur: noeud_puissance non implémenté.")


        if noeud.type == "noeud_affectation":
            self.genCode(noeud.fils[1])
            self.fichier.write("dup\n")
            self.fichier.write("set "+str(noeud.fils[0].slot)+"\n")

        if noeud.type == "noeud_variable":
            self.fichier.write("get "+ str(noeud.slot) +" ;"+noeud.valeur+"\n")

        if noeud.type == "noeud_bloc":
            for i in range(len(noeud.fils)):
                self.genCode(noeud.fils[i])

        if noeud.type == "noeud_expression":
            self.genCode(noeud.fils[0])
            self.fichier.write("drop\n")

        if noeud.type == "noeud_conditionnel":
            self.genCode(noeud.fils[0])
            self.cpt += 1
            memory_false = self.cpt
            self.fichier.write("jumpf l"+str(memory_false)+"\n")
            self.genCode(noeud.fils[1])
            self.cpt += 1
            if len(noeud.fils) > 2: #si il y a un break sur la cond
                self.fichier.write("jump l"+str(self.cpt)+"\n")
            self.fichier.write(".l"+str(memory_false)+"\n")
            if len(noeud.fils) > 2: #si il y a un break sur la cond
                self.genCode(noeud.fils[2])
                self.fichier.write(".l"+str(self.cpt)+"\n")
                # if noeud.fils[2].type == "noeud_break":
                #     self.genCode(noeud.fils[2])
                #     self.fichier.write(".l"+str(memory)+"\n")
                # else:
                #     self.genCode(noeud.fils[2])
                #     self.fichier.write(".l"+str(memory)+"\n")


        if noeud.type == "noeud_break":
            if self.loop != []:
                self.fichier.write("jump l"+str(self.loop[-1][1])+" ;break\n")
            else:
                raise GenCodeException("Erreur: break n'est pas dans une boucle.")

        if noeud.type == "noeud_loop":
            self.cpt += 1
            # stockage des labels de début et fin de loop dans un tuple: (debut,fin)
            self.loop.append((self.cpt,self.cpt+1))
            self.cpt += 1
            current_loop = self.loop[-1]
            self.fichier.write(".l"+str(current_loop[0])+"\n")
            self.genCode(noeud.fils[0])
            self.fichier.write("jump l"+str(current_loop[0])+"\n")
            self.fichier.write(".l"+str(current_loop[1])+"\n")
            self.loop.pop()



class GenCodeException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
