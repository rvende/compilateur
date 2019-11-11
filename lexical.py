import sys



class Lexical():

    def __init__(self, fichier):
        self.fichier = open(fichier,"r")
        self.les_tokens = []

        #self.mot_cles = {"if":"tok_if", "else":"tok_else", "for":"tok_for", "var":"tok_var", "while":"tok_while","function":"tok_function","return":"tok_return", "break":"tok_break"}
        self.mot_cles = {"if":"tok_if", "else":"tok_else", "for":"tok_for", "var":"tok_var", "while":"tok_while","function":"tok_function","return":"tok_return", "break":"tok_break",\
                        "continue": "tok_continue","send":"tok_send","recv":"tok_recv"}
        self.operateur_binaire = {"+":"tok_plus", "-":"tok_moins", "*":"tok_multiplication", "/":"tok_division",\
                                  "^":"tok_puissance", "%":"tok_modulo", "&":"tok_et", "|":"tok_ou"}
        self.ponctuaction = {"(":"tok_parenthese_ouvrante", ")":"tok_parenthese_fermante",\
                             "{":"tok_accolade_ouvrante", "}":"tok_accolade_fermante", ";":"tok_point_virgule", ",":"tok_virgule"}
        self.comparaison = {"!=":"tok_different", "<":"tok_inferieur", ">":"tok_superieur", "<=":"tok_inferieur_egal",\
                            ">=":"tok_superieur_egal", "=":"tok_affectation", "==":"tok_egal"}
        self.content = self.fichier.read()
        self.index_token = -1
        self.num_lettre = 0
        self.num_lig = 1
        self.num_col = 1

    def next(self):
        if self.index_token != -1 and self.index_token < len(self.les_tokens):
            return self.les_tokens[self.index_token]
        else:
            return None

    def skip(self):
        self.index_token = self.index_token + 1

    def accept(self, t):
        if(self.next()['type'] == t):
            self.skip()
        else:
            raise Exception("Erreur: fonction accept, type différent")

    def main(self):
        while(True):
            if self.next() != None:
                if self.next()['type'] == "tok_EOF":
                    self.index_token = 0
                    break
            if self.num_lettre < len(self.content):
                if self.content[self.num_lettre] != " " and self.content[self.num_lettre] != "\n" and self.content[self.num_lettre] != "\t" :
                    self.tokens(self.content[self.num_lettre])
                    self.skip()
                else:
                    if self.content[self.num_lettre] == "\n":
                        self.num_lig += 1
                        self.num_lettre += 1
                        self.num_col = 1
                    else:
                        self.num_lettre += 1
                        self.num_col += 1
            else:
                if len(self.content) == self.num_lettre:
                    self.les_tokens.append({'type':'tok_EOF', "ligne": self.num_lig, "colonne": self.num_col})
                    self.skip()
                self.num_lettre += 1
                self.num_col += 1


    def tokens(self, c):
        #print(c)
        #print(self.comparaison.keys())
        if c in self.operateur_binaire.keys():
            self.les_tokens.append({'type': self.operateur_binaire[c], "ligne": self.num_lig, "colonne": self.num_col})
            self.num_lettre += 1
            self.num_col += 1
        elif c in self.ponctuaction.keys():
            self.les_tokens.append({'type': self.ponctuaction[c], "ligne": self.num_lig, "colonne": self.num_col})
            self.num_lettre += 1
            self.num_col += 1
        elif c in self.comparaison.keys() or c == "!":
            if self.content[self.num_lettre+1] == "=":
                self.les_tokens.append({'type': self.comparaison[c+"="], "ligne": self.num_lig, "colonne": self.num_col})
                self.num_lettre += 2
                self.num_col += 2
            else:
                self.les_tokens.append({'type': self.comparaison[c], "ligne": self.num_lig, "colonne": self.num_col})
                self.num_lettre += 1
                self.num_col += 1
        elif c.isdigit():
            i = self.num_lettre+1
            if i < len(self.content):
                while(self.content[i].isdigit()):
                    c += self.content[i]
                    i += 1
                self.num_lettre = i
                self.num_col = i
                self.les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": self.num_lig, "colonne": self.num_col})
            else:
                self.num_lettre += 1
                self.num_col += 1
                self.les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": self.num_lig, "colonne": self.num_col})
        elif c.isalpha():
            i = self.num_lettre + 1
            while(self.content[i].isalpha()):
                c += self.content[i]
                i += 1
            self.num_lettre = i
            self.num_col = i
            if self.mot_cles.get(c,"") != "":
                self.les_tokens.append({'type':self.mot_cles.get(c), 'name': c, "ligne": self.num_lig, "colonne": self.num_col})
            else:
                self.les_tokens.append({'type':'tok_identificateur', 'name': c, "ligne": self.num_lig, "colonne": self.num_col})
