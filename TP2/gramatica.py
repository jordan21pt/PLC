import ply.yacc as yacc
import sys

from lexer import tokens

## incio da GIC

def p_lisp_grammar(p):
    """
    Programa : Inicio Corpo Fim
    Corpo : Declaracoes Instrucoes
    Declaracoes : Declaracoes Declaracao
        | 
    Declaracao : Tipo Var PontoVirgula
        | Tipo Var ParRetoEsq Expressao ParRetoDir PontoVirgula
        | Tipo Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir PontoVirgula
    Instrucoes : Instrucoes Instrucao
        | 
    Instrucao : Atribuicao
        | Leitura
        | Escrita
        | Selecao
        | Repeticao
    Atribuicao : Var Vale Expressao PontoVirgula
               | Var ParRetoEsq Expressao ParRetoDir Vale Expressao PontoVirgula
               | Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir Vale Expressao PontoVirgula
    Condicao : Expressao
        | Expressao Igual Expressao
        | Expressao Diferente Expressao
        | Expressao MenorIgual Expressao
        | Expressao MaiorIgual Expressao
        | Expressao Menor Expressao
        | Expressao Maior Expressao
    Expressao : Termo
        | Expressao Soma Termo
        | Expressao Subtracao Termo
        | Expressao OU Termo
    Termo : Fator
        | Termo Multiplicacao Fator
        | Termo Divisao Fator
        | Termo E Fator
    Fator : Frase
        | Var ParRetoEsq Expressao ParRetoDir
        | Var ParRetoEsq Expressao ParRetoDir ParRetoEsq Expressao ParRetoDir 
        | ParCurvoEsq Condicao ParCurvoDir
        | Negar Fator
    Leitura : Ler ParCurvoEsq Expressao ParCurvoDir PontoVirgula
    Escrita : Escrever ParCurvoEsq Expressao ParCurvoDir PontoVirgula
    Selecao : Se ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes PontoVirgula
        | Se ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes Senao Instrucoes PontoVirgula
    Repeticao : Enquanto ParCurvoEsq Condicao ParCurvoDir Faz Instrucoes PontoVirgula
        | Para ParCurvoEsq Atribuicao PontoVirgula Condicao PontoVirgula Atribuicao ParCurvoDir Faz Instrucoes PontoVirgula
    Frase : String
        | Lista_Palavras
    Lista_Palavras : Palavra
                | Lista_Palavras Palavra
    Palavra : Var
        | Num
    """

def p_error(p):
    parser.success = False
    print(f'Syntax error at token {p.value} (line {p.lineno}, position {p.lexpos})')


###inicio do parsing
parser = yacc.yacc()

# Leia o arquivo de entrada
with open('inputs/not.txt', 'r') as file:
    input_code = file.read()

# Tente analisar o código
result = parser.parse(input_code)

if result:
    print('Parsing bem-sucedido!')
