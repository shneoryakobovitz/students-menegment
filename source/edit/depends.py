import time


class Depends:
    

    @property
    def list_tamplates(self):
        user_tamp = self.config('users')[self.info_user['type']]
        #create one list
        tamplates = [val[0] for _, val in user_tamp.items()]
        return tamplates

    def refresh_table(self, table, time_old):
        updates = self.read_depends(table) > int(str(time_old))        
        timing = self.ref_timing[table] < time.time() if table in self.ref_timing else True
        return updates and timing

    def check_refresh_tables(self, time_old):
        for table in self.db:
             self.refresh_tables[table] = self.refresh_table(table, time_old)
        
        return self.refresh_tables
    
    def refresh_tamplates(self, time_old):
        refresh_tamp = {}
        self.check_refresh_tables(time_old)
        for tm in self.list_tamplates:
            tbl_n = self.info_tamplate(tm)['table']
            tbl_refresh = self.refresh_tables.get(tbl_n)

            #if table not in list refresh table that first call and needed refresh
            refresh_tamp[tm] = tbl_refresh if tbl_refresh else True

        return {"screen_students":True, "cards":True, "buttons":True}

state_tamplate =''
tamplate_screen = []
state_tamplates = ''
async def start_fetch_info_tamplate():
    pass
def state_info_tamplates():
    pass
async def refresh_tamplate():
    pass
def state_change_only_info_in_tamplate():
    pass










async def start_tamplates():
    for tamplate in tamplate_screen:
          if tamplate not in state_tamplates:
              info = await start_fetch_info_tamplate(tamplate)
              state_info_tamplates(info) # update info at tamplate
              state_tamplate(tamplate(info))

async def load_refresh():
    refresh_tamplates = await refresh_tamplate()#return list info at refreshing - [tamplate]
    for tamplate in refresh_tamplates:
        info = await start_fetch_info_tamplate(tamplate)
        if info['type'] == state_info_tamplates[tamplate]['type']:
            state_change_only_info_in_tamplate()
        else:
            #all tamplate changed
            state_tamplate(tamplate(info))

async def demo_client_request_refresh():
    if state_tamplate == {}: #start program
      await start_tamplates()
    else:
      #tamplate in state_tamplates
      await load_refresh()
