
import hdate

class Tamplates:
    ''' 

    function:
    get: table, name_tamplate
    action: edit table by info at tamplate
    return: tamplate with data from table

    '''

    def json_form(self, name_tamplate, table):
        new_api = {}
        new_api['name_tamplate'] = name_tamplate
        dt_tamplte = self.config('tamplates')[name_tamplate]
        new_api['foramt'] = dt_tamplte['convert']['format']
        new_api['data'] = table.iloc[0].to_dict()
        
        return new_api
    
    def json_table(self, name_tamplate, table):
        new_api = {}
        formats = {
            'csv': table.to_csv(),
            'html':table.to_html(),
            'dict':[i.to_dict() for i in table.iloc]
            }
        dt_tamplte = self.config('tamplates')[name_tamplate]
        new_api['name_tamplate'] = name_tamplate
        new_api['format'] = dt_tamplte['convert']['format']
        new_api['data'] = formats[new_api['format']]
            
        return new_api
    
    def json_list(self, name_tamplate, table, tmp_type):
        new_api = {}
        dt_tmp = self.info_tamplate(name_tamplate)
        table.to_csv('en.csv', encoding='ISO-8859-8')
        new_api['data'] = table.to_dict('records')
        new_api['type'] = tmp_type
        new_api['name'] = name_tamplate
        new_api['translate'] = dt_tmp['translate']
        new_api['check_value'] = dt_tmp['check_value']
        new_api['style'] = dt_tmp['style']
        new_api['event'] = dt_tmp['event']
        return new_api
    
    def json_table_summery(self, name_tamplate, table):
        new_api = {}
        dt_tamplte = self.config('tamplates')[name_tamplate]
        new_api = dt_tamplte
        #table.rename(columns={'id': 'מזהה'}, inplace=True)
        table['id'] = table.index
        new_api['data'] = table.replace('nan', '0.0').replace('0.0', '0').replace('100.0', '100').to_dict('records')
        new_api['columnsInfo'] = self.info_columns(table)
        return new_api
    
    def json_dict(self, name_tamplate, table, tmp_type):
        new_api = {}
        dt_tamplte = self.info_tamplate(name_tamplate)
        new_api['data'] = table.iloc[0].to_dict()
        new_api['type'] = tmp_type
        new_api['name'] = name_tamplate
        
        return new_api
    
    def json_cards(self, name_tamplate, table, tmp_type):
        new_api = {}
        dt_tamplte = self.info_tamplate(name_tamplate)
        new_api['data'] = table.to_dict('records')
        new_api['varible'] = dt_tamplte['varible']
        new_api['type'] = tmp_type
        new_api['name'] = name_tamplate
        
        return new_api
    
    def json_buttons(self, name_tamplate, table, tmp_type):
        new_api = {}
        dt_tamplte = self.info_tamplate(name_tamplate)
        new_api['type'] = tmp_type
        new_api['varible'] = dt_tamplte['varible']
        new_api['type'] = tmp_type
        new_api['name'] = name_tamplate
        new_api['data'] = [{"value": "שיעור", "text": "שיעור"}, {"value":"חדר", "text": "חדר"}]
        return new_api
    
    
    def json_html(self, name_tamplate, table, tmp_type):
        new_api = {}
        new_api['type'] = tmp_type
        new_api['data'] =  '<div>'  + ' '.join(str(table)) + '</div>'
        return new_api
    
    def create_tamplate_fromat(self, tmp_type, name_tamplate, table):
        match tmp_type:
            case 'form':
                return self.json_form(name_tamplate, table)
            case 'table':
                return self.json_table(name_tamplate, table)
            case 'list':
                return self.json_list(name_tamplate, table, tmp_type)
            case 'table_summery':
                return self.json_table_summery(name_tamplate, table)
            case 'cards':
                return self.json_cards(name_tamplate, table, tmp_type)
            case 'buttons':
                return self.json_buttons(name_tamplate, table, tmp_type)
            case 'html':
                return self.json_html(name_tamplate, table, tmp_type)
            case 'dict':
                return self.json_dict(name_tamplate, table, tmp_type)


class ColumnInfo:

    def info_columns(self, table):
        info_columns = map(lambda n_col: self.info_one_col(n_col, table) , table.columns)
        return list(info_columns)
    
    def info_one_col(self, name_col, table):
        infc = self.convert_title(name_col)
        if infc['table'] in self.info_cols and infc['column'] in self.info_cols[infc['table']]:
            data_col = self.info_cols[infc['table']][infc['column']]
            if 'function' in data_col:
                
                func = self.convert_functions(data_col['function'], table[infc['id']])
                infc.update(func)
            infc.update(data_col)
        else:
            infc.update(self.info_cols['default'])
        infc['field'] = infc['id']
        
        infc['label'] = infc['name']

        return infc
      
    def conv_to_hebrew(self, column):
        from datetime import datetime

        new_info_col = {"type": "singleSelect", "editable": True}
        not_dup = column.drop_duplicates()
        get_heb = lambda day: datetime.strptime(day, "%Y-%m-%d")
        new_data = map(lambda day: {'value': day, 'label':str(hdate.HDate(get_heb(day)))[:-6]}, not_dup)
        new_info_col['minWidth'] = 220
        new_info_col['valueOptions'] = list(new_data)
        return new_info_col

    def convert_functions(self, func_name, column):
        match (func_name):
            case 'heberw_date':
                return self.conv_to_hebrew(column)
            case _:
                return {}
