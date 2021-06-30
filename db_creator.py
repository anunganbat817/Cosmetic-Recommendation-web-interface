from numpy import genfromtxt
from time import time
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import csv
#engine = create_engine('sqlite:///cosmetic.db', echo=True)

   

Base = declarative_base()

class SkinCare(Base):
    __tablename__ = "SkinCare"
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    price = Column(Float)
    no_reviews = Column(Integer)
    size1 = Column(Float)
    url = Column(String)
    ingredients = Column(String)
    list_of_ingredients = Column(String)
    price_per_ml = Column(Float)

    def __repr__(self):
        return "{}".format(self.name)


#Create the database
engine = create_engine('sqlite:///cosmetic.db')
Base.metadata.create_all(engine)
file_name = "sephora_data.csv"
df = pd.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name=SkinCare.__tablename__, if_exists='replace', index = False)
df['name'] = df['name'].str.lower()
#from sqlalchemy import inspect
#inspector = inspect(engine)

#for SkinCare in inspector.get_table_names():
#   for column in inspector.get_columns(SkinCare):
#       print("Column: %s" % column['name'])