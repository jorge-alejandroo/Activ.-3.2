import ply.lex as lex

# Lista de tokens
tokens = (
    'ID',
    'PR',
    'PC',   # Punto y coma
    'LLI',  # Llave izquierda
    'LLD',  # Llave derecha
    'PI',   # Paréntesis izquierdo
    'PD',   # Paréntesis derecho
)

# Lista de palabras reservadas
reserved = {
    'int': 'PR',
    'main': 'ID',  # Lo manejas como identificador
    'for': 'PR'
}

# Reglas de expresiones regulares para los tokens
def t_PR(t):
    r'int|for'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es una palabra reservada
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores
    t.type = reserved.get(t.value, 'ID')  # Si no es reservada, es ID
    return t

def t_PC(t):
    r';'
    return t

def t_LLI(t):
    r'\{'
    return t

def t_LLD(t):
    r'\}'
    return t

def t_PI(t):
    r'\('
    return t

def t_PD(t):
    r'\)'
    return t

# Manejo de saltos de línea para contar las líneas del código
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de espacios en blanco y tabulaciones
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Crear el analizador léxico
def create_lexer():
    return lex.lex()

# Función de análisis léxico
def lexico(text):
    lexer = create_lexer()
    lexer.input(text)
    lexemes = []

    # Procesar cada token en el texto
    for tok in lexer:
        lexeme = {
            'linea': tok.lineno, 
            'tipo': tok.type, 
            'valor': tok.value
        }
        lexemes.append(lexeme)
    
    return lexemes



