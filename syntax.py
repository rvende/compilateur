from lexical import *
from arbre import *

tableauPriorite = {
    'tok_affectation': {'arbre': 'noeud_affectation', 'priorite': 0, 'associativite': 0},
    'tok_different': {'arbre': 'noeud_different', 'priorite': 1, 'associativite': 1},
    'tok_inferieur': {'arbre': 'noeud_inferieur', 'priorite': 1, 'associativite': 1},
    'tok_superieur': {'arbre': 'noeud_superieur', 'priorite': 1, 'associativite': 1},
    'tok_inferieur_egal': {'arbre': 'noeud_inferieur_egal', 'priorite': 1, 'associativite': 1},
    'tok_superieur_egal': {'arbre': 'noeud_superieur_egal', 'priorite': 1, 'associativite': 1},
    'tok_egal': {'arbre': 'noeud_egal', 'priorite': 1, 'associativite': 1},
    'tok_plus' : {'arbre': 'noeud_plus_binaire', 'priorite': 2, 'associativite': 1},
    'tok_moins': {'arbre': 'noeud_moins_binaire', 'priorite': 2, 'associativite': 1},
    'tok_multiplication': {'arbre': 'noeud_multiplication', 'priorite': 3, 'associativite': 1},
    'tok_division': {'arbre': 'noeud_division', 'priorite': 3, 'associativite': 1},
    'tok_modulo': {'arbre': 'noeud_modulo', 'priorite': 3, 'associativite': 1},
    'tok_puissance': {'arbre': 'noeud_puissance', 'priorite': 4, 'associativite': 0}
}

op_unaire = {
    'noeud_moins_unaire': 'sub',
    'noeud_plus_unaire': 'add'
}

op_binaire = {
    'noeud_plus_binaire': 'add',
    'noeud_moins_binaire': 'sub',
    'noeud_multiplication': 'mul',
    'noeud_division': 'div',
    'noeud_modulo': 'mod',
    'noeud_different': 'cmpne',
    'noeud_inferieur': 'cmplt',
    'noeud_superieur': 'cmpgt',
    'noeud_inferieur_egal': 'cmple',
    'noeud_superieur_egal': 'cmpge',
    'noeud_egal': 'cmpeq'
}

def chercherOp(token):
    return tableauPriorite.get(token['type'],None)

def instruction(lexical):
    if lexical.next()['type'] == "tok_if":
        lexical.skip()
        lexical.accept("tok_parenthese_ouvrante")
        Ntest = expression(0,lexical)
        lexical.accept("tok_parenthese_fermante")
        AcodeV = instruction(lexical)
        A = arbre("noeud_conditionnel")
        A.ajouterFils(Ntest)
        A.ajouterFils(AcodeV)
        if lexical.next()['type'] == "tok_else":
            lexical.accept("tok_else")
            AcodeF = instruction(lexical)
            A.ajouterFils(AcodeF)

    elif lexical.next()['type'] == "tok_accolade_ouvrante":
        lexical.accept("tok_accolade_ouvrante")
        A = arbre("noeud_bloc")
        while(lexical.next()['type'] != "tok_accolade_fermante"):
            x = instruction(lexical)
            A.ajouterFils(x)
        lexical.accept("tok_accolade_fermante")
    else:
        E = expression(0,lexical)
        lexical.accept("tok_point_virgule")
        A = arbre("noeud_expression")
        A.ajouterFils(E)
    return A

def expression(p, lexical):
    A1 = primaire(lexical)
    while True:
        op = chercherOp(lexical.next())
        if op is None or op['priorite'] < p:
            return A1
        lexical.skip()
        A2 = expression(op['priorite'] + op['associativite'], lexical)
        A = arbre(op['arbre'])
        A.ajouterFils(A1)
        A.ajouterFils(A2)
        A1 = A


def primaire(lexical):
    if(lexical.next() is None):
        lexical.skip()
    if(lexical.next()['type'] == "tok_constante"):
        A = arbre('noeud_constante', lexical.next()['valeur'])
        lexical.skip()
        return A
    if(lexical.next()['type'] == "tok_parenthese_ouvrante"):
        lexical.skip()
        A = expression(0, lexical)
        lexical.accept("tok_parenthese_fermante")
        return A
    #Opération unaire
    if(lexical.next()['type'] == "tok_moins"):
        lexical.skip()
        A = arbre("noeud_moins_unaire")
        A.ajouterFils(expression(tableauPriorite['tok_puissance']['priorite'], lexical))
        return A
    if(lexical.next()['type'] == "tok_plus"):
        lexical.skip()
        A = arbre("noeud_plus_unaire")
        A.ajouterFils(expression(tableauPriorite['tok_puissance']['priorite'], lexical))
        return A
    if(lexical.next()['type'] == "tok_identificateur"):
        A = arbre("noeud_variable", lexical.next()['name'])
        lexical.skip()
        return A
    #raise SyntaxException("Erreur: Primaire attendu près de "+ lexical.next()['type'] + " l:" + str(lexical.next()['ligne']) + ",c:"+ str(lexical.next()['colonne']))

def lancementGenerationCode(arbre):
    fichier = open("genCode", "w")
    fichier.write(".start\n")
    fichier.write("resn 1\n")
    genCode(arbre, fichier)
    fichier.write("dbg\n")
    fichier.write("halt\n")
    fichier.close()

cpt = 0
def genCode(noeud, fichier):
    # Constante
    if noeud.type == "noeud_constante":
        fichier.write("push "+str(noeud.valeur)+"\n")

    # Opérateur binaire
    if noeud.type in op_binaire.keys():
        genCode(noeud.fils[0], fichier)
        genCode(noeud.fils[1], fichier)
        fichier.write(op_binaire[noeud.type]+"\n")

    # Opérateur unaire
    if noeud.type in op_unaire.keys():
        fichier.write("push 0\n")
        genCode(noeud.fils[0], fichier)
        fichier.write(op_unaire[noeud.type]+"\n")

    # Autre
    if noeud.type == "noeud_puissance":
        raise GenCodeException("Erreur: noeud_puissance non implémenté.")

    if noeud.type == "noeud_affectation":
        genCode(noeud.fils[1], fichier)
        fichier.write("dup\n")
        fichier.write("set 0\n")

    if noeud.type == "noeud_variable":
        fichier.write("get 0\n")

    if noeud.type == "noeud_bloc":
        for i in range(len(noeud.fils)):
            genCode(noeud.fils[i], fichier)

    if noeud.type == "noeud_expression":
        genCode(noeud.fils[0], fichier)
        fichier.write("drop\n")

    if noeud.type == "noeud_conditionnel":
        global cpt
        genCode(noeud.fils[0], fichier)
        cpt += 1
        fichier.write("jumpf l"+str(cpt)+"\n")
        genCode(noeud.fils[1], fichier)
        cpt += 1
        print("Here: "+str(len(noeud.fils)))
        if len(noeud.fils) > 2:
            fichier.write("jump l"+str(cpt)+"\n")
        fichier.write(".l"+str(cpt-1)+"\n")
        if len(noeud.fils) > 2:
            genCode(noeud.fils[2], fichier)
            fichier.write(".l"+str(cpt)+"\n")

class GenCodeException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)


class SyntaxException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
