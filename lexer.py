import re
from enumTokenType import *

class Lexer:
    def __init__(self, data, tokens):
        self.data = data
        self.tokens = tokens

        self.current = 0
        self.previous = -1
        self.num_re = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.identifier_re = re.compile(r"(([a-zA-Z_]+)([a-zA-Z_0-9]*))")

    def __iter__(self):
        self.current = 0
        return self

    # At most une token can be put back in the stream.
    def put_back(self):
        self.current = self.previous

    def peek(self):
        if self.current < len(self.data):
            current = self.current

            while self.data[current] in " \t\n\r":
                current += 1
            
            previous = current
            char = self.data[current]
            current += 1

            if char == "(":
                return (EnumTokenType.OPEN_PAR, char, current)

            if char == ")":
                return (EnumTokenType.CLOSE_PAR, char, current)

            if char == "=":
                return (EnumTokenType.ASSIGNMENT, char, current)

            # Do not handle minus operator.
            if char in "+/*^":
                return (EnumTokenType.OPERATOR, char, current)

            matchNumber = self.num_re.match(self.data[current - 1 :])
            if matchNumber is not None:
                current += matchNumber.end() - 1
                return (EnumTokenType.NUMBER, matchNumber.group().replace(" ", ""), current)

            matchIdentifier = self.identifier_re.match(self.data[current - 1 :])
            if matchIdentifier is not None:
                current += matchIdentifier.end() - 1
                return (EnumTokenType.IDENTIFIER, matchIdentifier.group().replace(" ", ""), current)

            # If there is no match we may have a minus operator
            if char == "-":
                return (EnumTokenType.OPERATOR, char, current)

            # If we get here, there is an error an unexpected char.
            raise Exception(
                f"Error at {current}: "
                f"{self.data[current - 1:current + 10]}"
            )            

        return (None, None, self.current)

    def __next__(self):
        """Retrieve the next token."""
        token_id, token_value, current = self.peek()

        if token_id is not None:
            self.previous = self.current
            self.current = current

            return (token_id, token_value)

        raise StopIteration()

    def error(self, msg=None):
        """Generate a Lexical Errro."""
        err = (
            f"Error at pos {self.current}: "
            f"{self.data[self.current - 1:self.current + 10]}"
        )

        if msg is not None:
            err = f"{msg}\n{err}"

        raise Exception(err)
