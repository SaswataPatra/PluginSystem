
from flask import Flask,jsonify,request,json,abort
from numpy import require
# from flask_mysqldb import MySQL
import psycopg2
import create_table,create_logic_files as cf,user_response as usr
# from requests import request
# from flask_restful import reqparse
app = Flask(__name__) # referencing this file

conn = psycopg2.connect(
        host="postgresdb.ctgcc3olpy9z.ap-south-1.rds.amazonaws.com",
        database="atlan",
        user='postgres',
        port = 5432,
        password='password')

# mysql = MySQL(app)

# admin_json = reqparse.RequestParser()
# admin_json.add_argument("name", type=str, help="Name of the video is required", required=True)
# request = {
#    "questionConfig":{
#     "name": 0,
#     "age": 0,
#     "phone_number" : 0,
#     "monthly_income" : 1
# },
# "tableConfig":{
#     "tableName": "company_name",
#     "primary_key" : "age",
# }
# }
@app.route('/')
def index():
    # cur = mysql.connection.cursor()
    return "hello World"
@app.route('/admin/set-questions',methods=['POST'])
def admin_set_question():
    try:
        tableConfig = request.json['tableConfig']
        questionConfig = request.json['questionConfig']
        tableConfig = request.json['tableConfig']
        tableName = tableConfig['tableName']
        pk = tableConfig['primary_key']
        create_table.create(questionConfig,tableName,pk)
        value = cf.create(tableName)
    except:
        abort(404,"json not in format")
    return jsonify({"msg":value})
@app.route('/user/response',methods=['POST'])
def user_response():
    required_fields = request.json['required_fields']
    not_required_fields = request.json['not required fields']
    val,err=usr.isValidResponseReqFields(required_fields,not_required_fields)
    if not val:
        return jsonify({"msg":err})
    val,err=usr.isValidResponseForNotReqFields(not_required_fields,required_fields)
    if not val:
        return jsonify({"msg":err})
    else:
        val,err = usr.check_buissness_logic(required_fields)
        if not val:
            return jsonify({"msg":err})
        else:
            required_fields.update(not_required_fields)
            val,err = usr.insert_valid_response(required_fields)
            if not val:
                return jsonify({"msg":err})
            else:
                return ("Valid response")
if __name__ == "__main__":
    app.run(debug=True)






