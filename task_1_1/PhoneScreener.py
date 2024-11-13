from Screener import Screener

class PhoneScreener(Screener):
    
    def __init__(self, screenSymbol: str) -> None:
        super().__init__(screenSymbol)
        
    def screen(self, target: str, count:int=3) -> str:
        res = ''
        
        changedSymbles = 0 
            
        for symble in target[::-1]:
            if changedSymbles < count:
                if symble.isdigit():
                    res = self.screenSymbol + res
                    changedSymbles += 1
                    continue
            if len(res) :
                if res[0] == ' ' and symble == ' ':
                    continue
            res = symble + res

        return res
    
    
if __name__ == "__main__":
    phone = '+7 666 777       888'
    ps = PhoneScreener('x')
    print(ps.screen(phone, 5))
    assert '+7 666 7xx xxx' == ps.screen(phone, 5)