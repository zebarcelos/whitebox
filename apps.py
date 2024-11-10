operacoes_compra = ["(vMedia1[1] < vMedia2[1]) and (vMedia1 > vMedia2)","(Close[2] < vBollinger2[2]) and (Close[1] > vBollinger2[1]) and (Close > vBollinger2)"]
operacoes_venda = ["(vMedia1[1] > vMedia2[1]) and (vMedia1 < vMedia2)","(Close[2] > vBollinger1[2]) and (Close[1] < vBollinger1[1]) and (Close > vBollinger1)"]

def selecvars(*args):
    variaveis = ""
    for i in args:
        if isinstance(i, list):  # Se o argumento for uma lista
            for item in i:  # Itera sobre cada item da lista
                variaveis += item + "\n"
        else:  # Se não for lista, adiciona diretamente
            variaveis += i + "\n"
    return variaveis
   
def selecinds(*args):
    variaveis = ""
    for i in args:
        if isinstance(i, list):  # Se o argumento for uma lista
            for item in i:  # Itera sobre cada item da lista
                variaveis += item + "\n"
        else:  # Se não for lista, adiciona diretamente
            variaveis += i + "\n"
    return variaveis


def operationsbuy(*args):
    variaveis = ""
    
    # Verifica se há argumentos e se eles não são listas vazias
    if args and any(args):
        for i in args:
            if isinstance(i, list):  # Se o argumento for uma lista
                for index, item in enumerate(i):  # Itera com índice
                    if index == len(i) - 1:  # Verifica se é o último item
                        variaveis += item  # Adiciona sem 'and'
                    else:
                        variaveis += item + " and "
            else:  # Se não for lista
                variaveis += i + " and "
        
        # Remover o último ' and ' se houver
        if variaveis.endswith(" and "):
            variaveis = variaveis[:-5]
        
        return "if " + variaveis 
    
    return ""  # Retorna None se não houver argumentos ou se forem listas vazias


def operationssell(*args):
    variaveis = ""
    
    # Verifica se há argumentos e se eles não são listas vazias
    if args and any(args):
        for i in args:
            if isinstance(i, list):  # Se o argumento for uma lista
                for index, item in enumerate(i):  # Itera com índice
                    if index == len(i) - 1:  # Verifica se é o último item
                        variaveis += item  # Adiciona sem 'and'
                    else:
                        variaveis += item + " and "
            else:  # Se não for lista
                variaveis += i + " and "
        
        # Remover o último ' and ' se houver
        if variaveis.endswith(" and "):
            variaveis = variaveis[:-5]
        
        return "if " + variaveis 
    
    return ""  # Retorna None se não houver argumentos ou se forem listas vazias



# Exemplo de uso


print(operationssell(operacoes_venda))