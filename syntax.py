from lexical import *
from arbre import *

def expression(p):
    pass
    
def primaire():
    if(next() is None):
        skip()
    if(next()['type'] == "tok_constante"):
        A = arbre('noeud_constante', next()['valeur'])
        skip()
        return A
    if(next()['type'] == "tok_parenthese_ouvrante"):
        skip()
        #A = expression(0)
        accept("tok_parenthese_fermante")
    #Opération unaire
    if(next()['type'] == "tok_moins"):
        skip()
        A = arbre("noeud_moins_unaire")
        #A.ajouterFils(expression(7))
        return A
    print("Erreur: Primaire attendu")

if __name__ == "__main__":
    pass
        
        