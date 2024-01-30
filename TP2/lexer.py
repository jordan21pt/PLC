import ply.lex as lex
import sys

tokens = (
    'Inicio','Fim','Num','PontoVirgula','ParRetoEsq',
    'ParRetoDir','Soma','Subtracao','Multiplicacao','Divisao','ParCurvoEsq',
    'ParCurvoDir','Ler','Escrever','Se','Faz','Senao','Enquanto','Para','E','OU',
    'Negar','Diferente','Vale','Igual','MenorIgual','MaiorIgual','Menor','Maior',
    'Tipo','Var','String')

# Regras léxicas:

def t_Inicio(t):
    r'Inicio'
    print(f"Recognized Inicio: {t.value}")
    return t

def t_Fim(t):
    r'Fim'
    print(f"Recognized Fim: {t.value}")
    return t

def t_Tipo(t):
    r'int'
    print(f"Recognized int: {t.value}")
    return t

def t_Num(t):
    r'[+\-]?\d+'
    print(f"Recognized num: {t.value}")
    return t

def t_PontoVirgula(t):
    r'\;'
    print(f"Recognized PontoVirgula: {t.value}")
    return t

def t_ParRetoEsq(t):
    r'\['
    print(f"Recognized ParRetoEsq: {t.value}")
    return t

def t_ParRetoDir(t):
    r'\]'
    print(f"Recognized ParRetoDir: {t.value}")
    return t

def t_Soma(t):
    r'\+'
    print(f"Recognized Soma: {t.value}")
    return t

def t_Subtracao(t):
    r'\-'
    print(f"Recognized Subtracao: {t.value}")
    return t

def t_Multiplicacao(t):
    r'\*'
    print(f"Recognized Multiplicacao: {t.value}")
    return t

def t_Divisao(t):
    r'\/'
    print(f"Recognized Divisao: {t.value}")
    return t

def t_ParCurvoEsq(t):
    r'\('
    print(f"Recognized ParCurvoEsq: {t.value}")
    return t

def t_ParCurvoDir(t):
    r'\)'
    print(f"Recognized ParCurvoDir: {t.value}")
    return t

def t_Ler(t):
    r'Ler'
    print(f"Recognized Ler: {t.value}")
    return t

def t_Escrever(t):
    r'Escrever'
    print(f"Recognized Escrever: {t.value}")
    return t

def t_Senao(t):
    r'Senao'
    print(f"Recognized Senao: {t.value}")
    return t

def t_Se(t):
    r'Se'
    print(f"Recognized Se: {t.value}")
    return t

def t_Faz(t):
    r'Faz'
    print(f"Recognized Faz: {t.value}")
    return t

def t_Enquanto(t):
    r'Enquanto'
    print(f"Recognized Enquanto: {t.value}")
    return t

def t_Para(t):
    r'Para'
    print(f"Recognized Para: {t.value}")
    return t

def t_E(t):
    r'E'
    print(f"Recognized E: {t.value}")
    return t

def t_OU(t):
    r'OU'
    print(f"Recognized OU: {t.value}")
    return t

def t_Negar(t):
    r'Negar'
    print(f"Recognized Negar: {t.value}")
    return t

def t_Diferente(t):
    r'\!\='
    print(f"Recognized Diferente: {t.value}")
    return t

def t_Igual(t):
    r'\=\='
    print(f"Recognized Igual: {t.value}")
    return t

def t_Vale(t):
    r'\='
    print(f"Recognized Vale: {t.value}")
    return t

def t_MaiorIgual(t):
    r'\>\='
    print(f"Recognized MaiorIgual: {t.value}")
    return t

def t_MenorIgual(t):
    r'\<\='
    print(f"Recognized MenorIgual: {t.value}")
    return t

def t_Maior(t):
    r'\>'
    print(f"Recognized Maior: {t.value}")
    return t

def t_Menor(t):
    r'\<'
    print(f"Recognized Menor: {t.value}")
    return t

def t_String(t):
    r'"([^"]|(\\n))*"'
    print(f'Recognized String: {t.value}')
    return t

def t_Var(t):
    r'[a-zA-Z]\w*'
    print(f"Recognized Var: {t.value}")
    return t


t_ignore = ' \n\t'

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input("1+2")
