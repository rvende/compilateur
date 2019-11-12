from lexical import *
from syntax import *
from semantique import *
from genCode import *
import codecs


if __name__ == '__main__':
    filenames = ['bibliotheque_standard.c', sys.argv[1]] 
    with open('main.c', 'w') as outfile: 
        for fname in filenames: 
            with open(fname) as infile: 
                for line in infile: 
                    outfile.write(line)



    lexical = Lexical("main.c")
    
    lexical.main()
    print(lexical.les_tokens)
    liste_arbre = []
    while lexical.next()['type'] != "tok_EOF":
        syntax = Syntax(lexical)
        #arbre = syntax.instruction()
        arbre = syntax.fonction()
        arbre.afficher()
        liste_arbre.append(arbre)
        
        semantique = Analyse_semantique()
        semantique.analyse(arbre)

    
    generationCode = GenerationCode(syntax)
    generationCode.lancementGenerationCode(liste_arbre)


    #bashCommand = "./msm/msm -d -d genCode"
    bashCommand = "./msm/msm genCode"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print("output :"+str(output))
    
    #print("big" + str(int.from_bytes(output, "little")))                # 1
    #int.from_bytes(output, "little")
    #print(type(output.hex()))
    #print(bytes.fromhex(output.hex()))

    print(output.decode('utf-8'))
