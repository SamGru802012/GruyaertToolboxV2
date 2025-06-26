
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default='user')

class Box(Base):
    __tablename__ = 'boxes'
    id = Column(Integer, primary_key=True)
    ref = Column(String, unique=True)
    inner_length = Column(Float)
    inner_width = Column(Float)
    inner_height = Column(Float)
    wall_thickness = Column(Float, default=3.0)

class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True)
    product_ref = Column(String)
    box_id = Column(Integer, ForeignKey('boxes.id'))
    rotation = Column(String)
    rows = Column(Integer)
    columns = Column(Integer)
    layers = Column(Integer)
    total = Column(Integer)
    efficiency = Column(Float)
    box = relationship("Box")

def init_db(db_path="sqlite:///packing_app.db"):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return engine
