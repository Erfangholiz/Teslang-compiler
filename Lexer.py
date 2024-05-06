import re
import sys

#Run the program as such: python Lexer.py code.tes

# Get the file name from the command-line arguments
if len(sys.argv) < 2:
    print("Please provide a file name as an argument.")
    sys.exit(1)

file_name = sys.argv[1]

if(file_name[-4:].lower() != '.tes'):
    print('Your file needs to have a .tes extension')
    sys.exit(1)

# Open the file and do something with its contents
try:
    with open(file_name, 'r') as file:
        text = file.read()
        # Process the file contents here
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")


def lex(contents):
    #Check to see if there are any comments left open
    # comment_begin = r'<%'
    # comment_end = r'%>'

    # begin_matches = re.finditer(comment_begin, contents)
    # begin_matches_len = sum(1 for _ in begin_matches)
    # end_matches = re.finditer(comment_end, contents)
    # end_matches_len = sum(1 for _ in end_matches)
    
    # if(begin_matches_len != end_matches_len):
    #     print('Lexical Error: The number of closed and opened comments don\'t match!')
    #     exit()
    # else:
    #     i = 0
    #     for match in begin_matches:
    #         start = match.start()
    #         end = end_matches[i].end()
    #         comment = contents[start:end]
    #         new_line = r'\\n'
    #         replacement = '\n' * len(re.findall(new_line, comment))
    #         contents = contents[:start] + replacement + contents[end:]
    
    #Replace every comment with whitespace
    # comment_pattern = r'<%([^(<%)(%>)]|<%([^(<%)(%>)])*%>|\n | \t | \\ | \' | \")*%>'
    
    # def replacement(match):
    #     captured_text = match.group(0)
    #     newlines_count = len(re.findall(r"\n", captured_text))
    #     return "\n" * newlines_count

    # contents = re.sub(comment_pattern, replacement, contents)
    count = 0
    new_line_counter = 0
    for i in range(len(contents)):
        if contents[i:i+2] == '<%':
            if count == 0:
                start_comment = i
            count += 1
        if count > 0 and contents[i] == '\n':
            new_line_counter += 1
        if contents[i:i+2] == '%>':
            count -= 1
            if count == 0:
                contents = contents[:start_comment] + ' ' * ((i+2) - start_comment - 2 * new_line_counter) + new_line_counter * '\n' + contents[i+2:]
                new_line_counter = 0
        
    if count != 0:
        print('Lexical Error: The number of closed and opened comments don\'t match!')
        exit()

    # comment = r"(?s)<%.*?%>"
    # contents = re.sub(comment, "", contents)
          
    #Tokenization start
    line = 1
    tokens = []
    line_by_line = list(contents.split('\n'))
    SINGLE_SYMBOLS = ('(',
               ')',
               '-',
               '+',
               '=',
               ':',
               ';',
               '<',
               '>',
               '[',
               ']',
               '{',
               '}',
               '%',
               '*',
               '/',
               '?',
               '!',
               '#'
               )
    DOUBLE_SYMBOLS = ('::',
                      '||',
                      '==',
                      '<=',
                      '>=',
                      '!=',
                      '&&'
    )
    #Going through the code line by line
    for x in line_by_line:
        column = 1
        #Accounting for empty lines
        if(x == ''):
            tokens.append([])
        while(column <= len(x)):
            #Accounting for whitespace
            if (x[column - 1] == ' '):
                column += 1
            #Tokenizing strings and throwing lexical errors if they don't close properly
            elif(x[column - 1] == "'"):
                string_pattern = r'\'[\d | \D | \n | \t | \\ | \' | \"]*\''
                try:
                    tokens.append([re.search(string_pattern,x[column - 1:]).group(), line, column, 'STRING'])
                    column += re.search(string_pattern,x[column - 1:]).span()[1] - re.search(string_pattern,x[column - 1:]).span()[0]
                except AttributeError:
                    print(f'Lexical error: Faulty string at line: {line} column: {column}')
                    exit()
            elif(x[column - 1] == '"'):
                string_pattern = r'\"[\d | \D | \n | \t | \\ | \' | \"]*\"'
                try:
                    tokens.append([re.search(string_pattern,x[column - 1:]).group(), line, column, 'STRING'])
                    column += re.search(string_pattern,x[column - 1:]).span()[1] - re.search(string_pattern,x[column - 1:]).span()[0]
                except AttributeError:
                    print(f'Lexical error: Faulty string at line: {line} column: {column}')
                    exit()
            #Tokenizing symbols
            elif(x[column - 1:column + 1] in DOUBLE_SYMBOLS):
                tokens.append([x[column - 1:column + 1], line, column])
                column += 2
            elif(x[column - 1] in SINGLE_SYMBOLS):
                tokens.append([x[column - 1], line, column])
                column += 1
            #Tokenizing words
            else:
                tokens.append([])
                new_token = ''
                new_token_line = line
                new_token_column = column
                while(column <= len(x) and x[column - 1] != ' ' and x[column - 1] not in SINGLE_SYMBOLS):
                    new_token += x[column - 1]
                    column += 1
                tokens[-1].extend([new_token, new_token_line, new_token_column])
        line += 1

    #A dictionary of all tokens and their RegEx
    TOKEN_DICT = {
        #Key Words
        'FN':r'^fn$',
        'AS':r'^as$',
        'FOR':r'^for$',
        'TO':r'^to$',
        'LEN':r'^length$',
        'RETURN':r'^return$',
        'IF':r'^if$',
        'BEGIN':r'^begin$',
        'END':r'^end$',
        'ELSE':r'^else$',
        'DO':r'^do$',
        'WHILE':r'^while$',
        'SCAN':r'^scan$',
        'PRINT':r'^print$',
        'LIST':r'^list$',
        'EXIT':r'^exit$',
        
        
        #Data Types
        'INT':r'^int$',
        'VECTOR':r'^vector$',
        'STR':r'^str$',
        'BOOL':r'^bool$',
        'NULL':r'^null$',
        
        
        #User Defined
        'NUMBER':r'^\d+$',
        'ID':r'^[A-Za-z]([a-z]|[A-Z]|[0-9]|\_)*$',
        
        
        #Double Symbols
        'IFEQUAL':r'==',
        'BEQUAL':r'>=',
        'SEQUAL':r'<=',
        'NEQUAL':r'!=',
        'OR':r'\|\|',
        'AND':r'&&',
        'DBL_COLON':r'::',
        
        
        #Single Symbols
        'PLUS':r'\+',
        'MINUS':r'\-',
        'MULTIPLY':r'\*',
        'DIVIDE':r'/',
        'LPAREN':r'\(',
        'RPAREN':r'\)',
        'SEMI_COLON':r'\;',
        'EQ':r'\=',
        'LCURLYBR':r'\}',
        'RCURLYBR':r'\{',
        'GREATER_THAN':r'\>',
        'LESS_THAN':r'\<',
        'LSQUAREBR':r'\[',
        'RSQUAREBR':r'\]',
        'HASHTAG':r'\#',
        'QUESTION':r'\?',
        'PERCENT':r'%',
        'EXCLAMATION':r'!',
        'COLON':r':'
    }
    
    #Labeling each token
    for token in tokens:
        if(token == []):
            continue
        else:
            for KEY, VALUE in TOKEN_DICT.items():
                if(re.search(VALUE, token[0]) != None and len(token) == 3):
                    token.append(KEY)
            if(len(token) == 3):
                #Accounting for identifiers starting with non-english characters
                print(f'Lexical Error: Erroneous identifier at line {token[1]} column {token[2]}')
                exit()
    
    output = '''
      Line      |    Column      |    Token      |    Value      
________________________________________________________________
'''
    for token in tokens:
        if(token == []):
            continue
        a = '        '
        b = 8 - len(str(token[1]))
        c = 8 - len(str(token[2]))
        d = 13 - len(token[3])
        output += f'{a}{str(token[1])}{" " * b}|{a}{str(token[2])}{" " * c}|  {token[3]}{" " * d}|   {token[0]}\n'
    print(output)
        
    

lex(text)
