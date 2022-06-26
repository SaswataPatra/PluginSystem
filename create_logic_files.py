import os
from os.path import exists
def create(name): #automatic creation of files as per question set by admin-user
    try:
        pwd = os.getcwd()
        pwd= os.path.join(pwd,'buissnessLogic')
        path = f'{pwd}/{name}.py'
        if exists(path):
            return True,(f'file - {name}.py already exists \n path - {path}')
        else:
            f = open(path,"w")
            f.write(f'def {name}_func(request) -> bool:\n\t#plugin developers code goes here \n\treturn None,\'\'')
            return True,(f'file {name}.py created successfully!! \n Path - {path}')
    except:
        return False,"Unknown error occured while creating files"

# val,err=create("sello")
# print(val,err)