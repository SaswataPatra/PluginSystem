import os
from os.path import exists
def create(name):
    pwd = os.getcwd()
    pwd= os.path.join(pwd,'buissnessLogic')
    path = f'{pwd}/{name}.py'
    if exists(path):
        return (f'file - {name}.py already exists \n path - {path}')
    else:
        f = open(path,"w")
        f.write(f'def {name}_func(request) -> bool:\n\t #plugin developers code goes here \n\t pass')
        return (f'file {name}.py created successfully!! \n Path - {path}')

create("hello")