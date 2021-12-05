from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "postgresql://ysioenukhxqfvc:a82f291639e67fd9d3bd76a2db9ba975c465b856147721e0c1ff5cbed55f79ca@ec2-44-199-85-33.compute-1.amazonaws.com:5432/dale3qksnai120"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

TEST_DATABASE_URL = "postgresql://obbqpairajzwpb:2dae47d7e0c66169b037c1949a74ca7d872478eae077ba9369d4cd95247cc5be@ec2-54-204-148-110.compute-1.amazonaws.com:5432/ddkcbm3eqrqp43"
test_engine = create_engine(TEST_DATABASE_URL)
