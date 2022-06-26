import database_connection

def create(request,name,pk):
    try:
        conn = database_connection.connection()
        for item in request.values():
            if type(item)!=int or (item!=0 and item!=1):
                return False,"Bad request..\n field values of question can either be 0 or 1"
        cur = conn.cursor() 
        cur.execute(f'DROP TABLE IF EXISTS {name};')
        if not pk:
            cur.execute(f'CREATE TABLE {name} (id serial PRIMARY KEY)')
        else:
            cur.execute(f'CREATE TABLE {name} (id serial,'
                                                f'{pk} varchar (150) NOT NULL)')
        for key in request:
            if pk==key:
                continue
                # cur.execute(f'ALTER TABLE {name} ADD {key} varchar(200) PRIMARY KEY')
            elif request[key]==0:
                cur.execute(f'ALTER TABLE {name} ADD {key} varchar(200)')
            else:
                cur.execute(f'ALTER TABLE {name} ADD {key} varchar(200) NOT NULL')
        
        conn.commit()
        cur.close()
        conn.close()
        return True,"Questions posted successfully"
    except:
        return False,"Unknown error occured"

def user_test(request,name):
    question_dict = request['questionConfig']
    table_dict = request['tableConfig']
    name = table_dict['tableName']
    pk = table_dict['primary_key']

    conn = database_connection.connection()

    cur = conn.cursor()
    for key in request:
        cur.execute(f'INSERT INTO ')


request = {
   "questionConfig":{
    "name": 0,
    "age": 0,
    "phone_number" : 0,
    "monthly_income" : 1
},
"tableConfig":{
    "tableName": "company_name",
    "primary_key" : "age",
}
}


# create(request,'company')