import pandas as pd
from api import Apis

MEMORY_USERS = {}

def start_user(name, password):
    #check user:
    print(name, password)
    tbl_users = pd.read_csv('source/users.csv', encoding='ISO-8859-8').astype('str')
    print(tbl_users)
    tbl_users = tbl_users[
        (tbl_users['password'] == password)&
        (tbl_users['name'] == name)]
    print(tbl_users)
    if tbl_users.empty:
        return {'status':'not have user'}
    else:
        info_user = tbl_users.iloc[0].to_dict()
        return {'status': 'success', 'info': info_user}

def user_class(Id):
    #initial start by class
    
    print('\n\nUSER-ID: ', Id)
    if Id in MEMORY_USERS:
        return MEMORY_USERS[Id]
    else:
        MEMORY_USERS[Id] = Apis(Id)
        return MEMORY_USERS[Id]



def api_user(user_id, info, type_fetch):
    class_id = user_class(user_id)
    
    print(f'FECTH:\n  user_id: {user_id}\n  info: {info}\n  method:{type_fetch}')
    match type_fetch:
        case 'login':
            return start_user(**info)
        case 'depends':
            return class_id.api_depends(**info)
        case 'screen':
            return class_id.api_screen()
        case 'tamplate':
            return class_id.api_tamplate(**info)
        case 'event':
            return class_id.api_event(**info)
        case _:
            return {}



if __name__ == '__main__':
    import time
    start = time.time()
    data = api_user('1', {'name_tamplate': 'table_info'}, 'tamplate')
    print(time.time() - start)


"""
def api_screens(user_id, tamplate=''):
    
    return MEMORY_USERS[user_id].tamplate_style() if (user_id) else {}

def api_tampltes(user_id, tamplate):
    MEMORY_USERS[user_id].db = {}
    return MEMORY_USERS[user_id].api_tamplate(tamplate) if (user_id) else {}

def api_event(user_id, event_info):
    MEMORY_USERS[user_id].db = {}
    return MEMORY_USERS[user_id].api_event(**event_info)if (user_id) else {}

    

    def api_login(name: str ='', password: str=''):
    api = {}
    api['user_status'] = user_status(name, password)
    print(api)
    add_user(api['user_status']['info'])
    #if api['user_status']['status'] == 'success':
    #    user_class = add_user(api['user_status']['info'])
    #    api['tamplates'] = user_class.tamplate_style()
    api['status'] = api['user_status']['status']
    return api
"""
