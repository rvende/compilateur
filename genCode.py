from arbre import *
from syntax import *

class GenerationCode(object):
    """docstring forGenerationCode."""
    def __init__(self, syntax):
        self.cpt = 0
        self.loop = []
        self.syntax = syntax
        self.fichier = open("genCode", "w")


    def lancementGenerationCode(self, liste_noeud):
        """
        Permet de lancer la génération du code associé à chaque noeud de la liste
        liste_noeud.
        Paramètre: liste_noeud: une liste de string donnant le type de noeud
        """
        for noeud in liste_noeud:
            self.genCode(noeud)
        self.fichier.write(".start\n")
        self.fichier.write("prep main\n")
        self.fichier.write("call 0\n")
        #self.fichier.write("dbg \n")
        self.fichier.write("halt\n")
        self.fichier.close()

    def genCode(self, noeud):
        """
        Fonction qui permet la génération du code d'un noeud.
        Paramètre: noeud: une string donnant le type du noeud
        """
        # Constante
        if noeud.type == "noeud_constante":
            self.fichier.write("push "+str(noeud.valeur)+"\n")

        # Operateur binaire
        if noeud.type in self.syntax.op_binaire.keys():
            self.genCode(noeud.fils[0])
            self.genCode(noeud.fils[1])
            self.fichier.write(self.syntax.op_binaire[noeud.type]+"\n")

        # Operateur unaire
        if noeud.type in self.syntax.op_unaire.keys():
            self.fichier.write("push 0\n")
            self.genCode(noeud.fils[0])
            self.fichier.write(self.syntax.op_unaire[noeud.type]+"\n")

        # Autre
        if noeud.type == "noeud_puissance":
            raise GenCodeException("Erreur: noeud_puissance non implemente.")


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
            self.fichier.write("jumpf l"+str(memory_false)+" ;jump cond false \n")
            self.genCode(noeud.fils[1])
            self.cpt += 1
            if len(noeud.fils) > 2:
                if noeud.fils[2].type=="noeud_break": #si il y a un break sur la cond (on est dans une boucle for)
                    self.fichier.write("jump l"+str(self.cpt)+" ;jump label loop\n")
                if noeud.fils[2].type=="noeud_bloc": #on a un bloc else dans la cond
                    self.cpt += 1
                    memory_else = self.cpt
                    self.fichier.write("jump l"+str(self.cpt)+" ;jump label fin else\n")
            self.fichier.write(".l"+str(memory_false)+" ;label break\n")
            if len(noeud.fils) > 2: #si il y a un break sur la cond
                if noeud.fils[2].type == "noeud_break":
                    self.genCode(noeud.fils[2])
                    self.fichier.write(".l"+str(self.cpt)+" ;label loop "+str(noeud.type)+"\n")
                else:
                    self.genCode(noeud.fils[2])
                    self.fichier.write(".l"+str(memory_else)+" ;label after else \n")


        if noeud.type == "noeud_break":
            if self.loop != []:
                self.fichier.write("jump l"+str(self.loop[-1][1])+" ;break\n")
            else:
                raise GenCodeException("Erreur: break n'est pas dans une boucle.")

        if noeud.type == "noeud_continue":
            if self.loop != []:
                self.fichier.write("jump l"+str(self.loop[-1][0])+" ;continue\n")
            else:
                raise GenCodeException("Erreur: continue n'est pas dans une boucle.")

        if noeud.type == "noeud_loop":
            self.cpt += 1
            # stockage des labels de debut et fin de loop dans un tuple: (debut,fin)
            self.loop.append((self.cpt,self.cpt+1))
            self.cpt += 1
            current_loop = self.loop[-1]
            self.fichier.write(".l"+str(current_loop[0])+" ;loop\n")
            self.genCode(noeud.fils[0])
            self.fichier.write("jump l"+str(current_loop[0])+" ;jump loop\n")
            self.fichier.write(".l"+str(current_loop[1])+" ;end loop\n")
            self.loop.pop()

        if noeud.type == "noeud_appel_fonction":
            self.fichier.write("prep "+noeud.valeur+"\n")
            for i in range(len(noeud.fils)):
                self.genCode(noeud.fils[i])
            self.fichier.write("call "+str(len(noeud.fils))+"\n")

        if noeud.type == "noeud_function":
            self.fichier.write("."+noeud.valeur+"\n")
            self.fichier.write("resn "+str(noeud.slot-noeud.nargs)+"\n")

            self.genCode(noeud.fils[0])

            self.fichier.write("push 0 \n")
            self.fichier.write("ret \n")

        if noeud.type == "noeud_return":
            self.genCode(noeud.fils[0])
            self.fichier.write("ret \n")

        if noeud.type == "noeud_send":
            self.genCode(noeud.fils[0])
            self.fichier.write("send \n")

        if noeud.type == "noeud_recv":
            self.fichier.write("recv \n")





class GenCodeException(Exception):
    """docstring for SyntaxException"""
    def __init__(self, message):
        self.msg = message
        super(GenCodeException,self).__init__(self.msg)
