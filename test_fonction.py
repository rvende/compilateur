from lexical import *
from arbre import *
from syntax import *
from semantique import *
from genCode import *
import unittest
import subprocess

class Test_Fonction(unittest.TestCase):

	def test_fonction_recursive(self):
		f = open("test.c","w+")

		f.write("function somme(n){ if(n<=0){ return 2; }else{ return n + somme(n-1); } } function main() { var a; a = 2; a = a+ somme(22); return a;}")
		f = f.close()
		lexical = Lexical("test.c")
		lexical.main()
		liste_arbre = []
		while lexical.next()['type'] != "tok_EOF":
			syntax = Syntax(lexical)
			arbre = syntax.fonction()
			liste_arbre.append(arbre)
			semantique = Analyse_semantique()
			semantique.analyse(arbre)
		generationCode = GenerationCode(syntax)
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		print("Res : "+output.decode('utf8'))
		self.assertEqual(output.decode('utf8'),"257\n")

if __name__ == '__main__':
    unittest.main()