# from flask import request
# import database_connection
import create_table
import create_logic_files
def check(request):
    name = request['name']
    
    create_logic_files(name) 
    create_table.create(request,name)
