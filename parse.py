class BinOpToken:
    def __init__(self, name=None, left=None, right=None):
        self.name = name
        self.tag = "BIN OP"
        self.left = left
        self.right = right


class FuncToken:
    def __init__(self,name, parameters=None):
        self.tag = "FUNCTION"
        self.name = name
        self.parameters = parameters


class BlockToken:
    def __init__(self, name=None, condition=None, code=None):
        self.name = name
        self.condition = condition
        self.code = code
        self.tag = "BLOCK"


class VarToken:
    def __init__(self,name, value):
        self.name = name
        self.value = value
        self.tag = "DECLARATION"


class Parser:
    def __init__(self):
        pass


    def parse(self, tokens):
        self.print_tokens(tokens)
        parsed_tokens = []

        for i,line in enumerate(tokens):
            for operation in line:
                if operation.name in ("WHILE","IF"):
                    blockToken = self.parse_block(operation,tokens,i)
                    parsed_tokens.append(blockToken)
                
                if operation.name in ("CALCULATE"):
                    opToken = self.parse_op(operation)
                    parsed_tokens.append(opToken)

                if operation.name in ("PRINT"):
                    funcToken = self.parse_func(operation)
                    parsed_tokens.append(funcToken)

                if operation.name in ("DECLARATION"):
                    varToken = self.parse_var(operation)
                    parsed_tokens.append(varToken)


        for op in parsed_tokens:
            if op.tag == "BLOCK":
                self.print_block_token(op)

            if op.tag == "BIN OP":
                self.print_bin_token(op)

            if op.tag == "FUNCTION":
                self.print_func(op)
            
            if op.tag == "DECLARATION":
                self.print_var(op)

            
    def parse_var(self,operation):
        if len(operation.code) > 1:
            return VarToken(operation.code[0].code,operation.code[2].code)
        else:
            return VarToken(operation.code[0].code,None)

                
    def parse_func(self,operation):
        return FuncToken(operation.name,operation.code)


    def parse_op(self, operation):
        binToken = BinOpToken()
        
        for i,op in enumerate(operation.code):
            if op.name in ("MINUS","ADD","MULTIPLY","DIVIDE"):
                binToken.name = op.name
                binToken.left = operation.code[i-1]
                binToken.right = operation.code[i+1]

        return binToken

                    
    def parse_block(self,operation,tokens,i):
        blockToken = BlockToken(operation.name)

        for j,op in enumerate(operation.code):
            if op.name in ("EQUAL","EQUIVALENT","NOT","NOT EQUIVALENT","LESS","LESS EQUIVALENT","GREATER","GREATER EQUIVALENT"):
                blockToken.condition = BinOpToken(op.name, operation.code[j-1], operation.code[j+1])   

        target_op = "END " + operation.name
        block_code = self.locate_op(tokens, target_op,i)
        blockToken.code = block_code

        return blockToken

    
    def locate_op(self,tokens, target_op,i):
        # sourcery skip: hoist-statement-from-loop
        block_code = []
        i += 1
        while i < len(tokens):
            line = tokens[i]
            for operation in line:
                if operation.name == target_op:
                    return block_code
                else:
                    block_code.append(operation)
            i += 1
        
               
    def print_tokens(self,tokens):
        for line in tokens:
            for token in line:
                print(token.name)
                for op in token.code:
                    print("\t",op.name,op.code)
        print("")

    
    def print_block_token(self,blockToken):
        print(blockToken.name,":",blockToken.condition.left.code,blockToken.condition.name,blockToken.condition.right.code)
        for op in blockToken.code:
            print("\t",op.name,)
        print("")

    
    def print_bin_token(self,token):
        print("CALCULATE",token.left.name,token.left.code, token.name, token.right.name,token.right.code)
        print("")


    def print_func(self,token):
        print(token.name)
        for op in token.parameters:
            print("\t",op.name, op.code)
        print("")


    def print_var(self, token):
        print(token.tag,":",token.name,"=",token.value)
        print("")