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

contents = '''
fn sum(numlist as vector) <int> {
    result :: int = 0;
    
    for (i = 0 to length(numlist))
    begin   <%dsdasdasdasdas%>
        result = result + numlist[i];
    end
    
    return result;
}
'''
line = 1
tokens = []
line_by_line = list(contents.split('\n'))
SINGLE_SYMBOLS = ('(',
           ')',
           '-',
           '+',
           '=',
           '"',
           "'",
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
           '!'
           )
DOUBLE_SYMBOLS = ('::',
                  '||',
                  '==',
                  '<=',
                  '>=',
                  '!='
)
for x in line_by_line:
    column = 1
    if(x == ''):
        tokens.append([])
    while(column <= len(x)):
        if (column <= len(x) and x[column - 1] == ' '):
            column += 1
        elif(column <= len(x) and x[column - 1:column + 1] == '<%'):
            while(column <= len(x) and x[column - 1:column] != '%>'):
                column += 1
        elif(column <= len(x) and x[column - 1:column + 1] in DOUBLE_SYMBOLS):
            tokens.append([x[column - 1:column + 1], line, column])
            column += 2
        elif(column <= len(x) and x[column - 1] in SINGLE_SYMBOLS):
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

for token in tokens:
    print(token)


