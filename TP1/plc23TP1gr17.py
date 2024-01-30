import re
# funcoes auxiliares
def calcula_atletas_ano(dic): # esta funcao calcula quantos atletas se inscreveram por cada ano
    total_atletas_ano = {}
    for atletas_data in dic.values():
        if atletas_data.get("data_emd")[:4] not in total_atletas_ano:
            total_atletas_ano[atletas_data.get("data_emd")[:4]] = 1
        else:
            total_atletas_ano[atletas_data.get("data_emd")[:4]] += 1
    return total_atletas_ano

def escreve_html(frase):
    htmlOutput = f'''<html>
    <head>
    <meta charset="UTF-8">  
    <h1>Processador de Registos de Exames Médicos Desportivos</h1>
    </head>
    '''

    htmlOutput += frase + f'''</body></html>'''

    with open("index.html", "w") as htmlFile:
        htmlFile.write(htmlOutput)

# a) Encontrar a maior e menor idade
def idade_extremas(dic): # a)
    idade_min = None
    idade_max = None

    for atletas_data in dic.values():
        idade = int(atletas_data.get("idade"))
        
        if idade_max is None or idade > idade_max:
            idade_max = idade
        if idade_min is None or idade < idade_min:
            idade_min = idade

    html_string = f'''<h2>a) Cálculo das idades extremas:</h2><h3>Idade max: {idade_max} </h3><h3>Idade min: {idade_min} </h3>'''
    escreve_html(html_string)

def distribuicao_genero_total(dic): # b)
    total = len(dic) # isto da me o n total de linhas no ficheiro sem contar com a primeira...
    dist_mas = 0
    dist_fem = 0
    dist_fem_percentagem = 0
    dist_mas_percentagem = 0

    for atletas_data in dic.values():
        if atletas_data.get("genero") == 'M':
            dist_mas += 1
        else:
            dist_fem += 1
    
    dist_fem_percentagem = "{:.2f}".format(dist_fem / total * 100)
    dist_mas_percentagem = "{:.2f}".format(dist_mas / total * 100) 
    html_string = f'''<h2>b) Cálculo da distribuição por género:</h2><h3>Totalidade de atletas: {total}</h3>
                        <h3>Percentagem atletas masculinos: {dist_mas_percentagem}% com {dist_mas} atletas. </h3>
                        <h3>Percentagem atletas femeninos: {dist_fem_percentagem}% com {dist_fem} atletas.</h3>'''
    escreve_html(html_string)

def distribuicao_modalidade(dic): # c)
    total = len(dic) #total de atletas
    atleta_por_modalidades_total = {}

    # percorre os valores do dicionario e conta quantos atletas cada desporto
    # tem nao fazendo distinção do ano de inscrição
    for atletas_data in dic.values():
        if atletas_data.get("modalidade") not in atleta_por_modalidades_total:
            atleta_por_modalidades_total[atletas_data.get("modalidade")] = 1
        else:
            atleta_por_modalidades_total[atletas_data.get("modalidade")] += 1

    '''-----------------------------------------'''
    # é criada uma lista para guardar os tuplos (ano, modalidade)
    total_ano_modalidade = []

    # é usado um dicionário para guardar quantos atletas se inscreveram em cada ano
    total_atletas_ano = calcula_atletas_ano(dic)
    for atletas_data in dic.values():
        total_ano_modalidade.append((atletas_data.get("data_emd")[:4], atletas_data.get("modalidade")))

    # é usada uma lista de triplos para guardar a informacao (ano, modalidade, n_atletas)
    lista_modalidades_ano = []
    for atleta in total_ano_modalidade:
        ano, desporto = atleta
        encontrado = False
        for i, (existing_ano, existing_desporto, count) in enumerate(lista_modalidades_ano):
            if ano == existing_ano and desporto == existing_desporto:
                # o par ja existe entao, soma-se 1 ao contador...
                lista_modalidades_ano[i] = (existing_ano, existing_desporto, count + 1)
                encontrado = True
                break
        if not encontrado:
            # o par ano, desporto ainda nao existe, entao adicionamos...
            lista_modalidades_ano.append((ano, desporto, 1))
            
    # ordena se a lista pelas condicoes do enunciado...
    lista_modalidades_ano_ord = sorted(lista_modalidades_ano, key=lambda x: (x[0], x[1]))

    # cria-se uma lista para guardar as percentagens de atletas por desporto por ano...
    # esta é a resposta a 2º parte...
    lista_percentagens = []
    for ano, desporto, n in lista_modalidades_ano_ord:
        lista_percentagens.append((ano, desporto, n, "{:.2f}".format(n / total_atletas_ano[ano] * 100)))

    html_string = f'''
    <h2>c) Calcular a distribuição por Modalidade em cada ano e no total:</h2>
    <h3> i. Atletas no total: </h3>
    <h3>Totalidade de atletas: {total}</h3>'''
    for modalidade, numero in atleta_por_modalidades_total.items():
        html_string += f'''<h3>{modalidade}: {"{:.2f}".format((numero/total * 100))}% com ({numero}) atletas. </h3>'''
    
    html_string += f'''
     <h3> ii. Atletas em cada ano: </h3>
    '''

    ano_atual = None
    for ano, desporto, quantidade in lista_modalidades_ano_ord:
        if ano_atual != ano:
            html_string += f'''<h3><span style="color: red;">{ano}: com {total_atletas_ano[ano]} atletas inscritos.</h3>'''
            ano_atual = ano
        html_string += f'''
        <h3> {desporto}: {"{:.2f}".format(quantidade/total_atletas_ano[ano_atual] * 100)}% com {quantidade} atletas.</h3>
    '''
    escreve_html(html_string)

def percentagem_aptos_ano(dic): # d)
    total_atletas_ano = calcula_atletas_ano(dic)

    # percorro o dicionario em busca dos anos e da informacao se o atleta foi aprovado   
    atletas = []
    for atletas_data in dic.values():
        atletas.append(((atletas_data.get("data_emd")[:4]), atletas_data.get("aprovado")))

    # percorro a lista e crio um contador para contar quantos aprovados existem num ano...
    # estou tambem a guardar a info referente aos nao aprovados... (talvez mude isto...)
    atletas_aptos_ano = []
    for atleta in atletas:
        ano, apto = atleta
        encontrado = False
        for i, (existing_ano, existing_apto, count) in enumerate(atletas_aptos_ano):
            if ano == existing_ano and apto == existing_apto:
                # o par ja existe entao, soma-se 1 ao contador...
                atletas_aptos_ano[i] = (existing_ano, existing_apto, count + 1)
                encontrado = True
                break
        if not encontrado:
            # o par ano, desporto ainda nao existe, entao adicionamos...
            atletas_aptos_ano.append((ano, apto, 1))

    atletas_aptos_ano_ordenada = sorted(atletas_aptos_ano, key = lambda x: x[0])

    html_string = f'''
    <h2>c) Calcular a percentagem de aptos por ano:</h2>'''
    for ano, apto, contador in atletas_aptos_ano_ordenada:
        if apto == 'true':
            html_string += f'''<h3>{ano}: {"{:.2f}".format((contador/total_atletas_ano[ano] * 100))}% com ({contador}) atletas aptos, num total de {total_atletas_ano[ano]} atletas. </h3>'''
    
    escreve_html(html_string)

def nomesTrocados(dic):
    linha = '[\n'
    with open("emd.json", "w") as json_file:
        
        first = True  # Variável para controlar se é o primeiro objeto na lista
        
        for atletas_data in dic.values():
            if atletas_data.get("genero") == 'M':
                # Trocar os nomes usando a sub... r'(.+)' considera a string completa como 1 grupo
                a = atletas_data["nome_primeiro"]
                atletas_data["nome_primeiro"] = re.sub(r'(.+)', atletas_data["nome_ultimo"], atletas_data["nome_primeiro"])
                atletas_data["nome_ultimo"] = re.sub(r'(.+)', a, atletas_data["nome_ultimo"])

                # Escreve o objeto JSON
                if not first:
                    linha += ',\n'
                first = False
                
                linha += '\t{\n'
                linha += f'\t\t"_id": "{atletas_data["_id"]}",\n'
                linha += f'\t\t"index": "{atletas_data["index"]}",\n'
                linha += f'\t\t"data_emd": "{atletas_data["data_emd"]}",\n'
                linha += f'\t\t"nome_primeiro": "{atletas_data["nome_primeiro"]}",\n'
                linha += f'\t\t"nome_ultimo": "{atletas_data["nome_ultimo"]}",\n'
                linha += f'\t\t"idade": "{atletas_data["idade"]}",\n'
                linha += f'\t\t"genero": "{atletas_data["genero"]}",\n'
                linha += f'\t\t"morada": "{atletas_data["morada"]}",\n'
                linha += f'\t\t"modalidade": "{atletas_data["modalidade"]}",\n'
                linha += f'\t\t"clube": "{atletas_data["clube"]}",\n'
                linha += f'\t\t"email": "{atletas_data["email"]}",\n'
                linha += f'\t\t"federado": "{atletas_data["federado"]}",\n'
                linha += f'\t\t"aprovado": "{atletas_data["aprovado"]}"\n'
                linha += '\t}'
        
        # Fecha a lista de objetos JSON
        linha += '\n]'
        
        json_file.write(linha)

def main():
    
    # dicionario principal...
    data_dic = {}

    with open('emd.csv', 'r') as file:
        next(file) # ignorar a primeira linha do ficheiro...
        for line in file:
            colunas = re.split(r',', line.strip())
            _id, index, data_emd, nome_primeiro, nome_ultimo, idade, genero, morada, modalidade, clube, email, federado, aprovado = colunas
                
            # criar um dicionario para a linha atual...
            atleta = {
                "_id": _id,
                "index": index,
                "data_emd": data_emd,
                "nome_primeiro": nome_primeiro,
                "nome_ultimo": nome_ultimo,
                "idade": idade,
                "genero": genero,
                "morada": morada,
                "modalidade": modalidade,
                "clube": clube,
                "email": email,
                "federado": federado,
                "aprovado": aprovado
            }

            data_dic[_id] = atleta 

    while True:
        ans = int(input("Escolhe uma opção:\n 1- Cálculo das idades máximas e mínimas\n 2- Cálculo da percentagem por género\n 3- Cálculo da percentagem por modalidade\n 4- Cálculo da percentagem de aptos\n 5- Correção dos nomes em json\n 0- Sair\n"))
        if ans == 1:
            idade_extremas(data_dic)
        elif ans == 2:
            distribuicao_genero_total(data_dic)
        elif ans == 3:
            distribuicao_modalidade(data_dic)
        elif ans == 4:
            percentagem_aptos_ano(data_dic)
        elif ans == 5:
            nomesTrocados(data_dic)
        elif ans == 0:
            break

if __name__ == '__main__':
    main()