import sys

# Get the file name from the command-line arguments
if len(sys.argv) < 2:
    print("Please provide a file name as an argument.")
    sys.exit(1)

file_name = sys.argv[1]

# Open the file and do something with its contents
try:
    with open(file_name, 'r') as file:
        contents = file.read()
        # Process the file contents here
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")