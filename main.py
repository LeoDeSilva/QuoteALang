import sys

from lexer import Lexer
from parse import Parser
from interpreter import Interpreter

command_list = {
    "ITS ALIVE ITS ALIVE":"DECLARATION",
    "I WISH I KNEW HOW TO QUIT YOU":"WHILE",
    "ILL BE BACK":"END WHILE",
    "SAY HELLO TO MY LITTLE FRIEND":"PRINT",
    "MAKE IT HAPPEN":"CALCULATE",
    "YOUVE GOT TO ASK YOURSELF ONE QUESTION":"IF",
    "IM GOING TO MAKE HIM AN OFFER HE CANT REFUSE":"ELSE",
    "FRANKLY MY DEAR I DONT GIVE A DAMN":"END IF",
    "YOU CANT HANDLE THE TRUTH":"FALSE",
    "YOU HAD ME AT HELLO":"TRUE",
    "YOU TALKIN TO ME":"INPUT",
    "SHOW ME THE MONEY":"INT INPUT"
}

keywords = {
    "and":"AND",
    "or":"OR",
}

program = []

with open(sys.argv[1],"r") as f:
    for line in f:
        if (line.strip() == ""): continue
        formatted_line = line.strip()
        program.append(formatted_line)

lexer = Lexer(program,keywords)
tokens = lexer.lex(command_list)

parser = Parser()
parsed_tokens = parser.parse(tokens)

interpreter = Interpreter(parsed_tokens)
interpreter.interpret(parsed_tokens)
