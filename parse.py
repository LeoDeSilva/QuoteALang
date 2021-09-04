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
        parsed_tokens = []
        i = 0
        while i < len(tokens): 
            for operation in tokens[i]:
                if operation.name in ("WHILE","IF"):
                    blockToken,i = self.parse_block(operation,tokens,i)
                    parsed_tokens.append(blockToken)
                
                if operation.name in ("CALCULATE"):
                    opToken = self.parse_op(operation)
                    parsed_tokens.append(opToken)

                if operation.name in ("PRINT","INPUT","INT INPUT"):
                    funcToken = self.parse_func(operation)
                    parsed_tokens.append(funcToken)

                if operation.name in ("DECLARATION"):
                    varToken = self.parse_var(operation)
                    parsed_tokens.append(varToken)
                i += 1

        return parsed_tokens

            
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
        block_code,end_pos = self.locate_op(tokens, target_op,i)
        blockToken.code = self.parse(block_code)

        return blockToken, end_pos

    
    def locate_op(self,tokens, target_op,i):
        # sourcery skip: hoist-statement-from-loop
        block_code = []
        i += 1
        while i < len(tokens):
            line = tokens[i]
            for operation in line:
                if operation.name == target_op:
                    return block_code,i
                else:
                    block_code.append([operation])
            i += 1


        
               
   