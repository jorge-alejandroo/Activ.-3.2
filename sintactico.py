import ply.yacc as yacc
from lexico import tokens, lexico  # Asegúrate de que los tokens y el análisis léxico estén correctamente implementados

# Reglas para el analizador sintáctico

def p_program(p):
    '''program : main_block'''
    p[0] = p[1]

def p_main_block(p):
    '''main_block : PR ID PI PD LLI int_declaration LLD'''
    if p[1] == 'int' and p[2] == 'main':  # Revisamos directamente el valor del token
        p[0] = ('programa', 'Correcto')
    else:
        raise SyntaxError(f"Error en el bloque principal en la línea")

def p_int_declaration(p):
    '''int_declaration : PR ID PC'''
    # Verificamos si la declaración es del tipo "int x;"
    if p[1] == 'int' and p[2] == 'x':
        p[0] = ('declaracion', 'Correcto')
    else:
        raise SyntaxError(f"Error en la declaración de variable en la línea")

# Manejador de errores sintácticos
def p_error(p):
    if not p:
        # Si no hay token disponible, el error ocurre al final del archivo
        resultado.append({'linea': '-', 'tipo': '-', 'escritura': "Error de sintaxis: falta }"})
    else:
        # Este es el token que causó el error
        error_token = p.value
        # Obtener un mensaje de qué se esperaba antes de este token
        expected_token = expected_token_message(p)
        error_message = f"Error de sintaxis: Se esperaba: {expected_token}"
        resultado.append({'tipo': p.type, 'escritura': error_message})

# Función para mostrar qué token se esperaba en caso de error
def expected_token_message(p):
    if p.type == 'LLI':  # Se esperaba una llave de apertura '{'
        return "'{' después de ')'"
    elif p.type == 'PR':  # Se esperaba una palabra reservada (como 'int')
        return "'{' antes de ')'"
    elif p.type == 'ID':  # Se esperaba un identificador (como 'x')
        if p.value == 'main':
            return "'main' después de 'int'"
        else:
            return "'x' despues de int "
    elif p.type == 'PC':  # Se esperaba un punto y coma
        return "';' despues de x"
    elif p.type == 'PI':  # Se esperaba un paréntesis de apertura
        return "'(' después de 'main'"
    elif p.type == 'PD':  # Se esperaba un paréntesis de cierre
        return "')' antes de '{'"
    elif p.type == 'LLD':  # Se esperaba una llave de cierre '}'
        return "'}' despues de ;"
    else:
        return "un token válido"

# Crear el parser
parser = yacc.yacc()

def analizar_sintaxis(entrada):
    global resultado
    resultado = []
    try:
        # Realizamos primero el análisis léxico
        tokens = lexico(entrada)  # Esta función debe estar definida previamente
        # Luego, realizamos el análisis sintáctico
        parser.parse(entrada)

        # Recorremos los tokens para generar resultados
        for token in tokens:
            if token['valor'].lower() in ['int', 'main', 'x']:
                resultado.append({'linea': token['linea'], 'tipo': token['valor'], 'escritura': 'Correcto'})
            elif token['valor'] in ['(', ')', '{', '}', ';']:
                resultado.append({'linea': token['linea'], 'tipo': token['valor'], 'escritura': token['tipo']})
            else:
                resultado.append({'linea': token['linea'], 'tipo': token['valor'], 'escritura': 'Incorrecto'})
    except SyntaxError as e:
        error_message = f"Error de sintaxis: {e}"
        resultado.append({'linea': '-', 'tipo': '-', 'escritura': error_message})
    
    return resultado





