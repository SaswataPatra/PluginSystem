# import database_connection
import os

# def testing():
#     conn = database_connection.connection()

#     cur = conn.cursor()

#     cur.execute("SELECT * FROM company")
#     data = cur.fetchall()
#     print(data)
#     cur.close()
#     conn.close()


# import buissnessLogic
# import importlib

# x = importlib.import_module('buissnessLogic.hello')
# my_method = getattr(x, "hello_func")
# print(my_method("Hello"))

# def testing():
#     request={
#         "hello" : "bade",
#         "Mello" : 0
#     }
#     for item in request.values():
#         if type(item)!=int or (item!=0 and item!=1):
#             return "Bad request..\n field values of question can either be 0 or 1"
#     return "All good"


# print(testing())
from dotenv import load_dotenv
def testing():
    load_dotenv()
    x = os.environ.get("TWITTER_API_KEY")
    print (x)


testing()