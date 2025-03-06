import re
from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    VARIABLE = "VARIABLE"
    PREFIX = "PREFIX"
    LITERAL = "LITERAL"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    COMMENT = "COMMENT"

TOKEN_PATTERNS = [
    (TokenType.KEYWORD, r"\b(select|where|LIMIT)\b"),
    (TokenType.VARIABLE, r"\?[a-zA-Z_][a-zA-Z0-9_]*"),
    (TokenType.PREFIX, r"\b(dbo:|foaf:)\w+"),
    (TokenType.LITERAL, r'"[^"@]+"(?:@[a-z]{2})?'),
    (TokenType.OPERATOR, r"\."),
    (TokenType.DELIMITER, r"[{}]"),
    (TokenType.NUMBER, r"\b\d+\b"),
    (TokenType.IDENTIFIER, r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    (TokenType.COMMENT, r"\#[^\n]+")
]

class Lexer:
    def __init__(self, query):
        self.query = query
        self.tokens = []
    
    def tokenize(self):
        pos = 0
        match = None
        while pos < len(self.query):
            for token_type, pattern in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.query, pos)
                if match:
                    self.tokens.append((token_type, match.group()))
                    pos = match.end()
                    break
            if not match:
                pos += 1
        return self.tokens

if __name__ == "__main__":
    query = """
    # DBPedia: obras de Chuck Berry
    
    select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
    } LIMIT 1000
    """
    
    lexer = Lexer(query)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
