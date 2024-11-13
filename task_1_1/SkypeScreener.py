from Screener import Screener

class SkypeScreener(Screener):
    
    def __init__(self, screenSymbol: str) -> None:
        super().__init__(screenSymbol)
        
    def screen(self, target: str) -> str:
        if '<' in target:
            replacePart = target.split('skype:')[1].split('?')[0]
            res = target.replace(replacePart, 'xxx')
        else:
            replacePart = target.split('skype:')[1]
            res = target.replace(replacePart, 'xxx')
        return res
    
    
if __name__ == "__main__":
    
    ss = SkypeScreener('x')
    # test 1
    skype1 = 'skype:alex.max'
    res1 = ss.screen(skype1)
    print(res1)
    assert 'skype:xxx' == res1
    
    # test 2
    skype2 = '<a href=\"skype:alex.max?call\">skype</a>'
    res2 = ss.screen(skype2)
    print(res2)
    assert '<a href=\"skype:xxx?call\">skype</a>' == res2