
les_tokens = []

fichier = open("bidule.txt","r")
content = ficher.read()

num_lettre = 0
num_lig = 1

index_token = 0

def next():
    return les_tokens[index_token]

def skip():
    index_token += 1

def main():
    while(num_lettre < len(content)):
        if content[num_lettre] != " " and (content[num_lettre] != "\\" and next() != "n"):
            tokens(content[num_lettre], num_lig)
            skip()
        else:
            if content[num_lettre] != "\\" and next() != "n":
                skip()
                skip()
                num_lig += 1
            else:
                skip()


def tokens(c, num_lig):
    if c == "+":
        les_tokens.append({'type':'tok_plus', "ligne": num_lig})
    elif c == "-":
        les_tokens.append({'type':'tok_moins', "ligne": num_lig})
    elif c.isdigit():
        i = num_lettre+1
        while(content[i].isdigit()):
            c += content[i]
            i += 1
        num_lettre = i
        les_tokens.append({'type':'tok_constante', 'valeur': int(c), "ligne": num_lig})
    elif c.isalpha():
        i = num_lettre+1
        while(content[i].isalpha()):
            c += content[i]
            i += 1
        num_lettre = i
        les_tokens.append({'type':'tok_identificateur', 'name': c, "ligne": num_lig})

if __name__ == '__main__':
    main()
