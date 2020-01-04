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

		f.write("function somme(n){ if(n<=0){ return 2; }else{ return n + somme(n-1); } } function main() { var a; a = 2; a = a+ somme(22); print(a); return a;}")
		f = f.close()
		filenames = ['bibliotheque_standard.c', "test.c"]

		with open("main.c","w") as outfile:
			for fname in filenames:
				with open(fname) as infile:
					for line in infile:
						outfile.write(line)
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"257\n")

	def test_fonction_recursive_deux_arg(self):
		f = open("test.c","w+")

		f.write("function somme(n,m){ if(n<=0){ return 2+m; }else{ return n*m + somme(n-1,m); } } function main() { var a; a = 2; a = a+ somme(22,4); print(a); return a;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"1020\n")

	def test_fonction_recursive_trois_arg(self):
		f = open("test.c","w+")

		f.write("function somme(n,m,k){ if(n<=0){ return 2+m+k;  }else{ if(n == 15){ return n;} var i; for(i =0;i<3;i=i+1){ n = n-1; if(n == 12){ break; }} return n*m+k + somme(n-1,m,k-1) + k -2; } } function main() { var a; a = 2; a = a+ somme(22,4,2); print(a); return a;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"218\n")

	def test_fonction_recursive_trois_arg_with_loops_and_break(self):
		f = open("test.c","w+")

		f.write("function somme(n,m,k){ if(n<=0){ return 2+m+k;  }else{ return n*m+k + somme(n-1,m,k-1) + k -2; } } function main() { var a; a = 2; a = a+ somme(22,4,2); print(a); return a;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"582\n")

	def test_portee_variables(self):
		f = open("test.c","w+")

		f.write("function main() { var a; a = 4; { var b; b = a+3; print(b);}{ var a; a = 3; var b; b = 5; print(a+b);} print(a);}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"7\n8\n4\n")

	def test_affichage_negatif(self):
		f = open("test.c","w+")
		f.write("function main() { print(-51); return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"-51\n")

	def test_break_else(self):
		f = open("test.c","w+")
		f.write("function main() {var x;var i;x = 2;for(i = 0; i < 5; i = i + 1){if(x<5){x = x + 1;print(1);}else{break;} }print(3);return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"1\n1\n1\n3\n")


	def test_boucle_for(self):
		f = open("test.c","w+")
		f.write("function main() { var i; for(i=0;i<5;i=i+1){ print(i); } return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"0\n1\n2\n3\n4\n")


	def test_boucle_while(self):
		f = open("test.c","w+")
		f.write("function main() { var i; while(i<5){ print(i); i = i+1; } return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"0\n1\n2\n3\n4\n")



	def test_boucle_while_boucle_for_break(self):
		f = open("test.c","w+")
		f.write("function main() { var i; while(i<5){ print(i); if(i == 3){ var j; for(j=3;j>=0;j = j-1){ print(j);} break; }else{ i = i+1;} } return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"0\n1\n2\n3\n3\n2\n1\n0\n")



	def test_boucle_while_boucle_for_break_continue(self):
		f = open("test.c","w+")
		f.write("function main() { var i; while(i<5){ print(i); if(i == 4){ var j; for(j=3;j>=0;j = j-1){ print(j); } /* break*/ break; }else{ if(i == 2){ i= i+2; continue; } i = i+1; } } return 0;}")
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
		generationCode.lancementGenerationCode(liste_arbre)
		bashCommand = "./msm/msm genCode"
		process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
		output,error = process.communicate()
		self.assertEqual(output.decode('utf8'),"0\n1\n2\n4\n3\n2\n1\n0\n")





if __name__ == '__main__':
    unittest.main()
