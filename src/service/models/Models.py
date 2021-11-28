import datetime
from typing import Optional
from pydantic import EmailStr
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
import sys
import os

from sqlalchemy.sql.expression import false
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from baseService.DataBase import Base


class Proyecto(Base):
    __tablename__ = "Proyectos"
    proyecto_id = Column(String, primary_key=True, nullable=False)
    nombre_proyecto = Column(String, nullable=False)
    
class Tarea(Base):
    __tablename__ = "Tareas"
    tarea_id = Column(String, primary_key=True, nullable=False)
    proyecto_id = Column(String, ForeignKey('Proyecto.proyecto_id'))

class Empleado(Base):
    __tablename__ = "Empleados"
    legajo = Column(String, primary_key=True, nullable=False)
    nombre_completo_empleado = Column(String, nullable=False)

class Carga_horas(Base):
    __tablename__ = "cargas"
    carga_id = Column(String, primary_key=True)
    horas = Column(Integer, nullable= false)
    fecha = Column(DateTime )
    proyecto_id = Column(String, nullable=False)
    tarea_id = Column(String,nullable=False)
    empleado_id = Column(String,nullable=False)
    