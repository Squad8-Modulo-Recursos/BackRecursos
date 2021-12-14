import requests
from datetime import datetime
from fastapi import status
from fastapi import APIRouter
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse
import uuid
from models.Models import Carga_horas


router = APIRouter()
router_empleados = APIRouter()
session = None
Session = None


def set_engine(engine_rcvd):
    global engine
    global Session
    global session
    engine = engine_rcvd
    Session = sessionmaker(bind=engine)
    session = Session()


@router.post('/{proyecto_id}/{tarea_id}/cargarHoras/{legajo}', response_model=str, status_code=status.HTTP_200_OK)
async def cargar_Horas_Usuarios(proyecto_id: str, tarea_id: str, legajo: str, cantidad_horas: int, fecha: Optional[datetime] = None):  
    if( cantidad_horas <= 0):
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = 'La carga de horas no puede ser negativa')  
    try:
        carga_id = str(uuid.uuid4())
        session.add(Carga_horas(carga_id = carga_id,
                              horas = cantidad_horas,
                              proyecto_id = proyecto_id,
                              tarea_id = tarea_id,
                              empleado_id = legajo,
                              fecha =  fecha))
        session.commit()
    except Exception as e:
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = 'Error al cargar las horas ' + str(e))  
    return JSONResponse(status_code = status.HTTP_200_OK,
                                content= {"carga_id": carga_id,
                                "horas": cantidad_horas,
                                "proyecto_id": proyecto_id,
                                "tarea_id": tarea_id,
                                'empleado_id': legajo})

@router.get('/ObtenerHorasProyecto/{empleado_id}', response_model=str, status_code=status.HTTP_200_OK)
async def solicitar_Horas_Por_Proyecto(empleado_id, proyecto_id, fecha_menor: Optional[datetime] = None, fecha_mayor: Optional[datetime] = None):
    query = session.query(Carga_horas).filter(Carga_horas.empleado_id == empleado_id)
    query = query.filter(Carga_horas.proyecto_id == proyecto_id)
    if(fecha_menor is not None):
        query = query.filter(Carga_horas.fecha >= fecha_menor) 
    if(fecha_mayor is not None):
        query = query.filter(Carga_horas.fecha <= fecha_mayor) 
    if query.count() == 0:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content= 'No se encontro el proyecto con id: ' + str(proyecto_id))

    horas_totales = 0
    for carga in query:
        horas_totales += carga.horas
    return horas_totales

@router.get('/ObtenerHorasTarea/{empleado_id}', response_model=str, status_code=status.HTTP_200_OK)
async def solicitar_Horas_Por_Tarea(empleado_id, tarea_id, fecha_menor: Optional[datetime] = None, fecha_mayor: Optional[datetime] = None):
    query = session.query(Carga_horas).filter(Carga_horas.empleado_id == empleado_id)
    query = query.filter(Carga_horas.tarea_id == tarea_id)
    if(fecha_menor is not None):
        query = query.filter(Carga_horas.fecha >= fecha_menor) 
    if(fecha_mayor is not None):
        query = query.filter(Carga_horas.fecha <= fecha_mayor) 
    if query.count() == 0:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content= 'No se encontro la tarea con id: ' + str(tarea_id))

    horas_totales = 0
    for carga in query:
        horas_totales += carga.horas
    return horas_totales


@router.get('/ObtenerHorasEmpleado/{empleado_id}', response_model=str, status_code=status.HTTP_200_OK)
async def solicitar_Horas_Por_Empleado(empleado_id, fecha_menor: Optional[datetime] = None, fecha_mayor: Optional[datetime] = None):
    query = session.query(Carga_horas).filter(Carga_horas.empleado_id == empleado_id)
    if(fecha_menor is not None):
        query = query.filter(Carga_horas.fecha >= fecha_menor) 
    if(fecha_mayor is not None):
        query = query.filter(Carga_horas.fecha <= fecha_mayor) 
    if query.count() == 0:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content= 'No se encontro el empleado con id: ' + str(empleado_id))

    horas_totales = 0
    for carga in query:
        horas_totales += carga.horas
    return horas_totales


@router.get('/ObtenerTotalHoras', response_model=str, status_code=status.HTTP_200_OK)
async def solicitar_Horas():
    query = session.query(Carga_horas)
    lista_horas = []
    for hora in query:
        lista_horas.append({
            "carga_id": hora.carga_id,
            "horas": hora.horas,
            "fecha": hora.fecha,
            "proyecto_id": hora.proyecto_id,
            "tarea_id": hora.tarea_id,
            "empleado_id" :hora.empleado_id,
        })
    return JSONResponse(status_code = status.HTTP_200_OK, content = lista_horas)

@router.delete('/EliminarHoras/{Carga_id}', response_model=str, status_code=status.HTTP_200_OK)
async def eliminar_Horas(Carga_id):
    query = session.query(Carga_horas).filter(Carga_horas.carga_id == Carga_id).delete()
    return JSONResponse(status_code = status.HTTP_200_OK, content= "Se ha eliminado la carga " + str(Carga_id))


@router.patch('/ModificarHoras/{Carga_id}', response_model=str, status_code=status.HTTP_200_OK)
async def modificar_Horas(Carga_id, cantidad_horas: int):
    query = session.query(Carga_horas).filter(Carga_horas.carga_id == Carga_id)
    query.horas = cantidad_horas
    return JSONResponse(status_code = status.HTTP_200_OK, content= "Se ha modificado la carga " + str(Carga_id)+ " correctamente.")

@router_empleados.get('/ObtenerEmpleados')
async def solicitar_empleados():
    lista_empleados = requests.get("https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos")
    return JSONResponse(status_code = lista_empleados.status_code, content = lista_empleados.json())

