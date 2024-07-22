import pandas as pd
from convert.functions import SentencesConvert
import time

class FunctionsTable:

    '''
    function: modify table by params.
    get: params, name_table
    action: change table by params.
    return: table edit.
    '''

    def if_empty(self, table, table_name):
        print(table)
        if self.db[table_name].empty:
            table = self.read_table(table)
            print('table: ', table)
            self.db[table_name] = table

        return self.db[table_name]
    
    def filter_column(self, column, delete, table_name):
        pass
    
    def add_column(self, name_column, value, table_name):
        new_val = self.str_var(value)
        if new_val != 'empty':
            self.db[table_name][name_column] = self.str_var(value)
        else:
             self.db[table_name] = pd.DataFrame({})
    
    def rename_column(self, columns, table_name):
        self.db[table_name].rename(columns=columns, inplace=True)

    def func_merge_column(self, new_name, columns, table_name):
        self.db[table_name][new_name] = self.db[table_name][columns].fillna('-').apply(lambda x: ' '.join(x), axis=1)
    
    def pivot_table(self, index, columns, values, table_name):
        print('\n\npivot\n\n')
        self.db[table_name] = pd.pivot_table(self.db[table_name], 
                                             values=values, 
                                             index=index, 
                                             columns=columns
                                             )
        #new
        self.db[table_name].rename(columns={name_col: f'{values}Q{columns[0]}Q{name_col}' for name_col in self.db[table_name].columns if not 'Q' in name_col}, inplace=True)
        self.db[table_name].to_csv('table.csv', encoding='ISO-8859-8')
        self.db[table_name] = self.db[table_name].reset_index().astype(str)
        
    def func_filter_column(self, delete, columns, table_name):
            new_tbl = self.db[table_name]
            new_tbl.drop(columns, axis=1) if delete else new_tbl[columns]
            self.db[table_name] = new_tbl

    def replace_column(self, table_name, column, values={}, del_left=False):
        self.db[table_name][column].astype(str).replace(values, inplace=True)

    def merge_table(self, info):
        table_name = info['table_name']
        new_merge = {k: self.read_table(v.replace('tbl', '')) if 'tbl' in v else v if v != 'self' else self.db[table_name]  for k, v in info.items() if k != 'table_name' }
        
        print('left: ', new_merge['left'])
        print('right: ', new_merge['right'])
        self.db[table_name] = pd.merge(**new_merge, how='left').fillna('0')
        self.db[table_name].to_csv('123.csv', encoding='ISO-8859-8')

    def group_by(self, table_name, columns, summery_column, type_summery):
        #new_data = {}
        #if columns == 'all':
        #    for col in self.db[table_name].columns:
        #        if type_summery == 'mean':
        #            new_data[col] = self.db[table_name].groupby(col)[summery_column].mean().to_dict()
        #self.db[table_name] = new_data
        self.db[table_name] = pd.read_csv('demo.csv', encoding='ISO-8859-8').astype('str')

    def functions(self, info):
        func = info['function']
        info.pop('function', None)
        match func:
            case 'if_empty':
                return self.if_empty(**info)
            case 'merge_column':
                return self.func_merge_column(**info)
            case 'filter_column': 
                return self.func_filter_column(**info)
            case 'add_column':
                return self.add_column(**info)
            case 'pivot_table':
                return self.pivot_table(**info)
            case 'replace':
                return self.replace_column(**info)
            case 'merge':
                return self.merge_table(info)
            case 'group_by':
                return self.group_by(**info)
            case 'rename_column':
                return self.rename_column(**info)

class Table(FunctionsTable, SentencesConvert):
    '''
    create table by info from configuretion file.
    '''
    
    def create_table(self, info_tbl):
        match info_tbl['source']:
            case 'query':
                sql_query = self.translate('query', info_tbl['query'])
                print('sql_query: ', sql_query)
                if not 'empty' in sql_query:
                    tbl = self.get_table_from_db(sql_query)
                    print(f'table: {tbl}')
                else:
                    tbl = pd.DataFrame({})

                return tbl
            
            case 'copy':
                return self.read_table(info_tbl['table'])
            
    def manipulation(self, table_name, edit_commands):
        for command_info in edit_commands:
            if not self.db[table_name].empty or command_info['function'] == 'if_empty':
                command_info['table_name'] = table_name
                self.functions(command_info)
    
    def time_refresh(self, info_refresh, table_name):
        tp = info_refresh.get('type')
        if tp == 'timing':
            need_refresh = self.refresh_tables.get(table_name)
            if need_refresh:
                timing =  time.time() + info_refresh['timing']
                print('before: ', self.ref_timing.get(table_name))
                self.ref_timing[table_name] = timing
                print('after: ', timing)
        elif tp == 'query':
            self.ref_timing[table_name] = time.time() * 2
        

    def read_table(self, table_name):
        ''' create table usng data of table in file info '''

        print(f'READ TABLE: {table_name}')
        #infromation at table
        info_tbl = self.info_table(table_name)
        #check if table need refresh
        if True:#table_name not in self.db or self.refresh_tables.get(table_name):
            #initial table by query or copy from table
        
            self.db[table_name] = self.create_table(info_tbl)
            info_ref = info_tbl.get('refresh')
            if info_ref:
                self.time_refresh(info_ref, table_name)   
            
            edit_commands = info_tbl.get('manipulation')

            if not self.db[table_name].empty or edit_commands:
                if edit_commands:
                    #create manipulation at data by list
                    self.manipulation(table_name, edit_commands)
        if table_name == 'main_table':
            self.db[table_name] = self.db[table_name].drop_duplicates(subset='data_studentsQid')

        self.db[table_name].to_csv(f'{table_name}.csv', encoding='ISO-8859-8')
        return self.db[table_name].astype(str)
