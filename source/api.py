from edit.events import Events, QueryUpdate
from edit.table import Table
from edit.tamplate import ColumnInfo, Tamplates
from db import ReadDataBase
from edit.depends import Depends

class Apis(
    QueryUpdate,
    Events,
    Table,
    Depends,
    ColumnInfo,
    Tamplates,
    ReadDataBase
    ):
    
    '''
    
    title: response to client by data to insert.

    
    name function | return       |
    ==============================
    api_screen   | screens      |
    ==============================
    api_tamplate  | tamplate     |
    ==============================
    api_event     | status event |
    ==============================


    '''

    def __init__(self, user_id) -> None:
        super(Apis).__init__()
        self.user_id = user_id
                
    def api_screen(self):
        ''' user screens '''

        scrns = self.config('users')[self.info_user['type']]
        new_screens = {}
        for screen in scrns:
            new_tam_list = []
            for tam in scrns[screen]:
                info_tam = self.config('tamplates')[tam]
                info_tam['name'] = tam
                new_tam_list.append(info_tam)
            new_screens[screen] = new_tam_list
        return new_screens

    def api_depends(self, time_old):
        ''' '''
        api = self.refresh_tamplates(time_old)
        return api 

    def api_tamplate(self, name_tamplate: str ):
        ''' create api using table and covert to format '''
        #info of tamplates
        
        tamplate_info = self.info_tamplate(name_tamplate)
        table = self.read_table(table_name=tamplate_info['table'])
        if table.empty:
            #If an empty table refersh to another template.
            api = self.api_tamplate(
                tamplate_info['tamplate_if_empty'])
            
        else:
            #Create tamplate fromat using tamplate and table data.
            api = self.create_tamplate_fromat(
                tmp_type=tamplate_info['type_tamplate'],
                name_tamplate=name_tamplate,
                table=table
            )
        return api
        
        

    def api_event(self, info_event, data):

        info_query = self.config('events')[info_event['event']]
        print('info_query: ', info_query)
        query = self.convert_update_query(info_query, info_event, data)
        connect = self.update_to_db(query)
        if connect['connect']:
            self.export_depends(info_query['depends'])
            return {
                'status': 'success',
                'query': query,
                'response': info_query['response']['success']}
        else:
            return {
                'statue': 'fail',
                'response': info_query['response']['fail'],
                'exept': connect['info'].replace('"',"'")
                }