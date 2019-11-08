from lexical import *
from syntax import *
from semantique import *
from genCode import *


if __name__ == '__main__':
    lexical = Lexical(sys.argv[1])
    lexical.main()
    print(lexical.les_tokens)
    liste_arbre = []
    while lexical.next()['type'] != "tok_EOF":
        syntax = Syntax(lexical)
        #arbre = syntax.instruction()
        arbre = syntax.fonction()
        arbre.afficher()
        liste_arbre.append(arbre)
        print ("toto")
        semantique = Analyse_semantique()
        semantique.analyse(arbre)


    print("tata")
    generationCode = GenerationCode(syntax)
    generationCode.lancementGenerationCode(liste_arbre)

    print("tutu")

    bashCommand = "./msm/msm -d -d genCode"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode('utf8'))
