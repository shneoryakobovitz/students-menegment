'''
Program start document.
'''
#from api import Apis
#import os

from dotenv import load_dotenv
load_dotenv()
from screens import app
app.run(debug=True)

#user = Apis('1').api_tamplate('table_info')

'''
import sqlite3
import pandas as pd
import os



def update_files():
    os.chdir('files')
    for name_file in os.listdir():
        if 'csv' in name_file:
            name  = name_file[:-4]
            print(name)
            conn = sqlite3.connect('test.db')
            df = pd.read_csv(name_file, encoding='ISO-8859-8')
            # Replace 'your_table' with the actual table name
            df.to_sql(name, conn, if_exists="replace", index=False)
            conn.commit()
def r_tbl(name_tbl):
    con = sqlite3.connect("test.db")
    df = pd.read_sql_query(f"SELECT * from {name_tbl}", con)
    return df
update_files()
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://ujsuncxljgaehezu:jQt09zRXpoP5cchzHHT@b5zukw8nmucbdvjwnpqd-mysql.services.clever-cloud.com:20471/b5zukw8nmucbdvjwnpqd")
print(r_tbl('data_students'))
'''
