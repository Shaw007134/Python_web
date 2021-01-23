import pandas as pd
import numpy as np
from sqlalchemy import create_engine

eGRID2016_plants = './eGRID.csv'
eGRID2016_states = './State.csv'

df_plants = pd.read_csv(eGRID2016_plants)
df_states = pd.read_csv(eGRID2016_states)

df_plants = df_plants.dropna(axis=0, subset=['LAT'])
df_plants.replace([np.inf, -np.inf], np.nan, inplace=True)
df_plants = df_plants.fillna(0)

# df_states['STNGENAN'] = pd.to_numeric(df_states['STNGENAN'])

host = '127.0.0.1'
port = 3306
db = 'egrid'
user = 'root'
password = 'root'

# df_plants[df_plants.PLNGENAN < 0] = 0
engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' +
                           "@%s/%s?charset=utf8") % (user, password, host, db))

try:
    df_plants.to_sql('plants', con=engine, if_exists='replace', index=True)
except Exception as e:
    print(e)

try:
    df_states.to_sql('states', con=engine, if_exists='replace', index=True)
except Exception as e:
    print(e)
