import sys

from syntax import *

class lexical():
    
    def __init__(self, fichier):
        self.fichier = open(fichier,"r")
        self.les_tokens = []
        self.mot_cles = {"if":"tok_if","for":"tok_for","int":"tok_int"}
        self.content = self.fichier.read()
        print(self.content)
        print("taille :"+str(len(self.content)))
        self.index_token = -1
        self.num_lettre = 0
        self.num_lig = 1

    def next(self):
        if(self.index_token == len(self.les_tokens)):
            self.index_token = 0
        if self.index_token != -1:
            return self.les_tokens[self.index_token]
        else:
            return None

    def skip(self):
        if(self.index_token == len(self.les_tokens)):
            self.index_token = 0
        else:
            self.index_token = self.index_token + 1

    def accept(self, t):
        if(self.next()['type'] == t):
            self.skip()
        else:
            print("Erreur")

    def main(self):
        while(True):
            if self.next() != None:
                if self.next()['type'] == "tok_EOF":
                    break
            if self.num_lettre < len(self.content):
                if self.content[self.num_lettre] != " " and self.content[self.num_lettre] != "\n":
                    self.tokens(self.content[self.num_lettre])
                    self.skip()
                else:
                    if self.content[self.num_lettre] == "\n":
                        self.num_lig += 1
                        self.num_lettre += 1
                    else:
                        self.num_lettre += 1
            else:
                self.num_lettre += 1


    def tokens(self, c):
        if c == "+":
            self.les_tokens.append({'type':'tok_plus', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "-":
            self.les_tokens.append({'type':'tok_moins', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "*":
            self.les_tokens.append({'type':'tok_multiplication', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "/":
            self.les_tokens.append({'type':'tok_division', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "%":
            self.les_tokens.append({'type':'tok_modulo', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "^":
            self.les_tokens.append({'type':'tok_puissance', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "!":
            if self.content[self.num_lettre+1] == "=":
                self.les_tokens.append({'type':'tok_different', "ligne": self.num_lig})
                self.num_lettre += 2
        elif c == "<":
            if self.content[self.num_lettre+1] == "=":
                self.les_tokens.append({'type':'tok_inferieur_egal', "ligne": self.num_lig})
                self.num_lettre += 2
            else:
                self.les_tokens.append({'type':'tok_inferieur', "ligne": self.num_lig})
                self.num_lettre += 1
        elif c == ">":
            if self.content[self.num_lettre+1] == "=":
                self.les_tokens.append({'type':'tok_superieur_egal', "ligne": self.num_lig})
                self.num_lettre += 2
            else:
                self.les_tokens.append({'type':'tok_superieur', "ligne": self.num_lig})
                self.num_lettre += 1
        elif c == "=":
            if self.content[self.num_lettre+1] == "=":
                self.les_tokens.append({'type':'tok_egal', "ligne": self.num_lig})
                self.num_lettre += 2
            else:
                self.les_tokens.append({'type':'tok_affectation', "ligne": self.num_lig})
                self.num_lettre += 1
        elif c == "(":
            self.les_tokens.append({'type':'tok_parenthese_ouvrante', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == ")":
            self.les_tokens.append({'type':'tok_parenthese_fermante', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "{":
            self.les_tokens.append({'type':'tok_accolade_ouvrante', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "}":
            self.les_tokens.append({'type':'tok_accolade_fermante', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == ";":
            self.les_tokens.append({'type':'tok_point_virgule', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == ",":
            self.les_tokens.append({'type':'tok_virgule', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "&":
            self.les_tokens.append({'type':'tok_et', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c == "|":
            self.les_tokens.append({'type':'tok_ou', "ligne": self.num_lig})
            self.num_lettre += 1
        elif c.isdigit():
            i = self.num_lettre+1
            if i < len(self.content):
                while(self.content[i].isdigit()):
                    c += self.content[i]
                    i += 1
                self.num_lettre = i
                self.les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": self.num_lig})
            else:
                self.num_lettre += 1
                self.les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": self.num_lig})
        elif c.isalpha():
            i = self.num_lettre + 1
            while(self.content[i].isalpha()):
                c += self.content[i]
                i += 1
            self.num_lettre = i
            if self.mot_cles.get(c,"") != "":
                self.les_tokens.append({'type':self.mot_cles.get(c), 'name': c, "ligne": self.num_lig})
            else:
                self.les_tokens.append({'type':'tok_identificateur', 'name': c, "ligne": self.num_lig})
        if len(self.content)-1 == self.num_lettre:
            self.les_tokens.append({'type':'tok_EOF', "ligne": self.num_lig})
            self.skip()


if __name__ == '__main__':
    l = lexical(sys.argv[1])
    l.main()
    print(l.les_tokens)
    expression(0,l).afficher()
