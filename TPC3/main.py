import re
import sys

class Main:
    def __init__(self):
        self.data = []

    def parser(self, filename):
        with open(filename, 'r', encoding="utf-8") as file:
            self.data = file.readlines()
            self.data = [line.strip() for line in self.data]

    def markdown_to_html(self):
        html = []
        in_list = False

        for line in self.data:
            # Listas Numeradas (1., 2., 3., ...)
            if re.match(r'^\d+\.', line):
                if not in_list:
                    html.append('<ol>')
                    in_list = True
                line = re.sub(r'^\d+\.\s*(.*)$', r'<li>\1</li>', line)
                html.append(line)
                continue
            
            if in_list:
                html.append('</ol>')
                in_list = False

            # Cabeçalhos (#, ##, ###)
            line = re.sub(r'^# (.*)$', r'<h1>\1</h1>', line)
            line = re.sub(r'^## (.*)$', r'<h2>\1</h2>', line)
            line = re.sub(r'^### (.*)$', r'<h3>\1</h3>', line)
                
            # Negrito (**text**)
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            # Itálico (*text*)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            # Imagens ![alt](URL)
            line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', line)
            # Links [text](URL)
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                
            html.append(line)
        
        if in_list:
            html.append("</ol>")
        
        return "\n".join(html)

    def convert_and_save(self, input_file, output_file):
        self.parser(input_file)
        html_content = self.markdown_to_html()
        with open(output_file, "w") as file:
            file.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso correto: python3 main.py <input.md> <output.html>")
        sys.exit(1)

    main = Main()
    main.convert_and_save(sys.argv[1], sys.argv[2])
    print("Conversão Concluída!")