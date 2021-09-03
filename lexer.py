import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters


class Token:
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Lexer:
    def __init__(self,program, keywords):
        self.program = program
        self.pos = 0
        self.current_char = None
        self.keywords = keywords


    def advance(self,string):
        self.pos += 1 if self.pos < len(string) else None


    def lex(self, command_list):  # sourcery skip: hoist-statement-from-loop
        tokens = []
        for line in self.program:
            pos = 0
            command_line = []
            command = line.split(":")[0].upper()
            operand = line.split(":")[1].strip()
            operand_tokens = []

            if command not in command_list:
                print("INVALID COMMAND")
                quit()

            operand_tokens = self.parse_operand(operand,line,pos)
            optoken = Token(command_list[command], operand_tokens)
            command_line.append(optoken)      
            tokens.append(command_line)

        return tokens      


    def parse_operand(self,operand,line,pos):
        command = ""
        tokens = []
        
        while pos < len(operand):

            if operand[pos] == "=":
                token, pos = self.handle_symbols(operand,pos,"EQUAL","EQUIVALENT")
                tokens.append(token)
            elif operand[pos] == "!":
                token, pos = self.handle_symbols(operand,pos,"NOT","NOT EQUIVALENT")
                tokens.append(token)
            elif operand[pos] == "<":
                token, pos = self.handle_symbols(operand,pos,"LESS","LESS EQUIVALENT")
                tokens.append(token)
            elif operand[pos] == ">":
                token, pos = self.handle_symbols(operand,pos,"GREATER","GREATER EQUIVALENT")
                tokens.append(token)


            elif operand[pos] == "-":
                tokens.append(Token("MINUS","-"))
            elif operand[pos] == "+":
                tokens.append(Token("ADD","+"))
            elif operand[pos] == "*":
                tokens.append(Token("MULTIPLY","*"))
            elif operand[pos] == "/":
                tokens.append(Token("DIVIDE","/"))

            elif operand[pos] == '"':
                string, pos = self.parse_string(operand,pos)
                tokens.append(Token("STRING",string))
                

            elif operand[pos] in LETTERS:
                string,pos = self.parse_letters(operand,pos)
                if string in self.keywords:
                    tokens.append(Token(self.keywords[string],string))
                else:
                    tokens.append(Token("VARIABLE",string))


            elif operand[pos] in DIGITS:
                number,pos = self.parse_digits(operand,pos)
                tokens.append(Token("NUMBER",number))

            pos += 1 if pos < len(line) else None

        return tokens

    
    def parse_string(self, operand, pos):
        pos += 1
        string = ""
        while operand[pos] != '"':
            string += operand[pos]
            pos += 1
        pos += 1
        return string,pos


    def parse_letters(self,line,pos):
        string = ""
        try:
            while line[pos] in LETTERS:
                string += line[pos]
                pos += 1 if pos < len(line) else None
        except:
            pass
        return string,pos


    def parse_digits(self,line,pos):
        number = ""
        try:
            while line[pos] in DIGITS:
                number += line[pos]
                pos += 1 if pos < len(line)  else None
        except:
            pass

        return int(number),pos


    def handle_symbols(self, operand, pos,single,double):
        if operand[pos+1] == "=":
            string = operand[pos] + "="
            token = Token(double,string)
            pos += 1
        else:
            token = Token(single,operand[pos])
        
        return token,pos