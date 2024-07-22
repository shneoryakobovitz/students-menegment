import pandas as pd
from api import Apis

MEMORY_USERS = {}

def start_user(name, password):

    tbl_users = pd.read_csv('source/users.csv', encoding='ISO-8859-8').astype('str')
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
    if Id in MEMORY_USERS:
        return MEMORY_USERS[Id]
    else:
        MEMORY_USERS[Id] = Apis(Id)
        return MEMORY_USERS[Id]



def api_user(user_id, info, type_fetch):
    class_id = user_class(user_id)
    
    # print(f'FECTH:\n  user_id: {user_id}\n  info: {info}\n  method:{type_fetch}')
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
