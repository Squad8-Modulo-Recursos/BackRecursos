from fastapi import status
import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from typing import List, Optional
from starlette.responses import JSONResponse

















router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


#
#{
 #   user_id:
 #   nombre:
 #   proyectos:
 #   tareas:
 #   descripcion:
#}

#{
   # usuarios:{}
   # proyectos:{ }
   # tareas: {}
#}







@router.post('/{user_id}', response_model=str, status_code=status.HTTP_200_OK)
async def cargarHorasUsuarios(user_id: str , cantidad_horas: int , fallo: int):
    if fallo > 1 :
        return JSONResponse(status_code = status.HTTP_202_ACCEPTED, content = ('\'s password has been correctly changed.'))
    return{
        'horas agregadas' : cantidad_horas,
        'user_id' : user_id
    }
