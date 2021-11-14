from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "postgresql://zlkhaimrgorqjg:bbc08f13a8e820b66b3cc0880a36a676ec82c2b56d947918b823effda0098a5d@ec2-35-169-43-5.compute-1.amazonaws.com:5432/de54sdj8s0j75h"
engine = create_engine(DATABASE_URL)

Base = declarative_base()