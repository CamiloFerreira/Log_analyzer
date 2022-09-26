from tools import * 
from conf import * 
from flask import Blueprint,render_template,request,redirect
import json,os

page_mailer = Blueprint('mailer',__name__,template_folder='templates')

## Variables globales
dir_hosts = get_hosts()
dir_smtp  = get_smtp()
key       = get_key()

@page_mailer.route("/mailer")
def mailer():	
	data = [{'hostname':"Example.com","from":"","user":"","password":""}]
	if (os.path.exists(dir_smtp) == False):
		firstExecution = True
	else:
		firstExecution = False
		with open(dir_smtp,"r") as f:
			data = json.load(f)

	return render_template('mailer.html',first=firstExecution,data=data)

@page_mailer.route("/addSMTP",methods=['POST'])
def addSMTP():
	r = request.form
	data = []
	if( os.path.exists(dir_smtp) == False):
		with open(dir_smtp,"w") as f:
			data.append({'hostname': r['hostname'],'from':r['from'],'user':r['user'],'password':r['password']})
			json.dump(data,f,indent=4)
	else:
		with open(dir_smtp,"r") as f:
			data = json.load(f)
		data.append({'hostname': r['hostname'],'from':r['from'],'user':r['user'],'password':r['password']})


	with open(dir_smtp,"w") as f:
		json.dump(data,f,indent=4)

	return redirect("/mailer")

@page_mailer.route("/sendMail_test",methods=["POST"])
def sendMail_test():
	r = request.form  
	return SendMail(r['host'],r['user'],r['password'],r['from'],r['to'],r['subject'],r['content'])
@page_mailer.route("/sendMail",methods=["POST"])
def sendMail():
	r = request.form 
	id_smtp = 0
	data = []
	with open(dir_smtp,"r") as f:
		data = json.load(f)

	return SendMail(data[id_smtp]['hostname'],data[id_smtp]['user'],data[id_smtp]['password'],r['from'],r['to'],r['subject'],r['content'])