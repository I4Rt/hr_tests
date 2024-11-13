from Screener import Screener

class MailScreener(Screener):
    
    def __init__(self, screenSymbol: str) -> None:
        super().__init__(screenSymbol)
        
    def screen(self, target: str) -> str:
        res = ''
        name, domain = target.split('@')
        mask = self.screenSymbol*len(name)
        return mask + '@' + domain
    
    
if __name__ == "__main__":
    mail = 'test_mail@gmail.com'
    ms = MailScreener('x')
    print(ms.screen(mail))
    assert 'xxxxxxxxx@gmail.com' == ms.screen(mail)
            