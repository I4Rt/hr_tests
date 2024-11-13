class Screener:
    def __init__(self, screenSymbol:str) -> None:
            if not (type(screenSymbol) is str):
                raise Screener.SymbleIsNotLiteralException()
            else:
                if not screenSymbol.isalpha():
                    raise Screener.SymbleIsNotLiteralException()
            
            if len(screenSymbol) != 1:
                raise Screener.SymbleLengthException()
            
            self.screenSymbol = screenSymbol
        
    class SymbleLengthException(Exception):
        def __init__(self):            
            super().__init__('Symble string lenght should be 1')
            
    class SymbleIsNotLiteralException(Exception):
        def __init__(self):            
            super().__init__('Symble should be only literal')
            
    def screen(self, target:str) -> str:
        return ''
            
            
if __name__ == "__main__":
    s = Screener('a')
    print(s.screenSymbol)
    