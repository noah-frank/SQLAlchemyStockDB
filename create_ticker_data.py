from sqlalchemy import create_engine

engine = create_engine("sqlite:///databases/ticker_data.db", echo=True)

from sqlalchemy import select

from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.types import DateTime


metadata_extract = MetaData()

extract = Table(
    "RawData", metadata_extract,
    Column("id", Integer, primary_key=True),
    Column("datetime", DateTime, nullable=False),
    Column("open", Float, nullable=False),
    Column("high", Float, nullable=False),
    Column("low", Float, nullable=False),
    Column("close", Float, nullable=False),
    Column("volume", Integer, nullable=False),
    Column("ticker", String, nullable=False)
)

# MetaData() – A container for table definitions.
# Table() – Defines a table and its structure.
# Column() – Specifies each column’s data type and constraints.
# primary_key=True – Marks the id column as the primary key.

metadata_extract.create_all(engine)


metadata_load = MetaData()

load = Table(
    "LoadedData", metadata_load,
    Column("id", Integer, primary_key=True),
    # Column("Index")
    Column("datetime", DateTime, nullable=False),
    Column("open", Float, nullable=False),
    Column("high", Float, nullable=False),
    Column("low", Float, nullable=False),
    Column("close", Float, nullable=False),
    Column("volume", Integer, nullable=False),
    Column("rolling30avg", Float, nullable=True),
    Column("rolling30min", Float, nullable=True),
    Column("rolling30max", Float, nullable=True),
    Column("ticker", String, nullable=False)
)

# load.drop(engine)

from sqlalchemy import delete
stmt = delete(load).where(load.c.rolling30avg == None)

with engine.connect() as connection:
    connection.execute(stmt)
    connection.commit()

print("NULL RECORDS DELETED")

# MetaData() – A container for table definitions.
# Table() – Defines a table and its structure.
# Column() – Specifies each column’s data type and constraints.
# primary_key=True – Marks the id column as the primary key.

metadata_load.create_all(engine)

# from sqlalchemy import insert
# from datetime import datetime

# stmt = insert(load).values(
#     datetime=datetime.now(),
#     open=1, high=1, low=1, close=1, volume=1, ticker="TEST"
# )

# with engine.connect() as connection:
#     connection.execute(stmt)
#     connection.commit()

# print("DATA INSERTED")

# from sqlalchemy import drop
# load.drop(engine)

# load.drop(engine)
# print("TABLE DROPPED")