# Dada as seguintes regras de produção para uma gramática de uma linguagem livre de contexto, cujo símbolo não-terminal inicial é "E":
# 
# E -> TX
# X -> +TX | -TX | &
# T -> FY
# Y -> *FY | /FY | &
# F -> ( E ) | N
# N -> [+-]?([0-9][0-9]*(\.[0-9]*)?|\.[0-9][0-9]*)(e[0-9][0-9]*)?)?
# 
# 
# Linguagem ajustada:
# 
# P  -> SP'
# P' -> SP' | &
# S  -> A | E
# A  -> id = S | id(S) | E
# E  -> TE'
# E' -> +TE' | -TE' | &
# T  -> FT'
# T' -> *FT' | /FT' | &
# F  -> ( E ) | N | id
# N  -> [+-]?([0-9][0-9]*(\.[0-9]*)?|\.[0-9][0-9]*)(e[0-9][0-9]*)?)?
# id -> (([_a-zA-Z]+)([_a-zA-Z0-9]*))
# 
# Onde "&" representa a palava vazia. 
# Os símbolos terminais {+,-,*,/}, representam as operações aritméticas de adição, subtração, multiplicação e divisão. 
#
# A avaliação da expressão deve ser feita da direita para a esquerda, utilizando números com ponto flutuante.
#
# Em grupos de 3 alunos, o trabalho a ser entregue consiste em:
#
# - Alterar a gramática para incluir o operador de potenciação;
# - Alterar a gramática para incluir a utilização de identificadores nas expressões;
# - Alterar a gramática para incluir a operação de atribuição;
# - Alterar a gramática para incluir o uso de operações pré-definidas (por exemplo, sin, cos, log, sqrt);
# - Alterar a gramática para permitir a avaliação de várias expressões ;
# - Implementar um parser recursivo descendente que avalie uma lista de expressões, mostrando o resultado delas, ou erros no caso de expressões mal formadas.

from enumTokenType import *
from tokens import *
from lexer import *

# Parse P
# P  -> SP'
def parse_P(data):
    S = parse_S(data)
    P_prime = parse_P_prime(data)

    # return S + (P_prime or 0)

    if (P_prime):
        return P_prime

    return S

# Parse P'
# P' -> SP' | &
def parse_P_prime(data):
    try:
        next(data)
    except StopIteration:
        return 0

    data.put_back()

    S = parse_S(data)
    P_prime = parse_P_prime(data)

    # return S + (P_prime or 0)

    if (P_prime):
        return P_prime

    return S

# Parse S
# S  -> A | E
def parse_S(data):
    try:
        tokenType, _value, _curr, _prev = next(data)
    except StopIteration:
        raise Exception("Unexpected end of source.") from None

    data.put_back()

    if tokenType == EnumTokenType.IDENTIFIER:
        return parse_A(data)

    return parse_E(data)

# Parse A
# A -> id = S | id(S) | E
def parse_A(data):
    try:
        token, tokenId, _curr, previous = next(data)
    except StopIteration:
        raise Exception("Unexpected end of source.") from None

    if (token != EnumTokenType.IDENTIFIER):
        raise Exception("Invalid token type, expect an identifier") from None

    # get from token table
    tokenFromTable = data.tokens.getToken(tokenId)

    try:
        nextToken, _value, _curr, _prev = next(data)
    except StopIteration:
        nextToken = None

    # identifier open parentesis, is a function
    if nextToken == EnumTokenType.OPEN_PAR:
        if (tokenFromTable is None or (tokenFromTable != None and tokenFromTable['type'] != EnumTokenType.FUNCTION)):
            raise Exception("Wrong function") from None

        fn = tokenFromTable['value']
        S = parse_S(data)

        try:
            nextTokenClosePar, _value, _curr, _prev = next(data)
            if nextTokenClosePar != EnumTokenType.CLOSE_PAR:
                data.error("Unbalanced parenthesis.")
        except StopIteration:
            data.error("Unbalanced parenthesis.")

        return fn(S)

    # identifier is assignment, store value on token table
    if nextToken == EnumTokenType.ASSIGNMENT:
        if (tokenFromTable != None and tokenFromTable['type'] == EnumTokenType.FUNCTION):
            raise Exception("Is not possible overwrite a function") from None

        S = parse_S(data)

        # save identifier in token table
        data.tokens.addToken(tokenId, EnumTokenType.IDENTIFIER, S)

        return S

    data.put_back(previous) # returns to token idenfier

    return parse_E(data)

# Parse E
# E -> TE'
def parse_E(data):
    T = parse_T(data)
    E_prime = parse_E_prime(data)

    return T + (E_prime or 0)
    
# Parse E'
# E' -> +TE' | -TE' | &
def parse_E_prime(data):
    try:
        token, operator, _curr, _prev = next(data)
    except StopIteration:
        return 0

    if token == EnumTokenType.OPERATOR and operator in "+-":
        T = parse_T(data)
        E_prime = parse_E_prime(data)

        return (T if operator == "+" else -1 * T) + (E_prime or 0)

    # if token not in [EnumTokenType.OPERATOR, EnumTokenType.OPEN_PAR, EnumTokenType.CLOSE_PAR, EnumTokenType.IDENTIFIER, EnumTokenType.ASSIGNMENT, EnumTokenType.DELIMITER]:
        # data.error(f"Invalid character: {operator}")

    data.put_back()

    return 0

# Parse T
# T -> FT'
def parse_T(data):
    F = parse_F(data)
    T_prime = parse_T_prime(data)

    return F * (T_prime or 1)

# Parse T'
# T' -> *FT' | /FT' | &
def parse_T_prime(data):
    try:
        token, operator, _curr, _prev = next(data)
    except StopIteration:
        return 1

    if token == EnumTokenType.OPERATOR and operator in "*/":
        F = parse_F(data)
        T_prime = parse_T_prime(data)

        return (F if operator == "*" else 1 / F) * T_prime

    # if token not in [EnumTokenType.OPERATOR, EnumTokenType.OPEN_PAR, EnumTokenType.CLOSE_PAR, EnumTokenType.IDENTIFIER, EnumTokenType.ASSIGNMENT, EnumTokenType.DELIMITER]:
        # data.error(f"Invalid character: {operator}")

    data.put_back()

    return 1

# Parse F
# F -> ( E ) | N
def parse_F(data):
    try:
        token, value, _curr, _prev = next(data)
    except StopIteration:
        raise Exception("Unexpected end of source.") from None

    if token == EnumTokenType.OPEN_PAR:
        E = parse_E(data)

        try:
            nextTokenClosePar, _value, _curr, _prev = next(data)
            if nextTokenClosePar != EnumTokenType.CLOSE_PAR:
                data.error("Unbalanced parenthesis.")
        except StopIteration:
            data.error("Unbalanced parenthesis.")

        return E

    if token == EnumTokenType.IDENTIFIER:
        # get from token table
        tokenFromTable = data.tokens.getToken(value)

        if (tokenFromTable is None or (tokenFromTable != None and tokenFromTable['type'] != EnumTokenType.IDENTIFIER)):
            raise Exception("Wrong identifier") from None

        return float(tokenFromTable['value'])

    if token == EnumTokenType.NUMBER:
        return float(value)

    raise data.error(f"Unexpected token: {value}.")

# -------------------------------------------------------------------------

def parser(source_code):
    tokens = Tokens()
    lexer = Lexer(source_code, tokens)

    return parse_P(lexer)
