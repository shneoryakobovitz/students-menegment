import pandas as pd
import json
from sqlalchemy import create_engine, text
import time
import os
from dotenv import load_dotenv
load_dotenv()
mysql_connection_string = os.getenv('MY_SQL_CONNECTION')


class ReadDataBase:
    '''
    
    title: read and write data in out of the system.

    
    name function     | type data    | type file |
    ==============================================
    get_table_from_db | database     | mysql     |
    ==============================================
    json              | info screens | json      |
    ==============================================
    info_cols         | info columns | json      |
    ==============================================
    info_user         | users        | csv       |
    ==============================================
    '''
    db = {}
    ref_timing = {}
    refresh_tables = {}
    def config(self, path):
        with open('../local_files/info.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
        return info[path]
    
    def info_table(self, table_name):
        return self.config('tables')[table_name]

    def info_tamplate(self, tamplate_name):
        return self.config('tamplates')[tamplate_name]
    
    def read_depends(self, table):
        with open('../local_files/depends.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
        return info[table]
    
    def export_depends(self, tables):
        with open('../local_files/depends.json', 'r') as file:
            data = json.load(file)
        print('data: ', data)
        time_now = int(time.time())
        for t in tables:
            data[t] = time_now
        updated_json = json.dumps(data, indent=4)
        print('new_data: ', data)
        with open('../local_files/depends.json', 'w') as file:
            file.write(updated_json)
    
    @property
    def info_cols(self):
        with open('../local_files/columns.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
        return info
    
    @property
    def info_user(self):
        tbl_users = pd.read_csv('users.csv', encoding='ISO-8859-8').astype('str')
        info = tbl_users[tbl_users['id'] == self.user_id].iloc[0].to_dict()
        return info
    
    def get_table_from_db(self, sql_query):
        ''' get table by sql query '''
        
        engine = create_engine(mysql_connection_string)
        df = pd.read_sql_query(sql_query, con=engine)
        engine.dispose()

        return df
    


    
    def update_to_db(self, query):
        try:
            engine = create_engine(mysql_connection_string)
            print('query: ', query)
            update_statement = text(query)
            with engine.connect() as connection:
                connection.execute(update_statement)
                connection.commit()
            engine.dispose()
            return {'connect': True}
        
        except Exception as e:
            print('Exception')
            return {'connect': False,'info': str(e)}