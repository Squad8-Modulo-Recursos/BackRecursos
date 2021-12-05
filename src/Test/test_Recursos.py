import pytest
import sys
import os
import asyncio
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "service"))
from fastapi import status
from calls import ApiCalls
from baseService.Database import test_engine, Base
from baseService.ExamsService import app
from datetime import datetime
from fastapi.testclient import TestClient

client= TestClient(app)
Base.metadata.drop_all(test_engine)
Base.metadata.create_all(test_engine)
ApiCalls.set_engine(test_engine)