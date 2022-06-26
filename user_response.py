import database_connection
import os
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
            return False,"JSON not in format... \n not_required_field values present in required_field values"
        cur.execute(f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS COL WHERE TABLE_NAME = \'{tableName}\' AND COL.is_nullable=\'NO\';')
        # cur.execute(f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{tableName}\';')
        data = cur.fetchall()
        lst =[]
        for items in data:
            lst.append(items[0])
        lst.remove("id")
        print(lst)
        for items in lst:
            if items not in response.keys():
                return False,"json not in format for required fields....\n all required fields not filled"
        return True,""
    except:
        return False,"TABLE DOES NOT EXIST"

def isValidResponseForNotReqFields(response,required_fields):
    # if "tableName" not in required_fields.keys():
    #     return False,"JSON not in format \n tableName key required"
    # else:
    tableName=required_fields["tableName"]
    conn = database_connection.connection()
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{tableName}\';')
        data = cur.fetchall()
        diff = set(response) - set(required_fields) 
        if len(diff)!=len(response):
            return False,"JSON not in format... \n required_field values present in not_required field values"
        lst =[]
        for items in data:
            lst.append(items[0])
        lst.remove("id")
        print(lst)
        for items in response.keys():
            if items not in lst:
                return False,"json not in format for not-required fields..\n value to non-existing key present"
        return True,""
    except:
        return False,"UNEXPECTED ERROR OCCURED.. Check tableName"


def check_buissness_logic(response):
    try:
        tableName = response['tableName']
        response.pop('tableName')
        x = importlib.import_module('buissnessLogic.hello')
        function_name = tableName+"_func"
        my_method = getattr(x, function_name)
        res = my_method(response)
        if res is None:
            return False, f'Plugin for {tableName} still in development'
        else:
            return True,''
    except:
        return False,"Unexpected error occured"
def insert_valid_response(response):
    try:
        tableName = response['tableName']
        response.pop('tableName')
        conn = database_connection.connection()
        cur = conn.cursor()
        
    except:
        pass



resp = {
    "name" : "Saswata",
    "age" : "98",
    "phone_number" : "980",
    # "monthly_income" : "89",
}
res ={
    "monthly_income" : "789",
    "tableName" : "hello"
}
val,err=isValidResponseReqFields(res,resp)
print(val,":",err)

# val,err=isValidResponseForNotReqFields(resp,res)
# print(val,":",err)
