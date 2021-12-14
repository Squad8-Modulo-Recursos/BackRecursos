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

# Carga de horas
@given('un empleado')
def step_impl(contex):
    pass

@when('carga sus horas trabajadas en una tarea en una fecha determinada')
def step_impl(contex):
    response = client.post('/recursos/proyect_id/tarea_id/cargarHoras/legajo?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']

@then('se cargan las horas empleadas en la fecha corresponidiente y se actualizan sus horas trabajas')
def step_impl(contex):
    client.delete('/recursos/EliminarHoras/'+contex.carga_id)
    assert contex.content['empleado_id'] == 'legajo'
    assert contex.content['horas'] == 10
    assert contex.content['proyecto_id'] == 'proyect_id'
    assert contex.content['tarea_id'] == "tarea_id"
    

@when('carga un numero negativo de horas trabajas a una tarea en una fecha determinado')
def step_impl(contex):
    response = client.post('/recursos/proyect_id/tarea_id/cargarHoras/legajo?cantidad_horas=-10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    contex.content = response.json()
    

@then('no se cargaran las horas')
def step_impl(contex):
    assert contex.content == 'La carga de horas no puede ser negativa'


#Borrado de horas
@given('un empleado "{letra}"')
def step_impl(contex, letra):
    response = client.post('/recursos/proyect_id/tarea_id/cargarHoras/legajo_'+ letra +'?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']

@when('quiere eliminar una carga de horas a una tarea')
def step_impl(contex):  
    response = client.delete('/recursos/EliminarHoras/'+contex.carga_id)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    

@then('se borrara la carga de hora en el sistema')
def step_impl(contex):
    assert contex.content == 'Se ha eliminado la carga ' + str(contex.carga_id)
    

# Control de horas



@when('consulto sus horas trabajadas en un periodo determinado')
def step_impl(contex):  
    response = client.get('/recursos/ObtenerHorasEmpleado/legajo_A?fecha_menor=2021-12-02T21:33:33&fecha_mayor=2022-12-03T21:33:33')
    client.delete('/recursos/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.horas = contex.content
    

@then('se me mostraran las horas trabajadas en ese periodo')
def step_impl(contex):
    assert contex.horas == '10'
    

@when('consulto sus horas trabajadas sin especificar el periodo')
def step_impl(contex):
    response = client.get('/recursos/ObtenerHorasEmpleado/legajo_B')
    client.delete('/recursos/EliminarHoras/'+contex.carga_id)
    assert response.status_code == status.HTTP_200_OK
    contex.horas = response.json()
    

@then('se me mostraran las horas totales cargadas al empleado')
def step_impl(contex):
    assert contex.horas == '10'

@given('que ingrese una cantidad incorrecta de horas a una tarea')
def step_impl(contex):
    response = client.post('/recursos/proyect_id/tarea_id/cargarHoras/legajo_D?cantidad_horas=10&fecha=2022-12-02T21:33:33')
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()
    contex.carga_id = contex.content['carga_id']

@when('quiero modificarla ingrensando una nueva cantidad correcta')
def step_impl(contex):
    response = client.patch('/recursos/ModificarHoras/'+contex.carga_id+'?cantidad_horas=12')
    client.delete('/recursos/EliminarHoras/'+contex.carga_id)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    contex.content = response.json()

@then('se actualizara las horas en el sistema')
def step_impl(contex):
    assert contex.content == "Se ha modificado la carga " + str(contex.carga_id)+ " correctamente."

