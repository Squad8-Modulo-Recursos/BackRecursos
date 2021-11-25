from typing import Optional

from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from baseService.DataBase import Base, engine
from calls import ApiCalls

app = FastAPI()


ApiCalls.set_engine(engine)

app.include_router(ApiCalls.router, prefix="/asdasd", tags=["Users"])

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    uvicorn.run(app, host='0.0.0.0', port=8000)