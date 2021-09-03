def parse_DECLARATION():
    print("DECLAREITN")

def parse_FUNCTION():
    print("FUNCTIN")



intrepret_functions = {
    "DECLARATION": parse_DECLARATION(),
    "FUNCTION": parse_FUNCTION(),
}


class Interpreter:
    def __init__(self):
        self.variables = {}
    

    def interpret(self, parsed_tokens):
        for token in parsed_tokens:
            print(token.tag)

    
