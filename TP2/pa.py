import ply.yacc as yacc
import sys
import os.path
from lexer import tokens
import os



def p_Programa(p):
	"""
	Programa : Inicio Corpo Fim
	"""
	p[0] = p[2]


def p_Corpo(p):
	"""
	Corpo : Declaracoes Instrucoes
	"""
	p[0] = (p[1] or '') + 'START\n' + (p[2] or '') + 'STOP'
	
def p_Declaracoes(p):
	"""
	Declaracoes : Declaracoes Declaracao
	"""
	p[0] = (p[1] or '') + (p[2] or '')


def p_Declaracoes_Vazia(p):
	"""
	Declaracoes : 
	"""
	pass

def p_Declaracao_Variavel(p):
	"""
	Declaracao : Tipo Var PontoVirgula
	"""
	global contador_pos_stack
	tipo = p[1]
	nome = p[2]

	if tipo == "int":
		if nome not in tabela_de_simbolos:
			tabela_de_simbolos[nome] = {
				'tipo': tipo,
				'valor': 0,
				'posicao_stack': contador_pos_stack
			}
			#tabela_de_posicoes.append = 0
			contador_pos_stack += 1
			p[0] = 'PUSHI 0\n'
		else: 
			p[0] = f'ERR \"múltipla declaração da variável {p[2]}\\n\"\nSTOP\n'
	else:
		p[0] = f'ERR \"tipo nao aceite {p[2]}\\n\"\nSTOP\n'


def p_Declaracao_Array(p):
	"""
	Declaracao : Tipo Var  Expressao ParRetoDir PontoVirgula
	"""
	global contador_pos_stack
	tipo = p[1]
	nome = p[2]
	tam = p[4]

	try:
		tamanho = int(tam)
	except ValueError:
		p[0] = f'ERR \"Tamanho inválido para a variavel {nome}\\n\"\nSTOP\n'
		return
	
	array = {}
	for i in range(tamanho):
		array[i] = 0

	if tipo == "int":
		if nome not in tabela_de_simbolos:
			tabela_de_simbolos[nome] = {
				'tipo': tipo,
				'tamanho': tamanho,
				'array': array,
				'posicao_stack': contador_pos_stack 
			}
			contador_pos_stack += 1
			p[0] = f'PUSHN {tamanho}\n'
		else:
			p[0] = f'ERR \"múltipla declaração da variável {p[2]}\\n\"\nSTOP\n'
	else:
		p[0] = f'ERR \"tipo nao aceite {p[2]}\\n\"\nSTOP\n'

def p_Declaracao_Matriz(p):
	"""
	Declaracao : Tipo Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir PontoVirgula
	"""
	global contador_pos_stack
	tipo = p[1]
	nome = p[2]
	tam1 = p[4]
	tam2 = p[7]

	try:
		tamanho1 = int(tam1)
		tamanho2 = int(tam2)
	except ValueError:
		p[0] = f'ERR \"Tamanho inválido para a variavel {nome}\\n\"\nSTOP\n'
		return

	matriz = {}
	
	for i in range(int(tamanho1)):
		matriz[i] = {}
		for j in range(int(tamanho2)):
			matriz[i][j] = 0

	if tipo == "int":
		if nome not in tabela_de_simbolos:
			tabela_de_simbolos[nome] = {
				'tipo': tipo,
				'tamanho1': tamanho1,
				'tamanho2': tamanho2,
				'matriz': matriz,
				'posicao_stack': contador_pos_stack 
			}
			contador_pos_stack += 1
			p[0] = f'PUSHN {tamanho1*tamanho2}\n'
		else:
			p[0] = f'ERR \"múltipla declaração da variável {p[2]}\\n\"\nSTOP\n'
	else:
		p[0] = f'ERR \"tipo nao aceite {p[2]}\\n\"\nSTOP\n'

def p_Instrucoes(p):
	"""
	Instrucoes : Instrucoes Instrucao
	"""
	p[0] = (p[1] or '') + (p[2] or '')

def p_Instrucoes_Vazia(p):
	"""
	Instrucoes : 
	"""
	pass

def p_Instrucao(p):
	"""
	Instrucao : Atribuicao
		| Leitura
		| Escrita
		| Selecao
		| Repeticao
	"""
	p[0] = p[1]

def p_Atribuicao_Variavel(p):
	"""
	Atribuicao : Var Vale Expressao PontoVirgula
	"""
	nome = p[1]
	valor = p[3]
	if nome not in tabela_de_simbolos:
		p[0] = f'ERR \"variavel nao defenida {p[1]}\\n\"\nSTOP\n'
	else:
		tabela_de_simbolos[nome]['valor'] = valor
		pos = tabela_de_simbolos[nome]['posicao_stack']
		#tabela_de_posicoes[pos] = (nome, valor)
		p[0] = f'{valor}\nSTOREG {pos}\n'

def p_Atribuicao_Array(p):
	"""
	Atribuicao : Var ParRetoEsq Expressao ParRetoDir Vale Expressao PontoVirgula
	"""
	nome = p[1]
	indice = p[3]
	valor = p[6]
	if nome not in tabela_de_simbolos:
		p[0] = f'ERR \"variavel nao defenida {p[1]}\\n\"\nSTOP\n'
	else:
		tabela_de_simbolos[nome]['array'][indice] = valor
		p[0] = f'{valor}\n'


def p_Atribuicao_Matriz(p):
	"""
	Atribuicao : Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir Vale Expressao PontoVirgula
	"""
	nome = p[1]
	indice1 = p[3]
	indice2 = p[6]
	valor = p[9]
	if nome not in tabela_de_simbolos:
		p[0] = f'ERR \"variável nao defenida {p[1]}\\n\"\nSTOP\n'
	else:
		tabela_de_simbolos[nome]['matriz'][indice1][indice2] = valor
		p[0] = f'PUSHI {valor}\n'


tabela_de_condicoes = {
	'==': 'EQUAL\n',
	'!=': 'EQUAL\nNOT\n',
	'<=': 'INFEQ\n',
	'>=': 'SUPEQ\n',
	'<':  'INF\n',
	'>':  'SUP\n',
}

def p_Condicao_Expressao(p):
	"""
	Condicao : Expressao
	"""
	p[0] = p[1]

def p_Condiao(p):
    """
    Condicao : Expressao Igual Expressao
        | Expressao Diferente Expressao
        | Expressao MenorIgual Expressao
        | Expressao MaiorIgual Expressao
        | Expressao Menor Expressao
        | Expressao Maior Expressao
    """
    #exp1 = tabela_de_simbolos[]
    #exp2 = tabela_de_simbolos[p[3]]['posicao_stack']
    op = tabela_de_condicoes[p[2]]

    p[0] = f'{p[1]}\n{p[3]}\n{op}'

def p_Expressao_Termo(p):
	"""
	Expressao : Termo
	"""
	p[0] = p[1]

tabela_aritmetica = {
	'+': 'ADD\n',
	'-': 'SUB\n',
	'*': 'MUL\n',
	'/': 'DIV\n',
	'OU': 'OR\n',
	'E': 'AND\n'
}

def p_Expressao_Soma_OU_Subtracao(p):
	"""
	Expressao : Expressao Soma Termo
		| Expressao Subtracao Termo
		| Expressao OU Termo
	"""
	exp1 = p[1]
	termo1 = p[3]
	op = tabela_aritmetica[p[2]]
	p[0] = f'{exp1}\n {termo1}\n{op}'

def p_Termo_Fator(p):
	"""
	Termo : Fator
	"""
	p[0] = p[1]

def p_Termo_Multiplicacao_E_Divisao(p):
	"""
	Termo : Termo Multiplicacao Fator
		| Termo Divisao Fator
		| Termo E Fator
	"""
	termo1 = p[1]
	fator1 = p[3]
	op = tabela_aritmetica[p[2]]
	p[0] = f'{termo1}\n{fator1}\n{op}'

def p_Fator_Frase(p):
	"""
	Fator : Frase
	"""
	p[0] = p[1]

def p_Fator_Array(p):
	"""
	Fator : Var ParRetoEsq Expressao ParRetoDir
	"""
	nome = p[1]
	indice = p[3]

	if nome not in tabela_de_simbolos:
		print("erro! variavel nao declarada!")
		p[0] = None
		return

	p[0] = tabela_de_simbolos[nome]['array'][indice]

def p_Fator_Matriz(p):
	"""
	Fator : Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir 
	"""
	nome = p[1]
	indice1 = int(p[3])
	indice2 = int(p[6])

	if nome not in tabela_de_simbolos:
		print("erro! variavel nao declarada!")
		p[0] = None
		return

	p[0] = tabela_de_simbolos[nome]['matriz'][indice1][indice2]
    
def p_Fator_Par_Condicao(p):
	"""
	Fator : ParCurvoEsq Condicao ParCurvoDir
	"""
	p[0] = p[2]

def p_Negar_Fator(p):
	"""
	Fator : Negar Fator
	"""
	p[0] = f'{p[2]}\nNOT\n'

def p_Leitura(p):
	"""
	Leitura : Ler PontoVirgula
	"""
	p[0] = f'READ \n'

def p_Escrita(p):
	"""
	Escrita : Escrever ParCurvoEsq Expressao ParCurvoDir PontoVirgula
	"""
	try:
		if isinstance(int(p[3][6]), int):
			p[0] = f'{p[3]}\nWRITEI\n'
		else:
			p[0] = f'{p[3]}\n'
	except (ValueError, IndexError):
		p[0] = f'{p[3]}\n'

def p_Selecao_Se_Faz(p):
	"""
	Selecao : Se ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes PontoVirgula
	"""
	global contador_op_fluxo
	p[0] = p[3] + 'JZ '+ f'IF{contador_op_fluxo}\n' + p[6] + f'IF{contador_op_fluxo}:\n'
	contador_op_fluxo +=1
	
def p_Selecao_Se_Faz_Senao(p):
	"""
	Selecao : Se ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes Senao Instrucoes PontoVirgula
	"""
	global contador_op_fluxo
	p[0] = p[3] + 'JZ '+ f'IF{contador_op_fluxo}\n' + p[6] + f'JUMP ELSE{contador_op_fluxo}\n' + f'IF{contador_op_fluxo}:\n' + p[8] + f'ELSE{contador_op_fluxo}:\n'
	contador_op_fluxo += 1

def p_Repeticao_Enquanto(p):
	"""
	Repeticao : Enquanto ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes PontoVirgula
	"""
	global contador_op_fluxo
	condicao = p[3]
	instrucao = p[6]
	p[0] = f'WHILE{contador_op_fluxo}:\n' + condicao + 'JZ ' + f'ENDWHILE{contador_op_fluxo}\n' + instrucao + f'JUMP WHILE{contador_op_fluxo}\n' + f'ENDWHILE{contador_op_fluxo}:\n'
	contador_op_fluxo += 1

def p_Repeticao_Para(p):
	"""
	Repeticao : Para ParCurvoEsq Atribuicao PontoVirgula Condicao PontoVirgula Atribuicao ParCurvoDir Faz Instrucoes PontoVirgula
	"""
	global contador_op_fluxo
	atribuicao1 = p[3]
	condicao = p[5]
	atribuicao2 = p[7]
	instrucao = p[10]
	p[0] = condicao + f'FOR{contador_op_fluxo}:\n' + condicao + 'JZ ' + f'ENDFOR{contador_op_fluxo}\n' + instrucao + atribuicao2 + f'JUMP FOR{contador_op_fluxo}\n' + f'ENDFOR{contador_op_fluxo}:\n'
	contador_op_fluxo += 1

def p_Frase_String(p):
	"""
	Frase : String
	"""
	p[0] = f'PUSHS {p[1]}\nWRITES\n'

def p_Frase_Lista_Palavras(p):
	"""
	Frase : Lista_Palavras
	"""
	p[0] = p[1]

def p_Lista_Palavras_Palavra(p):
	"""
	Lista_Palavras : Palavra
	"""
	p[0] = p[1]

def p_Lista_Palavras(p):
	"""
	Lista_Palavras : Lista_Palavras Palavra	
	"""
	p[0] = p[1] + p[2]

def p_Palavra_Variavel(p):
	"""
	Palavra : Var
	"""
	if p[1] in tabela_de_simbolos:
		p[0] = f'PUSHG {tabela_de_simbolos[p[1]]["posicao_stack"]}'
	else:
		p[0] = p[1]
	
def p_Palavra_Num(p):
	"""
	Palavra : Num
	"""
	p[0] = f'PUSHI {p[1]}'

def p_error(p):
    print("Syntax error!")
    parser.success = False
    if p:
        print(f"Unexpected token: {p.value}")
    else:
        print("Unexpected end of input")

parser = yacc.yacc()
parser.success = True

tabela_de_simbolos = {}
contador_op_fluxo = 0
contador_pos_stack = 0
tabela_de_posicoes = []

def listar_programas():
    # Diretório onde estão os programas
    diretorio = "inputs"

    # Lista os arquivos na pasta 'inputs'
    programas = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(".txt")]

    # Mostra a lista numerada ao usuário
    print("Escolha um programa:")
    for i, programa in enumerate(programas, 1):
        print(f"{i} - {programa}")

    return programas

# Function to parse the content of a file and write the result to another file
def parse_and_write(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        # Read the content of the input file
        input_code = input_file.read()

        # Parse the content using your parser
        result = parser.parse(input_code)

        if parser.success:
            # Write the result to the output file in the outputs folder
            with open(output_filename, 'w') as output_file:
                output_file.write(result)
            print(f"Analysis successful. Result written to {output_filename}")
        else:
            print("Analysis failed. No output file generated.")

# List the programs in the 'inputs' folder
lista_programas = listar_programas()

# Choose a program
escolha = -1
while escolha < 1 or escolha > len(lista_programas):
    escolha = int(input("Digite o número do programa desejado: "))

programa_escolhido = lista_programas[escolha - 1]

# Define input and output file paths
input_path = os.path.join("inputs", programa_escolhido)
output_path = os.path.join("outputs", os.path.splitext(programa_escolhido)[0] + ".mv")

# Parse and write the result to the output file
parse_and_write(input_path, output_path)

