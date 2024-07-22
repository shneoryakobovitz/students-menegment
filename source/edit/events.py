
import pandas as pd

class Events:
    '''
    
    function: convert data to query
    get: data, info query.
    action: change data by info query.
    retturn: query from info and data.
    
    '''
    def convert_to_sql(self, df):
        return f''' {str(tuple(df.columns)).replace("'","")} VALUES {str([tuple(i) for i in df.values])[1:-1]} '''
    
    def c_table_query(self, data, info_query):
        df = pd.DataFrame(data)
        df = self.filter_table_orginal(df, name_table=info_query['table'])
        df = self.check_pivot(df)

        return self.convert_to_sql(df)

    def c_list_sql(self, data, info_query):
        df = pd.DataFrame(data)
        vals = [v for v in info_query['list'].values() if not '{' in v]
        df = df[vals]
        df[info_query['replace']] = df[info_query['replace']].astype(str).replace(info_query['replace']['values'])
        for name_col, val in info_query['list'].items():
            if "{" in val:
                df[name_col] = self.str_var(val)
            else:
                df = df.rename(columns={val: name_col})
        text_sql = self.convert_to_sql(df)
        d = {'"':""}
        for k, v in d.items():
            text_sql = text_sql.replace(k, v)
        
        for k, v in info_query['list'].items():
            if 'key' in v:
                text_sql = text_sql.replace(v.split('$')[1], k)
        
        return text_sql

    def c_form_simple(self, data, info_query=''):
        new_q = map(lambda key: f'{key} = "{data[key]}" ',data.keys())
        return ' ,'.join(list(new_q))
    
    def update_frmt(self, type_frmt, data, info_query):
        match type_frmt:
            case 'form_simple':
                return self.c_form_simple(data, info_query)
            case 'values_sql':
                return self.c_list_sql(data, info_query)
            case 'table_query':
                return self.c_table_query(data, info_query)

class QueryUpdate:

    def check_pivot(self, table):
        #replace this
        columns = [col for col in table.columns if col.count('Q') == 4]
        print('columns: ', columns)
        if columns:
            column_t = self.convert_title(columns[0])
            index = [col for col in table.columns if col not in columns]
            rep_col = {col: self.convert_title(col)['name'] for col in columns}
            table.rename(columns=rep_col, inplace=True)
            table = table.melt(id_vars=index, var_name=column_t['org_column'], value_name=column_t['column'])
            rep_col = {col:f"{column_t['table']}Q{col}" for col in table.columns if not 'Q' in col}
            table.rename(columns=rep_col, inplace=True)
        
        return table

    def filter_table_orginal(self, table, name_table):
        table.to_csv('21.csv', encoding="ISO-8859-8")
        columns_filter = [i for i in table.columns if self.convert_title(i)['table'] == name_table]
        print('columns_filter: ', columns_filter)
        return table[columns_filter]
    
    def convert_update_query(self, info_query, event_info, data_update):
        new_query = info_query['query']
        new_query = new_query.replace('name_table', event_info['table'])
        new_query = new_query.replace(info_query['type_query'], self.update_frmt(info_query['type_query'], data_update, event_info))
        new_query = self.change_query(new_query)
        print('new_query:',new_query)
        return new_query
    