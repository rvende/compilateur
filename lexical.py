
les_tokens = []

fichier = open("test.c","r")
content = fichier.read()
print(content)
index_token = -1
num_lettre = 0
num_lig = 1

def next():
    if index_token != -1:
        return les_tokens[index_token]
    else:
        return None

def skip():
    global index_token
    index_token = index_token + 1

def main():
    global num_lettre
    global num_lig
    while(True):
        if next() != None:
            if next()['type'] == "tok_EOF":
                for elem in les_tokens:
                    print(elem['type'])
                break
        if content[num_lettre] != " " and content[num_lettre] != "\n":
            tokens(content[num_lettre])
            skip()
        else:
            if content[num_lettre] == "\n":
                num_lig += 1
            num_lettre += 1


def tokens(c):
    global num_lettre
    global num_lig
    if c == "+":
        les_tokens.append({'type':'tok_plus', "ligne": num_lig})
        num_lettre += 1
    elif c == "-":
        les_tokens.append({'type':'tok_moins', "ligne": num_lig})
        num_lettre += 1
    elif c == "*":
        les_tokens.append({'type':'tok_multiplication', "ligne": num_lig})
        num_lettre += 1
    elif c == "/":
        les_tokens.append({'type':'tok_division', "ligne": num_lig})
        num_lettre += 1
    elif c == "%":
        les_tokens.append({'type':'tok_modulo', "ligne": num_lig})
        num_lettre += 1
    elif c == "^":
        les_tokens.append({'type':'tok_puissance', "ligne": num_lig})
        num_lettre += 1
    elif c == "!":
        if content[num_lettre+1] == "=":
            les_tokens.append({'type':'tok_different', "ligne": num_lig})
            num_lettre += 2
    elif c == "<":
        if content[num_lettre+1] == "=":
            les_tokens.append({'type':'tok_inferieur_egal', "ligne": num_lig})
            num_lettre += 2
        else:
            les_tokens.append({'type':'tok_inferieur', "ligne": num_lig})
            num_lettre += 1
    elif c == ">":
        if content[num_lettre+1] == "=":
            les_tokens.append({'type':'tok_superieur_egal', "ligne": num_lig})
            num_lettre += 2
        else:
            les_tokens.append({'type':'tok_superieur', "ligne": num_lig})
            num_lettre += 1
    elif c == "=":
        if content[num_lettre+1] == "=":
            les_tokens.append({'type':'tok_egal', "ligne": num_lig})
            num_lettre += 2
        else:
            les_tokens.append({'type':'tok_affectation', "ligne": num_lig})
            num_lettre += 1
    elif c == "(":
        les_tokens.append({'type':'tok_parenthèse_ouvrante', "ligne": num_lig})
        num_lettre += 1
    elif c == ")":
        les_tokens.append({'type':'tok_parenthèse_fermante', "ligne": num_lig})
        num_lettre += 1
    elif c == "{":
        les_tokens.append({'type':'tok_accolade_ouvrante', "ligne": num_lig})
        num_lettre += 1
    elif c == "}":
        les_tokens.append({'type':'tok_accolade_fermante', "ligne": num_lig})
        num_lettre += 1
    elif c == ";":
        les_tokens.append({'type':'tok_point_virgule', "ligne": num_lig})
        num_lettre += 1
    elif c == ",":
        les_tokens.append({'type':'tok_virgule', "ligne": num_lig})
        num_lettre += 1
    elif c.isdigit():
        i = num_lettre+1
        while(content[i].isdigit()):
            c += content[i]
            i += 1
        num_lettre = i
        les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": num_lig})
    elif c.isalpha():
        i = num_lettre + 1
        while(content[i].isalpha()):
            c += content[i]
            i += 1
        num_lettre = i
        les_tokens.append({'type':'tok_identificateur', 'name': c, "ligne": num_lig})
    if len(content)-1 == num_lettre:
        les_tokens.append({'type':'tok_EOF', "ligne": num_lig})
        skip()


if __name__ == '__main__':
    main()
