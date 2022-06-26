import database_connection
import importlib
def isValidResponseReqFields(response,not_required_fields):
    if "tableName" not in response.keys():
        return False,"JSON not in format \n tableName key required"
    else:
        tableName=response["tableName"]
    conn = database_connection.connection()
    cur = conn.cursor()
    try:
        diff = set(response) - set(not_required_fields) 
        if len(diff)!=len(response):
            return False,"JSON not in format... \n not_required_field values present in required_field values" #checking whether values in required fields and not_required fields co incide 

        cur.execute(f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS COL WHERE TABLE_NAME = \'{tableName}\' AND COL.is_nullable=\'NO\';')# fetching the coloumn names which has been set as not null
    except:
        return False,"Table does not exist"
    try:
        data = cur.fetchall()
        lst =[]
        for items in data:
            lst.append(items[0])
        lst.remove("id")
        for items in lst:
            if items not in response.keys():
                return False,"json not in format for required fields....\n all required fields not filled"
        
        return True,"success"
    except:
        return False,"Unexpected error occured"


def isValidResponseForNotReqFields(response,required_fields):
    tableName=required_fields["tableName"]
    conn = database_connection.connection()
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{tableName}\';') #fetching the column names
        data = cur.fetchall()
        diff = set(response) - set(required_fields) 
        if len(diff)!=len(response):
            return False,"JSON not in format... \n required_field values present in not_required field values"
        lst =[]
        for items in data:
            lst.append(items[0])
        lst.remove("id")
        # print(lst)
        for items in response.keys():
            if items not in lst:
                return False,"json not in format for not-required fields..\n value to non-existing key present"
        return True,"success"
    except:
        return False,"UNEXPECTED ERROR OCCURED.. Check tableName"


def check_buissness_logic(response):
    try:
        tableName = response['tableName']
        print("table:",tableName)
        path = f'buissnessLogic.{tableName}'
        x = importlib.import_module(path)
        function_name = tableName+"_func"
        print("function name",function_name)
        my_method = getattr(x, function_name)
        res,msg= my_method(response)
        print("Response : ",res)
        if res is None:
            return False, f'Plugin for {tableName} is still in development' #Initial phase
        else:
            return res,msg #After development
    except:
        return False,"Unexpected error occured"

def insert_valid_response(response):  # Value insertion in table after validation
    try:
        # print("response1",response)
        tableName = response['tableName']
        tmp = response.copy()
        tmp.pop('tableName')

        conn = database_connection.connection()
        cur = conn.cursor()

        placeholders = ', '.join(['%s'] * len(tmp))
        columns = ', '.join(tmp.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tableName, columns, placeholders)
        cur.execute(sql, list(tmp.values()))
        
        conn.commit()
        cur.close()
        conn.close()
        return (True,"Successfully validated response")
    except:
        return (False,"An unexpected error occured")
