from lexical import *
from arbre import *
from syntax import *
from semantique import *
from genCode import *
import unittest
import subprocess

class Test_Fonction(unittest.TestCase):

	def test_fonction_recursive_un_arg(self):
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
		
	def test_fonction_recursive_deux_arg(self):
		f = open("test.c","w+")

		f.write("function somme(n,m){ if(n<=0){ return 2+m; }else{ return n*m + somme(n-1,m); } } function main() { var a; a = 2; a = a+ somme(22,4); return a;}")
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
		self.assertEqual(output.decode('utf8'),"1020\n")

	def test_fonction_recursive_trois_arg(self):
		f = open("test.c","w+")

		f.write("function somme(n,m,k){ if(n<=0){ return 2+m+k;  }else{ if(n == 15){ return n;} var i; for(i =0;i<3;i=i+1){ n = n-1; if(n == 12){ break; }} return n*m+k + somme(n-1,m,k-1) + k -2; } } function main() { var a; a = 2; a = a+ somme(22,4,2); return a;}")
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
		self.assertEqual(output.decode('utf8'),"218\n")

	def test_fonction_recursive_trois_arg_with_loops_and_break(self):
		f = open("test.c","w+")

		f.write("function somme(n,m,k){ if(n<=0){ return 2+m+k;  }else{ return n*m+k + somme(n-1,m,k-1) + k -2; } } function main() { var a; a = 2; a = a+ somme(22,4,2); return a;}")
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
		self.assertEqual(output.decode('utf8'),"582\n")

if __name__ == '__main__':
    unittest.main()