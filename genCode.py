from arbre import *
from syntax import *

def lancementGenerationCode(arbre, syntax, semantique):
    fichier = open("genCode", "w")
    fichier.write(".start\n")
    fichier.write("resn "+str(semantique.nbVariable)+"\n")
    genCode(arbre, fichier, syntax)
    fichier.write("dbg\n")
    fichier.write("halt\n")
    fichier.close()

cpt = 0
def genCode(noeud, fichier, syntax):
    # Constante
    if noeud.type == "noeud_constante":
        fichier.write("push "+str(noeud.valeur)+"\n")

    # Opérateur binaire
    if noeud.type in syntax.op_binaire.keys():
        genCode(noeud.fils[0], fichier, syntax)
        genCode(noeud.fils[1], fichier, syntax)
        fichier.write(syntax.op_binaire[noeud.type]+"\n")

    # Opérateur unaire
    if noeud.type in syntax.op_unaire.keys():
        fichier.write("push 0\n")
        genCode(noeud.fils[0], fichier, syntax)
        fichier.write(syntax.op_unaire[noeud.type]+"\n")

    # Autre
    if noeud.type == "noeud_puissance":
        raise GenCodeException("Erreur: noeud_puissance non implémenté.")

    if noeud.type == "noeud_affectation":
        genCode(noeud.fils[1], fichier, syntax)
        fichier.write("dup\n")
        fichier.write("set "+str(noeud.fils[0].slot)+"\n")

    if noeud.type == "noeud_variable":
        fichier.write("get "+ str(noeud.slot) +" ;"+noeud.valeur+"\n")

    if noeud.type == "noeud_bloc":
        for i in range(len(noeud.fils)):
            genCode(noeud.fils[i], fichier, syntax)

    if noeud.type == "noeud_expression":
        genCode(noeud.fils[0], fichier, syntax)
        fichier.write("drop\n")

    if noeud.type == "noeud_conditionnel":
        global cpt
        genCode(noeud.fils[0], fichier, syntax)
        cpt += 1
        fichier.write("jumpf l"+str(cpt)+"\n")
        genCode(noeud.fils[1], fichier, syntax)
        cpt += 1
        print("Here: "+str(len(noeud.fils)))
        if len(noeud.fils) > 2:
            fichier.write("jump l"+str(cpt)+"\n")
        fichier.write(".l"+str(cpt-1)+"\n")
        if len(noeud.fils) > 2:
            genCode(noeud.fils[2], fichier, syntax)
            fichier.write(".l"+str(cpt)+"\n")


class GenCodeException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
