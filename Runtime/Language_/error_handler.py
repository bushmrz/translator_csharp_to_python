from Token.token_type import TokenType


class ErrorHandler:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False

    def runtime_error(self, error):
        print(f"[line {error.token.line}]: {error.message}")
        with open('error_logs.txt', 'a') as file:
            err_log = f"[line {error.token.line}] :  {error.message} \n"
            file.write(err_log)
        self.hadRuntimeError = True

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        with open('error_logs.txt', 'a') as file:
            err_log = f"[line {line}] Error{where}: {message} \n"
            file.write(err_log)
        self.hadError = True

    def error_token(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)
