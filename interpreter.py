from parse import Parser
parser = Parser()

class Interpreter:
    def __init__(self, parsed_tokens):
        self.parsed_tokens = parsed_tokens
        self.variables = {}
        self.intrepret_functions = {
            "DECLARATION": self.parse_DECLARATION,
            "FUNCTION": self.parse_FUNCTION,
            "BLOCK": self.parse_BLOCK,
            "BIN OP": self.parse_BIN_OP,
        }
    

    def interpret(self, parsed_tokens):
        for token in parsed_tokens:
            self.intrepret_functions[token.tag](token)
    
    def parse_DECLARATION(self, token):
        self.variables[token.name] = token.value


    def parse_FUNCTION(self, token):
        if token.name == "PRINT":
            result = ""
            for op in token.parameters:
                if op.name == "STRING":result += op.code
                elif op.name == "NUMBER": result += str(op.code)
                elif op.name == "VARIABLE":result += str(self.return_variable(op.code))

            print(result)

        elif token.name in ("INPUT", "INT INPUT"):
            variable = token.parameters[0].code
            self.variables[variable] = input(variable+":") if token.name == "INPUT" else self.handle_int_input(variable)


    def handle_int_input(self,variable):
        while True:
            try:
                return int(input(variable+":"))
            except:
                pass


    def parse_BLOCK(self, token):
        if token.name == "IF":
            self.parse_IF(token)
        elif token.name == "WHILE":
            self.parse_WHILE(token)



    def parse_WHILE(self, token):
        run = self.parse_CONDITION(token)    
        #parsed_code = parser.parse([token.code])
        
        while run:
            self.interpret(token.code)
            run = self.parse_CONDITION(token)


    def parse_IF(self, token):
        run = self.parse_CONDITION(token)
        #parsed_code = parser.parse([token.code])

        if run:
            self.interpret(token.code)


    def parse_CONDITION(self,token):
        condition = token.condition
        left_val = self.return_variable(condition.left.code) if condition.left.name == "VARIABLE" else condition.left.code 
        right_val = self.return_variable(condition.right.code) if condition.right.name == "VARIABLE" else condition.right.code 

        run = False
        if condition.name in ("EQUAL","EQUIVALENT"): run = left_val == right_val
        elif condition.name == "NOT EQUIVALENT": run = left_val != right_val
        elif condition.name == "LESS": run = left_val < right_val
        elif condition.name == "LESS EQUIVALENT": run = left_val <= right_val
        elif condition.name == "GREATER": run = left_val > right_val
        elif condition.name == "GREATER EQUIVALENT": run = left_val >= right_val
        
        return run


    def parse_BIN_OP(self, token):
        left_val = self.return_variable(token.left.code) if token.left.name == "VARIABLE" else token.left.code
        right_val = self.return_variable(token.right.code) if token.right.name == "VARIABLE" else token.right.code

        if token.name == "ADD": self.variables[token.left.code] = int(left_val + right_val)
        elif token.name == "MINUS": self.variables[token.left.code] = int(left_val - right_val)
        elif token.name == "MULTIPLY": self.variables[token.left.code] = int(left_val * right_val)
        elif token.name == "DIVIDE": self.variables[token.left.code] = int(left_val / right_val)
        elif token.name == "EQUAL": self.variables[token.left.code] = int(right_val)


        
    def return_variable(self,name):
        return self.variables[name]
