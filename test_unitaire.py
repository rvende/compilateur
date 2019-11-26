from lexical import *
from arbre import *
from syntax import *
import unittest

class Test_Syntax(unittest.TestCase):
	"""docstring for Test_Syntax coverage run unittest discover 
	coverage report
	coverage html"""

	def test_plus_unaire(self):
		f = open("test.c","w+")
		f.write("+3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_plus_unaire")
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_moins_unaire(self):
		f = open("test.c","w+")
		f.write("-3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_moins_unaire")
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)
	
	def test_plus_binaire(self):
		f = open("test.c","w+")
		f.write("2+3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_plus_binaire")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_moins_binaire(self):
		f = open("test.c","w+")
		f.write("2-3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_moins_binaire")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_division(self):
		f = open("test.c","w+")
		f.write("2/3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_division")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_multiplication(self):
		f = open("test.c","w+")
		f.write("2*3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_multiplication")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_modulo(self):
		f = open("test.c","w+")
		f.write("2%3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_modulo")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	def test_puissance(self):
		f = open("test.c","w+")
		f.write("2^3")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()
		a1 = arbre("noeud_puissance")
		a1.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(arbre("noeud_constante", 3))
		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

	#def test_moins_seul(self):
	#	f = open("test.c","w+")
	#	f.write("-")
	#	f.close()
	#	l = Lexical("test.c")
	#	syntax = Syntax(l)
	#	res = syntax.expression(0).toString()
	#	l.main()
	#	with self.assertRaises(SyntaxException) as context:
	#		syntax.expression(0).afficher()

	def test_all_operateur(self):
		f = open("test.c","w+")
		f.write("-2+3*6/2%8^2")
		f.close()
		l = Lexical("test.c")
		l.main()
		syntax = Syntax(l)
		res = syntax.expression(0).toString()

		a1 = arbre("noeud_plus_binaire")

		a2 = arbre("noeud_moins_unaire")
		a2.ajouterFils(arbre("noeud_constante", 2))
		a1.ajouterFils(a2)

		a3 = arbre("noeud_modulo")
		a1.ajouterFils(a3)

		a4 = arbre("noeud_division")
		a3.ajouterFils(a4)
		

		a5 = arbre("noeud_multiplication")
		a5.ajouterFils(arbre("noeud_constante", 3))
		a5.ajouterFils(arbre("noeud_constante", 6))
		a4.ajouterFils(a5)
		a4.ajouterFils(arbre("noeud_constante", 2))

		a6 = arbre("noeud_puissance")
		a6.ajouterFils(arbre("noeud_constante", 8))
		a6.ajouterFils(arbre("noeud_constante", 2))
		a3.ajouterFils(a6)

		res_attendu = a1.toString()
		self.assertEqual(res, res_attendu)

if __name__ == '__main__':
    unittest.main()