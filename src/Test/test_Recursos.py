import pytest
import sys
import os
import asyncio

from requests.models import Response
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "service"))
from fastapi import status
from calls import ApiCalls
from baseService.DataBase import test_engine, Base
from baseService.ResoursesService import app
from datetime import datetime
from fastapi.testclient import TestClient

client= TestClient(app)
Base.metadata.drop_all(test_engine)
Base.metadata.create_all(test_engine)
ApiCalls.set_engine(test_engine)



def test_crear_carga():
    response = client.post('/recursos/proyect_id/tarea_id/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    carga_id = content['carga_id']
    assert content['empleado_id'] == 'legajo'
    assert content['horas'] == 10
    assert content['proyecto_id'] == 'proyect_id'
    assert content['tarea_id'] == "tarea_id"
    client.delete('/EliminarHoras/'+carga_id)


def test_solicitar_horas_proyecto():
    response = client.post('/proyecto_id')
    assert response.status_code == status.HTTP_200_OK
    content = response.json() 


