from starlette.status import HTTP_200_OK
from behave import *
import pytest
import sys
import os
import asyncio

from requests.models import Response
sys.path.append(os.path.join(os.path.dirname(__file__), "..","..","src" ,"service"))
from fastapi import params, status
from calls import ApiCalls
from baseService.DataBase import test_engine, Base
from baseService.ResoursesService import app
from fastapi.testclient import TestClient

client= TestClient(app)
Base.metadata.drop_all(test_engine)
Base.metadata.create_all(test_engine)
ApiCalls.set_engine(test_engine)


@given('un proyecto')
def step_impl(contex):
    contex.legajo = 'legajo'
    contex.id_proyecto = 'proyecto_test'
    response = client.post(f'/recursos/{contex.id_proyecto}/tarea_id/cargarHoras/{contex.legajo}?cantidad_horas=10&fecha=2021-12-02')
    assert response.status_code == status.HTTP_200_OK
    contex.carga_id = response.json()['carga_id']
 
@when('consulto las horas trabajadas sin especificar el periodo')
def step_impl(contex):
    response = client.get(f'/recursos/ObtenerHorasProyecto/{contex.legajo}/{contex.id_proyecto}')
    contex.horas = response.json()
    contex.status = response.status_code

@then('se me mostraran las horas cargadas a todo el proyecto')
def step_impl(contex):
    delete = client.delete(f'/recursos/EliminarHoras/{contex.carga_id}')
    assert contex.status == status.HTTP_200_OK
    assert contex.horas == '10'


 
@when('consulto las horas trabajadas del proyecto en un periodo determinado')
def step_impl(contex):
    response = client.get(f'/recursos/ObtenerHorasProyecto/{contex.legajo}/{contex.id_proyecto}', params={'fecha_menor':'2021-12-02', 'fecha_mayor':'2021-12-03'})
    contex.horas = response.json()
    contex.status = response.status_code

@then('se me mostraran las horas cargadas al proyecto en ese periodo')
def step_impl(contex):
    client.delete(f'/recursos/EliminarHoras/{contex.carga_id}')
    assert contex.status == status.HTTP_200_OK 
    assert contex.horas == '10'



@given('un proyecto sin horas cargadas')
def step_impl(contex):
    contex.legajo = 'legajo'
    contex.id_proyecto = 'proyecto_vacio'
    contex.horas = '0'
    pass


@then('se notificará que no hay horas cargadas')
def step_impl(contex):
    assert contex.status == status.HTTP_404_NOT_FOUND