import sys
import re

class Main():

    def __init__(self):
        
        self.data = []
        self.switch = True # True = Somador On | False = Somador Off
        self.totalSum = 0

    def somadorOnOff(self):
        on = '[Oo][Nn]'
        off = '[Oo][Ff][Ff]'
        digits = '\d+'
        result = '='

        for line in self.data:
            syntax = f"(?P<on>{on})|(?P<off>{off})|(?P<digits>{digits})|(?P<result>{result})"

            catches = re.finditer(syntax, line)

            for catch in catches:
                if catch.lastgroup == 'result':
                    print(f"Soma total: {self.totalSum}\n")

                elif catch.lastgroup == 'on':
                    self.switch = True
                    print(f"Switch ON!\n")

                elif catch.lastgroup == 'off':
                    self.switch = False
                    print(f"Switch OFF!\n")

                elif catch.lastgroup == 'digits' and self.switch:
                    self.totalSum += int(catch.group('digits'))

        print("End of file!")

if __name__ == "__main__":
    main = Main()
    main.data = sys.stdin.readlines()
    main.somadorOnOff()