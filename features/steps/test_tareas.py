from behave import *
import pytest
import sys
import os
import asyncio

from requests.models import Response
sys.path.append(os.path.join(os.path.dirname(__file__), "..","..","src" ,"service"))
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

@given('una tarea "{letra}"')
def step_impl(contex, letra):
    response = client.post('/recursos/proyect_id/tarea_id_' + letra +'/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']

@when('consulto las horas trabajadas de la tarea sin especificar el periodo')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasTarea/tarea_id_A')
    client.delete('/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.horas = contex.content
    

@then('se me mostraran las horas totales cargadas a la tarea')
def step_impl(contex):
    assert contex.horas == '10'
    

@when('consulto las horas trabajadas de la tarea en un periodo determinado')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasTarea/tarea_id_B?fecha_menor=2021-12-02T21:33:33&fecha_mayor=2022-12-03T21:33:33')
    client.delete('/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.horas = response.json()
    

@then('se me mostraran las horas cargadas a la tarea en ese periodo')
def step_impl(contex):
    assert contex.horas == '10'

@given('una tarea sin horas cargadas')
def step_impl(contex):
    pass

@when('consulto las horas trabajadas')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasTarea/tarea_id_C')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    contex.content = response.json()
    
    

@then('se notificara que no hay horas cargadas a la tarea')
def step_impl(contex):
    assert contex.content == 'No se encontro el proyecto con id: tarea_id_C'