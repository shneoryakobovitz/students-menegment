from datetime import datetime
import pytz
import os
import time

'''
functions convert to python object and varibles.
'''

class Functions:

    ''' functions them not belong with database 
    
    '''

    def date_now(self):
        date_loc = pytz.timezone(os.getenv("LOCATION"))
        date_loc = datetime.now(date_loc).date()
        return f'{date_loc}'

    def time_now(self):
        date_loc = pytz.timezone(os.getenv("LOCATION"))
        dt = datetime.now(date_loc).time()
        full = lambda x: x if len(str(x)) == 2 else f'0{x}'
        return f'{dt.hour}{full(dt.minute)}'
    
    def path_functions(self, func):
        match func:
            case 'date_now': 
                return self.date_now()
            case 'time_now': 
                return self.time_now()


class Var(Functions):
    
    ''' path functions (word) '''

    def var_table(self, val):
        #return format matches the query sting
        table = self.read_table(val)
        print(table)
        table = 'empty' if table.empty else table.iloc[0][0]
        return table
    
    def var(self, type_var, val):
        match type_var:
            case 'value':
                return val
            case 'function':
                return self.path_functions(val)
            case 'table':
                return self.var_table(val)
            case 'user':
                return self.info_user[val]


class SentencesConvert(Var):
    
    '''
    
    function: convert string to python format.
    get: sentence or word
    action: chnage sentance.
    return: object with real data.
    
    '''
    
    def str_var(self, word):
        if '{' and ':' and '}' in word:
            start, key, val, end = word[:word.find('{')], word[word.find('{')+1:word.find(':')], word[word.find(':')+1: word.find('}')], word[word.find('}')+1:]
            if key == 'table':
                self.read_table(val)
            return f'{start}{self.var(type_var=key, val=val)}{end}'
        else:
            return word
        
    def time_n(self):
        return int(time.time())
    
    def convert_title(self, column_name):
        d = column_name.split('Q')
        var = {'table': d[0],
               'column': d[1] if len(d)> 1 else 'id', 'name':d[-1], 'id': column_name}
        if len(d) == 5:
            var['org_table'] = d[2]
            var['org_column'] = d[3]
        
        return var

    def change_query(self, query):
        ''' getting string query and change to sql query '''

        new_query_list = [str(self.translate('word', word)) for word in query.split()]
        new_query_list = ' '.join(new_query_list)
        
        return new_query_list
    
    def translate(self, type_trans, value):
        match type_trans:
            case 'word':
                return self.str_var(value)
            case 'title_column':
                return self.convert_title(value)
            case 'query':
                return self.change_query(value)