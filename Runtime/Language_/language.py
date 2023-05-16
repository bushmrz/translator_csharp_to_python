from Token.token_type import TokenType
from SyntaxAnalizer.scanner import Scanner
from Ast.ast_printer import AstPrinter
from Ast.rpn_printer import RpnPrinter
from Ast.python_printer import PythonPrinter
from Runtime.interpreter import Interpreter
from SyntaxAnalizer.parser import Parser
from Runtime.resolver import Resolver
from Runtime.Language_.error_handler import ErrorHandler


class Language:
    error_handler = ErrorHandler()
    interpreter = Interpreter(error_handler)
    ast = AstPrinter()
    hadError = False
    hadRuntimeError = False

    @staticmethod
    def set_scanner_error_handler(handler):
        global scanner_error
        scanner_error = handler

    @staticmethod
    def main(args):
        if len(args) > 1:
            print("Usage: lox [script]")
            exit(64)
        elif len(args) == 1:
            Language.run_file(args[0])
        else:
            Language.run_prompt()

    @staticmethod
    def run_file(path):
        with open(path, "r") as file:
            source = file.read()
            try:
                Language.run(source)
            except:
                pass
            if Language.hadError:
                exit(65)
            if Language.hadRuntimeError:
                exit(70)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                Language.run(line)
                Language.hadError = False
            except EOFError:
                break

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        # [print(i.type) for i in tokens]
        parser = Parser(tokens, Language.error_handler)
        statements = parser.parse()

        if Language.hadError:
            return

        resolver = Resolver(Language.interpreter)
        resolver.resolve(statements)

        if Language.hadError:
            return

        try:
            Language.interpreter.interpret(statements)
            # Uncomment to see RPN representation of the code tree
            # print(Language.ast.print_nodes(statements))
            # print(RpnPrinter().print_nodes(statements))
            print(PythonPrinter().print_nodes(statements))
        except RuntimeError as e:
            Language.runtime_error(e)

    @staticmethod
    def using_rpn(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, Language.error_handler)
        statements = parser.parse()
        if Language.hadError:
            return

        resolver = Resolver(Language.interpreter)
        resolver.resolve(statements)

        if Language.hadError:
            return

        try:
            Language.interpreter.interpret(statements)
            Language.ast.print_nodes(statements)
            return RpnPrinter().return_text(statements)
        except RuntimeError as e:
            Language.runtime_error(e)

    @staticmethod
    def get_python_code(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, Language.error_handler)
        statements = parser.parse()

        if Language.hadError:
            return

        resolver = Resolver(Language.interpreter)
        resolver.resolve(statements)

        if Language.hadError:
            return

        try:
            Language.interpreter.interpret(statements)
            return PythonPrinter().return_text(statements)
        except RuntimeError as e:
            Language.runtime_error(e)

    @staticmethod
    def error(line, message):
        Language.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        Language.hadError = True

    @staticmethod
    def error_token(token, message):
        if token.type == TokenType.EOF:
            Language.report(token.line, " at end", message)
        else:
            Language.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error):
        print(f"[line {error.token.line}]: {error.message}")
        Language.hadRuntimeError = True
