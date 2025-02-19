import re

class Main:
    def __init__(self):
        
        self.data = []

        self.compositores = []
        self.obras_por_periodo = {}
        self.titulos_por_periodo = {}

    def parser(self, filename):
        with open(filename, 'r') as file:
            self.data = file.read()

            struct = r'^([^;]+);"([^;]+)";([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$'

            self.data = re.findall(struct, self.data, re.MULTILINE | re.DOTALL)

            for line in self.data:
                # Lista ordenada alfabeticamente dos compositores musicais
                if line[4] not in self.compositores:
                    self.compositores.append(line[4])
                
                # Distribuição das obras por período: quantas obras catalogadas em cada período
                if line[3] not in self.obras_por_periodo:
                    self.obras_por_periodo.update({line[3]: 1})
                else:
                    self.obras_por_periodo.update({line[3]: self.obras_por_periodo[line[3]] + 1})

                # Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período
                if line[3] not in self.titulos_por_periodo:
                    self.titulos_por_periodo.update({line[3]: [line[0]]})
                else:
                    self.titulos_por_periodo[line[3]].append(line[0])
                    self.titulos_por_periodo[line[3]].sort()

            self.compositores.sort()
        


    def print_output(self):
        print("Lista de Compositores(A-Z):\n")
        for compositor in self.compositores:
            print(f"{compositor}")

        print("\n===============================================\n")

        print("Número de obras por período:\n")
        for periodo, n in self.obras_por_periodo.items():
            print(f"Período {periodo}: {n} obras")

        print("\n===============================================\n")

        print("Títulos das obras por período:\n")
        for periodo, titulos in self.titulos_por_periodo.items():
            print(f"===== Período {periodo} =====\n")
            for titulo in titulos:
                print(f"{titulo}")
            print("\n")
                

if __name__ == "__main__":
    nome_ficheiro = "obras.csv"
    main = Main()
    main.parser(nome_ficheiro)
    main.print_output()