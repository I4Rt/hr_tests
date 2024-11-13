# main.py

'''
1.2 Короткие ссылки

Создать сервис для укорачивания ссылок и редиректа на оригинальную 
ссылку с короткой. Предусмотреть хранилище для укороченных ссылок, 
защиту от перебора, редирект с укороченной ссылки на оригинальную. 
Стек по желанию: либо python/uvicorn, либо ruby/ror. Без 
использования сторонних библиотек или сервисов.

'''

import uvicorn
from fastapi import Request, FastAPI
from fastapi.responses import RedirectResponse 

HASH_HILDER = {}

app = FastAPI()

@app.get("/get/{path_hash}")
async def get(path_hash:int):
   if path_hash in HASH_HILDER:
      return RedirectResponse(HASH_HILDER[path_hash])
   return {"/get": False, 'comment': 'Unknown route'}

@app.get("/compress")
async def compress(request: Request):
   global HASH_HILDER
   full_route = request.query_params.get('full_route')

   if full_route:
      # prepare the url to suit for RedirectResponse
      if not full_route.startswith('http://') and not full_route.startswith('https://'):
         full_route = 'http://' + full_route
      
      # hashing the url and put it to the hash table
      hashed_url = hash(full_route)
      HASH_HILDER[hashed_url] = full_route
      
      return {"/compress": True, 'compressed_route': f'{request.base_url}get/{hashed_url}'}
   return {"/compress": False, 'comment': 'Missing "full_route" value'}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)