"""
Code generation using MIPS
"""
import os


WORD_SIZE = 4

class MIPS:

    _output = ""
    offset = 0

    def __init__(self, output_file="/tmp/mips.asm"):
        space = "    "
        self._output = f"{space}.globl main\n{space}.text\n\nmain:\n"
        self.offset = 0
        self.output_file = output_file

    def write(self, command: str):
        self._output += "    " + command + "\n"

    def read(self):
        return self._output

    def clean(self):
        self._output = ""

    def execute(self, verbose=True):
        source = self.read()
        # source += "    syscall\n"

        with open(self.output_file, "w") as f:
            f.write(source)

        command = f"spim -file {self.output_file}"

        if verbose:
            print(source)
            print("=" * 80)

        print(command)
        os.system(command)

    def ast(self, expr: str):
        raise Exception("AST method should be defined.")

    def codegen(self, expr: str):
        raise Exception("codegen method should be defined.")

    # mips commands:

    def add(self,reg_1, reg_2, reg_3):
        """Add register 2 and 3 and store the result into the register 1."""
        self.write(f"add {reg_1}, {reg_2}, {reg_3}")

    def addiu(self, reg_1, reg_2, imm):
        """
        add immediate.

        note: "u" means that overflow is not checked.
        """
        self.write(f"addiu {reg_1}, {reg_2}, {imm}")

    def li(self, reg_1, i):
        """
        load immediate
        """
        self.write(f"li {reg_1}, {i}")

    def lw(self, reg_1, reg_2, offset):
        """load word."""
        self.write(f"lw {reg_1}, {offset}({reg_2})")

    def sw(self, reg_1, reg_2, offset):
        """store word."""
        self.write(f"sw {reg_1}, {offset}({reg_2})")

    def sub(self, reg_1, reg_2, reg_3):
        """subtraction instruction."""
        self.write(f"sub {reg_1}, {reg_3}, {reg_2}")


class MathMIPS(MIPS):
    def isnumber(self, v: str):
        if not isinstance(v, str):
            return False
        return v in "0123456789"


    def tokenize(self, expr: str) -> list:
        tokens = []

        token = ""
        n_expr = len(expr)

        for i, char in enumerate(expr):
            
            next_char = expr[i+1] if n_expr > i + 1 else None
                
            if char == " ":
                if token != "":
                    tokens.append(token)
                token = ""
                continue

            if char == "+":
                tokens.append(("BINOP", "ADD"))
                continue

            if char == "-":
                tokens.append(("BINOP", "SUB"))
                continue

            if self.isnumber(char):
                token += char

                if self.isnumber(next_char):
                    continue

                tokens.append(("INT", token))
                token = ""

        return tokens

    def ast(self, expr: str):
        tokens = self.tokenize(expr)

        ast = []
        stack = []
        n_tokens = len(tokens)
        branch = None
        errors = []

        for i, token in enumerate(tokens):
            token_type, token_value = token
            next_token = tokens[i+1] if n_tokens > i + 1 else None

            if token_type == "BINOP":
                if not stack or not next_token:
                    errors.append(
                        "+ sign is a binary operation, so it needs one number "
                        "before and another one after."
                    )

                branch = [token, stack.pop(-1)]
                continue

            if token_type == "INT":
                if not branch:
                    stack.append(token)
                    continue

                branch.append(token)
                ast.append(branch)
                branch = None

        return ast

    def codegen(self, expr_or_ast):
        if isinstance(expr_or_ast, str):
            ast = self.ast(expr_or_ast)
        else:
            ast = expr_or_ast

        for node in ast:
            if isinstance(node, list):
                op = node[0]
                args = node[1:]

                node_type, node_value = op

                if node_type == "BINOP":
                    self.codegen([args[0]])

                    self.sw("$a0", "$sp", offset=self.offset)
                    self.addiu("$sp", "$sp", imm=self.offset-WORD_SIZE)
                    self.offset += WORD_SIZE

                    self.codegen([args[1]])

                    self.lw("$t1", "$sp", offset=self.offset)
                    
                    if node_value == "ADD":
                        self.add("$a0", "$a0", "$t1")

                    if node_value == "SUB":
                        self.sub("$a0", "$a0", "$t1")

                    self.addiu("$sp", "$sp", imm=self.offset)
                    self.offset -= WORD_SIZE
                continue

            node_type, node_value = node

            if node_type == "INT":
                self.li("$a0", node_value)
                continue

