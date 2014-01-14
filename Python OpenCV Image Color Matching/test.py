import ply.lex as lex
import ply.yacc as yacc

# List of token names.
tokens = (
   'LAMBDA',
   'DOT',
   'LPAREN',
   'RPAREN',
   'IDENTIFIER',
)

# Regular expression rules for simple tokens
t_LAMBDA  = r'\^'
t_DOT     = r'\.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-z]'
    t.value = str(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def p_expression_lambda(p):
    'expression : LAMBDA IDENTIFIER DOT expression'

def p_expression_left_right_paren(p):
    'expression : term expression'

def p_expression_identifier_term(p):
    'expression : LPAREN expression RPAREN'

def p_expression_identifier_term1(p):
    'expression : IDENTIFIER'

def p_term_lambda(p):
    'term : LAMBDA IDENTIFIER DOT expression term'

def p_term_left_right_paren(p):
    'term : LPAREN expression RPAREN term'

def p_term_identifier_term(p):
    'term : IDENTIFIER term'

def p_term_empty(p):
    'term :'
    pass


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   parser.parse(s)