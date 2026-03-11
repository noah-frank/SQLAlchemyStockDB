from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///databases/ticker_data.db", echo=True)

sql = text("SELECT * FROM LoadedData")
pd.read_sql(sql, con=engine)