import re
# import sys

# # Get the file name from the command-line arguments
# if len(sys.argv) < 2:
#     print("Please provide a file name as an argument.")
#     sys.exit(1)

# file_name = sys.argv[1]

# if(file_name[-4:].lower() != '.tes'):
#     print('Your file needs to have a .tes extension')
#     sys.exit(1)

# # Open the file and do something with its contents
# try:
#     with open(file_name, 'r') as file:
#         contents = file.read()
#         # Process the file contents here
# except FileNotFoundError:
#     print(f"Error: File '{file_name}' not found.")

example = '''
fn sum(numlist as vector) <int> {
    result :: int = 0;
    for (i = 0 to length(numlist))
    begin   <%dsdasdasdasdas%>
    a = ' asd fsdfdjsjdfkll l \\n \t \\ asddda 8uujm \\  asd '
    <% asdas
    asd
    asd
    asd
    as
    d
    asd
    asdda
    s
    dasd
    asd
    asd
    %>
        result = result + numlist[i];
    end <%dsdasdasdasdas%>
    <%dsdasdasdasdas%>
    return result;
}
'''

def lex(contents):
    comment_begin = r'<%'
    comment_end = r'%>'

    begin_matches = re.finditer(comment_begin, contents)
    begin_matches_len = sum(1 for _ in begin_matches)
    end_matches = re.finditer(comment_end, contents)
    end_matches_len = sum(1 for _ in end_matches)
    
    if(begin_matches_len != end_matches_len):
        print('A comment was opened and never closed!')
    # else:
    #     i = 0
    #     for match in begin_matches:
    #         start = match.start()
    #         end = end_matches[i].end()
    #         comment = contents[start:end]
    #         new_line = r'\\n'
    #         replacement = '\n' * len(re.findall(new_line, comment))
    #         contents = contents[:start] + replacement + contents[end:]
    

    comment_pattern = r"(?s)<%.*?%>"
    
    def replacement(match):
        captured_text = match.group(0)
        newlines_count = len(re.findall(r"\n", captured_text))
        return "\n" * newlines_count

    contents = re.sub(comment_pattern, replacement, contents)
            
            

    # comment = r"(?s)<%.*?%>"
    # contents = re.sub(comment, "", contents)
            
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
    for x in line_by_line:
        column = 1
        if(x == ''):
            tokens.append([])
        while(column <= len(x)):
            if (x[column - 1] == ' '):
                column += 1
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
            elif(x[column - 1:column + 1] in DOUBLE_SYMBOLS):
                tokens.append([x[column - 1:column + 1], line, column])
                column += 2
            elif(x[column - 1] in SINGLE_SYMBOLS):
                tokens.append([x[column - 1], line, column])
                column += 1
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
        'INT':r'int',
        'VECTOR':r'vector',
        'STR':r'str',
        'BOOL':r'bool',
        'NULL':r'null',
        
        
        #User Defined
        'NUMBER':r'^\d+$',
        'ID':r'[A-Za-z]([a-z]|[A-Z]|[0-9]|\_)*',
        
        
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
    

    for token in tokens:
        if(token == []):
            continue
        else:
            for KEY, VALUE in TOKEN_DICT.items():
                if(re.search(VALUE, token[0]) != None and len(token) == 3):
                    token.append(KEY)
    
    for token in tokens:
        print(token)
        
    

lex(example)
