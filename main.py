from lexical import *
from syntax import *
from semantique import *
from genCode import *


if __name__ == '__main__':
    lexical = Lexical(sys.argv[1])
    lexical.main()

    syntax = Syntax(lexical)
    arbre = syntax.instruction()
    arbre.afficher()

    semantique = Analyse_semantique()
    semantique.analyse(arbre)

    generationCode = GenerationCode(syntax, semantique)
    generationCode.lancementGenerationCode(arbre)


    bashCommand = "./msm/msm -d -d genCode"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode('utf8'))
