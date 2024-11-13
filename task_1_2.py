import json, inspect, time

async def readBody(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    readBody = True
    while readBody:
        message = await receive()
        body += message.get('body', b'')
        print(list(message.keys()))
        readBody = message.get('readBody', False)
    return body

class BodyTools:
    
    @staticmethod
    def parseBody(body):
        try:
            return json.loads(body)
        except:
            return None

class ArgsTools:
    @staticmethod
    def parseArgs(args):
        try:
            return dict(list(map( lambda x: x.split('='), args.decode().split('&'))))
        except:
            return None

class Answer:
    def send(self, sender):
        pass

class Responce(Answer):
    def __init__(self, body:str) -> None:
        self.body = str.encode(body)
        
    async def send(self, sender):
        await sender({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await sender({
            'type': 'http.response.body',
            'body': self.body,
        })
        
class Redirect(Answer):
    def __init__(self, location:str) -> None:
        self.location = str.encode(location)
        
    async def send(self, sender):
        await sender({
            'type': 'http.response.start',
            'status': 307,
            'headers': [
                [b'content-length', b'0'],
                [b'location', self.location],
                    
            ]
        })
        await sender({
            'type': 'http.response.body',
            'body': b'',
        })

class AppInstance:
    __instance = None
    
    def __init__(self) -> None:
        self.__appControllers = []
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = AppInstance()
        return cls.__instance
    
    def route(self, route):
        def decorator(function) -> tuple[bool, Answer]:
            def wrapper(host, realRoute, args, body):
                
                result = None
                routeEqual = False
                
                if route == realRoute:
                    #passing required params to function
                    funcArgsList = []
                    funcRequiredParams = inspect.getfullargspec(function)[0]
                    for requiredArg in funcRequiredParams:
                        if requiredArg == 'args':
                            funcArgsList.append(ArgsTools.parseArgs(args))
                        elif requiredArg == 'body':
                            funcArgsList.append(BodyTools.parseBody(body))
                        elif requiredArg == 'host':
                            funcArgsList.append(host)
                        elif requiredArg == 'route':
                            funcArgsList.append(realRoute)
                        else:
                            raise Exception(f'Wrong param "{requiredArg}"')
                        
                    result = function(*funcArgsList) 
                    routeEqual = True
                    
                return routeEqual, result
            wrapper.__name__ == function.__name__
            self.__appControllers.append(wrapper)
            return wrapper
        return decorator


    def getControllers(self):
        return self.__appControllers
   
   
appContext = AppInstance.getInstance()  

HASH_HOLDER = {}
CLIENT_CONNECTION_HOLDER = {}
REQUEST_MIN_INTERVAL = 1




@appContext.route('/compress')
def compress(host, route, body):
    global HASH_HOLDER
    if body:
        if 'route' in body:
            routeToCompress = body['route']
            # prepare the url to suit for RedirectResponse
            if not routeToCompress.startswith('http://') and not routeToCompress.startswith('https://'):
                routeToCompress = 'http://' + routeToCompress
            
            # hashing the url and put it to the hash table
            hashedUrl = str(hash(routeToCompress))
            HASH_HOLDER[hashedUrl] = routeToCompress
            
            bodyStr = json.dumps({route: True, 'route': f'{host}/get?target={hashedUrl}'})
            return Responce(bodyStr)
            
    bodyStr = json.dumps({route: False, 'error': 'Missing body param "route"'})
    return Responce(bodyStr)

@appContext.route('/get')
def get(route, args):
    print(args)
    if args:
        if 'target' in args:
            target = args['target']
            if target in HASH_HOLDER:
                return Redirect(HASH_HOLDER[target])
            bodyStr = json.dumps({route: False, 'error': 'Unknown redirect target'})
            return Responce(bodyStr)
    bodyStr = json.dumps({route: False, 'error': 'Missing argument param "target"'})
    return Responce(bodyStr)
    


async def app(scope, receive, send):
    
    host= f'{scope["server"][0]}:{scope["server"][1]}'
    route = scope['path']
    args = scope['query_string']
    body = await readBody(receive)
    
    # Brute-force atack check
    client = scope['client']
    if client in CLIENT_CONNECTION_HOLDER:
        if time.time() - CLIENT_CONNECTION_HOLDER[client] < REQUEST_MIN_INTERVAL:
            await Responce(json.dumps({route: False, "error": "Too many requests"})).send(send)
            return
    CLIENT_CONNECTION_HOLDER[client] = time.time()
            
    
    
    assert scope['type'] == 'http'
    
    for controller in AppInstance.getInstance().getControllers():
        match, res = controller(host, route, args, body)
        if match:
            await res.send(send)
            return
        
    await Responce(json.dumps({route: False, "error": "No Route Match"})).send(send)
    

    
