from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "postgresql://ysioenukhxqfvc:a82f291639e67fd9d3bd76a2db9ba975c465b856147721e0c1ff5cbed55f79ca@ec2-44-199-85-33.compute-1.amazonaws.com:5432/dale3qksnai120"
engine = create_engine(DATABASE_URL)

Base = declarative_base()