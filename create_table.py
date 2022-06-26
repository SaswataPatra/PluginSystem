import database_connection

def create(request,name,pk):#on the fly table creation 
    try:
        conn = database_connection.connection()
        for item in request.values():
            if type(item)!=int or (item!=0 and item!=1):
                return False,"Bad request..\n field values of question can either be 0 or 1"
        cur = conn.cursor() 
        cur.execute(f'DROP TABLE IF EXISTS {name};')
        if not pk:
            cur.execute(f'CREATE TABLE {name} (id serial PRIMARY KEY)') # if primary key isnt set id is set as default
        else:
            cur.execute(f'CREATE TABLE {name} (id serial,'
                                                f'{pk} varchar (150) NOT NULL)') # if pk is set by admin-ser explicitly
        for key in request:
            if pk==key:
                continue
            elif request[key]==0:
                cur.execute(f'ALTER TABLE {name} ADD {key} varchar(200)')# on the fly ddl operations 
            else:
                cur.execute(f'ALTER TABLE {name} ADD {key} varchar(200) NOT NULL')
        
        conn.commit()
        cur.close()
        conn.close()
        return True,"Questions posted successfully"
    except:
        return False,"Unknown error occured"


