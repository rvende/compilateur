from lexical import *
from arbre import *
from syntax import *
from semantique import *
from genCode import *
import unittest
import subprocess

class Test_GenCode(unittest.TestCase):

	def test_noeud_continue(self):
		f = open("test.c","w+")
		f.write("function main() { continue; print(32); return 0;}")
		f = f.close()
		filenames = ['bibliotheque_standard.c', "test.c"]

		with open("main.c","w") as outfile:
			for fname in filenames:
				with open(fname) as infile:
					for line in infile:
						outfile.write(line)
			outfile.close()
		lexical = Lexical("main.c")
		lexical.main()
		liste_arbre = []
		while lexical.next()['type'] != "tok_EOF":
			syntax = Syntax(lexical)
			arbre = syntax.fonction()
			liste_arbre.append(arbre)
			semantique = Analyse_semantique()
			semantique.analyse(arbre)
		generationCode = GenerationCode(syntax)
		self.assertRaises(GenCodeException,generationCode.lancementGenerationCode,liste_arbre)
		

	def test_noeud_break(self):
		f = open("test.c","w+")
		f.write("function main() { break; print(32); return 0;}")
		f = f.close()
		filenames = ['bibliotheque_standard.c', "test.c"]

		with open("main.c","w") as outfile:
			for fname in filenames:
				with open(fname) as infile:
					for line in infile:
						outfile.write(line)
			outfile.close()
		lexical = Lexical("main.c")
		lexical.main()
		liste_arbre = []
		while lexical.next()['type'] != "tok_EOF":
			syntax = Syntax(lexical)
			arbre = syntax.fonction()
			liste_arbre.append(arbre)
			semantique = Analyse_semantique()
			semantique.analyse(arbre)
		generationCode = GenerationCode(syntax)
		self.assertRaises(GenCodeException,generationCode.lancementGenerationCode,liste_arbre)
	



if __name__ == '__main__':
    unittest.main()