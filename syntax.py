from lexical import *
from arbre import *

def expression(p):
    pass

def primaire(lexical):
    print(lexical.next())
    lexical.index_token = 0
    if(lexical.next() is None):
        lexical.skip()
    if(lexical.next()['type'] == "tok_constante"):
        A = arbre('noeud_constante', lexical.next()['valeur'])
        lexical.skip()
        return A
    if(lexical.next()['type'] == "tok_parenthese_ouvrante"):
        lexical.skip()
        A = expression(0)
        lexical.accept("tok_parenthese_fermante")
        return A
    #Opération unaire
    if(lexical.next()['type'] == "tok_moins"):
        lexical.skip()
        A = arbre("noeud_moins_unaire")
        #A.ajouterFils(expression(7))
        return A
    print("Erreur: Primaire attendu")
