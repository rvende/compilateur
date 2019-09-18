from lexical import *
from arbre import *

tableauPriorite = {
    'tok_plus' : {'arbre': 'noeud_plus_binaire', 'priorite': 1, 'associativite': 1},
    'tok_moins': {'arbre': 'noeud_moins_binaire', 'priorite': 1, 'associativite': 1},
    'tok_multiplication': {'arbre': 'noeud_multiplication', 'priorite': 2, 'associativite': 1},
    'tok_division': {'arbre': 'noeud_division', 'priorite': 2, 'associativite': 1},
    'tok_modulo': {'arbre': 'noeud_modulo', 'priorite': 2, 'associativite': 1},
    'tok_puissance': {'arbre': 'noeud_puissance', 'priorite': 3, 'associativite': 0},
}

def chercherOp(token):
    return tableauPriorite.get(token['type'],None)

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
    # if(lexical.index_token+1 == len(lexical.les_tokens)):
    #     lexical.index_token = 0
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
    raise SyntaxException("Erreur: Primaire attendu près de "+ lexical.next()['type'] + " l:" + str(lexical.next()['ligne']) + ",c:"+ str(lexical.next()['colonne']))

class SyntaxException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
        
