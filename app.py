
from flask import Flask,jsonify,request,abort 
import smtplib
import create_table,create_logic_files as cf,user_response as usr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import re
import os
app = Flask(__name__) # referencing this file

load_dotenv()
from_ = os.environ.get('MAIL_ADDRESS')
your_pass = os.environ.get('MAIL_PASSKEY')

def send(to): #smtp mail sending
    try:
        if(not re.search(os.environ.get("REGEX"),to)):   #valid email check
            return False,("Invalid Email")  
        body = "Hello World"
        subject = 'Verification successfull'
        message = MIMEMultipart()
        message['From'] = from_
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(from_,your_pass)
        mail.sendmail(from_,to, text)
        mail.close()
        return True,"Mail sent successfully"
    except:
        return False,"Error in sending mail"

@app.route('/')
def index(): #dummy function for home
    return "hello World"
@app.route('/admin/set-questions',methods=['POST'])#admin question creation api
def admin_set_question():
    try:
        tableConfig = request.json['tableConfig']
        questionConfig = request.json['questionConfig']
        tableConfig = request.json['tableConfig']
        tableName = tableConfig['tableName'].lower()
        pk = tableConfig['primary_key']
        val,err1=create_table.create(questionConfig,tableName,pk)
        print("Table created",val)
        if not val:
            return jsonify({"msg":err1})
        val,err2 = cf.create(tableName)
        print("File created",val) #initial plugin file creation with default values
        if not val:
            return jsonify({"msg":err2})
    except:
        abort(400,"Bad request...json not in format")
    msg = f'{err1}    {err2}'
    return jsonify({"msg":msg})
@app.route('/user/response',methods=['POST'])#user response fetching api and validation
def user_response():
    try:
        required_fields = request.json['required_fields']
        not_required_fields = request.json['not_required_fields']
    except: 
        abort(400," Bad request,json not in format...")
    try:
        required_fields['tableName'] = required_fields.get('tableName').lower()
        val,err=usr.isValidResponseReqFields(required_fields,not_required_fields)
        print("Req field : ",val,err)
        if not val:
            return jsonify({"msg":err})
        val,err=usr.isValidResponseForNotReqFields(not_required_fields,required_fields)
        print("Req field : ",val,err)
        if not val:
            return jsonify({"msg":err})
        else:
            val,err = usr.check_buissness_logic(required_fields) #plugin validation 
            if not val:
                return jsonify({"msg":err})
            else:
                
                required_fields.update(not_required_fields)
                val,err = usr.insert_valid_response(required_fields)
                if not val:
                    return jsonify({"msg":err})
                else:
                    print("Ima in mail")
                    address = required_fields.get('mail') #mail sending
                    if address is not None:
                        val,err = send(address)
                    if not val:
                        return jsonify({"msg":err})
                    return jsonify({"msg":"Valid response "+err})
    except:
        abort(500,"Unknown error occured")

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG'))






