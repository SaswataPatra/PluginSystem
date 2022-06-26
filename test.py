# import database_connection

# def testing():
#     conn = database_connection.connection()

#     cur = conn.cursor()

#     cur.execute("SELECT * FROM company")
#     data = cur.fetchall()
#     print(data)
#     cur.close()
#     conn.close()


import buissnessLogic
import importlib

x = importlib.import_module('buissnessLogic.hello')
my_method = getattr(x, "hello_func")
print(my_method("Hello"))

