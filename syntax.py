from lexical import *
from arbre import *



class Syntax(object):
    """docstring forSyntax."""
    def __init__(self, lexical):
        self.tableauPriorite = {
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
        self.op_unaire = {
            'noeud_moins_unaire': 'sub',
            'noeud_plus_unaire': 'add'
        }
        self.op_binaire = {
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
        self.lexical = lexical

    def chercherOp(self, token):
        return self.tableauPriorite.get(token['type'],None)

    def instruction(self):
        if self.lexical.next()['type'] == "tok_if":
            self.lexical.skip()
            self.lexical.accept("tok_parenthese_ouvrante")
            Ntest = self.expression(0)
            self.lexical.accept("tok_parenthese_fermante")
            AcodeV = self.instruction()
            A = arbre("noeud_conditionnel")
            A.ajouterFils(Ntest)
            A.ajouterFils(AcodeV)
            if self.lexical.next()['type'] == "tok_else":
                self.lexical.accept("tok_else")
                AcodeF = self.instruction()
                A.ajouterFils(AcodeF)
        elif self.lexical.next()['type'] == "tok_var":
            self.lexical.accept("tok_var")
            A = arbre("noeud_declaration",self.lexical.next()['name'])
            self.lexical.skip()
            self.lexical.accept("tok_point_virgule")

        elif self.lexical.next()['type'] == "tok_accolade_ouvrante":
            self.lexical.accept("tok_accolade_ouvrante")
            A = arbre("noeud_bloc")
            while(self.lexical.next()['type'] != "tok_accolade_fermante"):
                x = self.instruction()
                A.ajouterFils(x)
            self.lexical.accept("tok_accolade_fermante")
        else:
            E = self.expression(0)
            self.lexical.accept("tok_point_virgule")
            A = arbre("noeud_expression")
            A.ajouterFils(E)
        return A

    def expression(self, p):
        A1 = self.primaire()
        while True:
            op = self.chercherOp(self.lexical.next())
            if op is None or op['priorite'] < p:
                return A1
            self.lexical.skip()
            A2 = self.expression(op['priorite'] + op['associativite'])
            A = arbre(op['arbre'])
            A.ajouterFils(A1)
            A.ajouterFils(A2)
            A1 = A


    def primaire(self):
        if(self.lexical.next() is None):
            self.lexical.skip()
        if(self.lexical.next()['type'] == "tok_constante"):
            A = arbre('noeud_constante', self.lexical.next()['valeur'])
            self.lexical.skip()
            return A
        if(self.lexical.next()['type'] == "tok_parenthese_ouvrante"):
            self.lexical.skip()
            A = self.expression(0)
            self.lexical.accept("tok_parenthese_fermante")
            return A
        #Opération unaire
        if(self.lexical.next()['type'] == "tok_moins"):
            self.lexical.skip()
            A = arbre("noeud_moins_unaire")
            A.ajouterFils(self.expression(self.tableauPriorite['tok_puissance']['priorite']))
            return A
        if(self.lexical.next()['type'] == "tok_plus"):
            self.lexical.skip()
            A = arbre("noeud_plus_unaire")
            A.ajouterFils(self.expression(self.tableauPriorite['tok_puissance']['priorite']))
            return A
        if(self.lexical.next()['type'] == "tok_identificateur"):
            A = arbre("noeud_variable", self.lexical.next()['name'])
            self.lexical.skip()
            return A

class SyntaxException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        super().__init__(message)
