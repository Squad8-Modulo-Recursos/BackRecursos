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


@given('un proyecto')
def step_impl(contex):
    response = client.post('/recursos/project_id/tarea_id/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    client.delete('/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']
 
@when('consulto las horas trabajadas del proyecto sin especificar el periodo')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasProyecto/project_id')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.horas = contex.content

@then('se me mostraran las horas cargadas a todo el proyecto')
def step_impl(contex):
    assert contex.content == '10'



@given('un proyecto')
def step_impl(contex):
    response = client.post('/recursos/project_id/tarea_id/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    response = client.post('/recursos/project_id/tarea_id/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:37')
    client.delete('/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']
 
@when('consulto las horas trabajadas del proyecto en un periodo determinado')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasProyecto/project_id?fecha_menor=2021-12-02T21:33:32&fecha_mayor=2022-11-02T21:33:34')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.horas = contex.content

@then('se me mostraran las horas cargadas al proyecto en ese periodo')
def step_impl(contex):
    assert contex.content == '10'



@given('un proyecto sin horas cargadas')
def step_impl(contex):
    pass

@when('consulto las horas trabajadas sin especificar el periodo')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasProyecto/project_id')
    contex.content = response.json()
    contex.status = response.status_code

@then('se notificará que no hay horas cargadas')
def step_impl(contex):
    assert contex.status == status.HTTP_404_NOT_FOUND
