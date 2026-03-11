from sqlalchemy import create_engine, delete, MetaData, Table

engine = create_engine("sqlite:///databases/ticker_data.db", echo=True)

metadata = MetaData()
load = Table("LoadedData", metadata, autoload_with=engine)
stmt = delete(load) #.where(load.c.rolling30avg==None)

with engine.connect() as connection:
    connection.execute(stmt)
    connection.commit()

print("ALL RECORDS DELETED")