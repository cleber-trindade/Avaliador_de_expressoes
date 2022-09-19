import math
from enumTokenType import *

class Tokens:
    def __init__(self):
        self.tokens = {
            'sin': {
                'type': EnumTokenType.FUNCTION,
                'value': lambda x: math.sin(x)
            },
            'cos': {
                'type': EnumTokenType.FUNCTION,
                'value': lambda x: math.cos(x)
            },
            'log': {
                'type': EnumTokenType.FUNCTION,
                'value': lambda x: math.log(x)
            },
            'sqrt': {
                'type': EnumTokenType.FUNCTION,
                'value': lambda x: math.sqrt(x)
            }
        }

    def addToken(self, tokenId, tokenType, value):
        self.tokens[tokenId] = {
            'name': tokenId,
            'type': tokenType,
            'value': value
        }

    def getToken(self, tokenId):
        try:
            return self.tokens[tokenId]
        except KeyError:
            return None