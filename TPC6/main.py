import ply.lex as lex
import ply.yacc as yacc

tokens = ('NUM', 'PA', 'PF', 'SUM', 'SUB', 'MUL', 'DIV')

t_ignore = ' \t'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PA(t):
    r'\('
    return t

def t_PF(t):
    r'\)'
    return t

def t_SUM(t):
    r'\+'
    return t

def t_SUB(t):
    r'-'
    return t

def t_MUL(t):
    r'\*'
    return t

def t_DIV(t):
    r'/'
    return t

def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def match(self, expected_type):
        if self.current_token and self.current_token.type == expected_type:
            value = self.current_token.value
            self.next_token()
            return value
        else:
            raise SyntaxError(f"Erro de sintaxe: esperado {expected_type}, encontrado {self.current_token}")

    def expr(self):
        result = self.term()
        while self.current_token and self.current_token.type in ('SUM', 'SUB'):
            if self.current_token.type == 'SUM':
                self.match('SUM')
                result += self.term()
            elif self.current_token.type == 'SUB':
                self.match('SUB')
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            if self.current_token.type == 'MUL':
                self.match('MUL')
                result *= self.factor()
            elif self.current_token.type == 'DIV':
                self.match('DIV')
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Divisão por zero")
                result /= divisor
        return result

    def factor(self):
        if self.current_token.type == 'NUM':
            return self.match('NUM')
        elif self.current_token.type == 'PA':
            self.match('PA')
            result = self.expr()
            self.match('PF')
            return result
        else:
            raise SyntaxError(f"Erro de sintaxe: fator inesperado {self.current_token}")

def avaliar_expressao(expressao):
    lexer.input(expressao)
    tokens = [tok for tok in lexer]
    parser = Parser(tokens)
    return parser.expr()

expressoes = [
    "2+3",
    "67-(2+3*4)",
    "(9-2)*(13-4)"
]

for exp in expressoes:
    try:
        resultado = avaliar_expressao(exp)
        print(f"{exp} = {resultado}")
    except Exception as e:
        print(f"Erro ao avaliar '{exp}': {e}")