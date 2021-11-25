
from datetime import datetime
from fastapi import status
from sqlalchemy.sql.sqltypes import DateTime
import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse
import uuid
from models.Models import Carga_horas
from sqlalchemy.orm.exc import NoResultFound


router = APIRouter()
session = None
Session = None


def set_engine(engine_rcvd):
    global engine
    global Session
    global session
    engine = engine_rcvd
    Session = sessionmaker(bind=engine)
    session = Session()


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


@router.post('{proyecto_id}/{tarea_id}/cargarHoras/{legajo}', response_model=str, status_code=status.HTTP_200_OK)
async def cargarHorasUsuarios(proyecto_id: str , tarea_id: str ,legajo: str ,  cantidad_horas: int,fecha: Optional[datetime] = None):
    carga_id = str(uuid.uuid4())
    nuevaCarga = Carga_horas(carga_id = carga_id,
                              horas = cantidad_horas,
                              proyecto_id = proyecto_id,
                              tarea_id = tarea_id,
                              empleado_id = legajo,
                              fecha =  fecha)
    try:
        session.add(nuevaCarga)
        session.commit()
    except Exception as e:
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = 'Error al cargar las horas ' + str(e))
    
    return JSONResponse(status_code = status.HTTP_200_OK,
                                content= {"carga_id": carga_id,
                                "horas": cantidad_horas,
                                "proyecto_id": proyecto_id,
                                "tarea_id": tarea_id,
                                'empleado_id': legajo})

@router.get('/ObtenerHoras/{proyecto_id}', response_model=str, status_code=status.HTTP_200_OK)
async def solicitarHorasPorProyecto(proyecto_id , fecha_menor: Optional[datetime] = None , fecha_mayor: Optional[datetime] = None):
    try:
        Carga_del_proyecto = session.query(Carga_horas).filter(Carga_horas.proyecto_id == proyecto_id)
    except NoResultFound as err:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content= 'No se encotro el proyecto con id: ' + str(proyecto_id))
    horas_totales = 0
    for carga in Carga_horas:
        horas_totales += carga.horas
    return horas_totales

##@router.get()
##async def solicitarHorasPorTarea(tarea_id , fecha):
##@router.get()
##async def solicitarHorasPorEmpleado(Empleado_id , fecha):

