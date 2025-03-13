import re
import sys
import json
import ply.lex as lex
from datetime import datetime


class Product:
    def __init__(self, code, name, stock, price):
        self.code = code
        self.name = name
        self.stock = stock
        self.price = price

    def __str__(self):
        return f"{self.code} - {self.name} - {self.stock} - {self.price}"
    
DB = "db.json"
MOEDAS = {"2e": 2.0, "1e": 1.0, "50c": 0.5, "20c": 0.2, "10c": 0.1, "5c": 0.05, "2c": 0.02, "1c": 0.01}

tokens = (
    'SAIR', 'LISTAR', 'MOEDA', 'SELECIONAR', 'SALDO'
)

t_SAIR = r'SAIR'
t_LISTAR = r'LISTAR'
t_MOEDA = r'MOEDA'
t_SELECIONAR = r'SELECIONAR'
t_SALDO = r'SALDO'

t_ignore = ' \t\n'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
    
class Main:
    def __init__(self):
        self.stock = []
        self.balance = 0.0

    def load_stock(self):
        try:
            with open(DB, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.stock = [Product(item["cod"], item["nome"], item["quantidade"], item["preco"]) for item in data]

                print(f"maq: {datetime.now().date()}, Stock carregado, Estado atualizado.")
                print("maq: Bom dia. Estou disponível para atender o seu pedido.")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar o stock: {e}")
        
    def format_price(self, price):
        euros = int(price)
        cents = int(round((price - euros) * 100))
        if euros > 0 and cents > 0:
            return f"{euros}e{cents}c"
        elif euros > 0:
            return f"{euros}e"
        else:
            return f"{cents}c"
        
    def listar_stock(self):
        print("\nmaq:")
        print("cod | nome | quantidade | preço")
        print("---------------------------------")
        for product in self.stock:
            print(product.__str__())

    def inserir_moeda(self, moedas):
        for moeda in moedas:
            if moeda in MOEDAS:
                self.balance += MOEDAS[moeda]
            else:
                print(f"maq: Moeda inválida: {moeda}")
        print(f"maq: Saldo = {self.format_price(self.balance)}")

    def selecionar_produto(self, code):
        for product in self.stock:
            if product.code == code:
                if product.stock > 0:
                    if self.balance >= product.price:
                        self.balance -= product.price
                        product.stock -= 1
                        print(f"maq: Pode retirar o produto dispensado {product.name}.")
                        print(f"maq: Saldo = {self.format_price(self.balance)}")
                    else:
                        print(f"Saldo insufuciente para satisfazer o seu pedido")
                        print(f"maq: Saldo = {self.format_price(self.balance)}; Pedido = {self.format_price(product.price)}")
                else:
                    print(f"maq: Produto {product.name} esgotado!")
                return
        print("maq: Produto não encontrado.")

    def salvar_stock(self):
        try:
            data_to_save = [{
                "cod": product.code,
                "nome": product.name,
                "quantidade": product.stock,
                "preco": product.price
            } for product in self.stock]

            with open(DB, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        except IOError as e:
            print(f"Erro ao salvar o stock: {e}")

    def sair(self):
        self.salvar_stock()
        if self.balance > 0:
            troco = self.format_price(self.balance)
            print(f"maq: Pode retirar o troco: {troco}")

        print("maq: Até à próxima.")

    def run(self):
        self.load_stock()

        while True:
            user_input = input("\n>> ")
            lexer.input(user_input)

            for tok in lexer:
                if tok.type == 'SAIR':
                    self.sair()
                    return
                elif tok.type == 'LISTAR':
                    self.listar_stock()
                elif tok.type == 'MOEDA':
                    moedas = re.findall(r'[0-9]+[e,c]{1}', user_input)
                    self.inserir_moeda(moedas)
                elif tok.type == 'SELECIONAR':
                    self.selecionar_produto(user_input.split()[1])
                elif tok.type == 'SALDO':
                    print(f"maq: Saldo = {self.format_price(self.balance)}")
                else:
                    print("maq: Comando não reconhecido.")
        
if __name__ == "__main__":
    main = Main()
    main.run()