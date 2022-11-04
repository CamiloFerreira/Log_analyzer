from conf import db,key
from tools import * 
from flask import Blueprint,render_template,request
import json,os

page_inbox = Blueprint('inbox',__name__,template_folder='templates')


def getHosts():
	servidores = db.getServidores()
	aHost = []
	for serv in servidores:
		aHost.append(serv['hostname'])
	return aHost

@page_inbox.route("/SpamCheck",methods=['POST'])
def getSpamcheck():
	hosts = getHosts()
	r = request.form
	try : 
		id_host = int(r['id'])
		update  = bool(r['descargar'])
		spam = db.getSpam(id_host)
		if( spam == [] or update == True):
			spam = SpamCheck(hosts[id_host])
			db.deleteSpam(id_host)
			for s in spam:
				s['id_host'] = id_host
			db.insertarSpam(spam)

		return {'success':'OK','status':200,'data':spam} 
	except:
		return {'success':'Error','status':400,'data':'NULL'} 

@page_inbox.route("/virusCheck",methods=['POST'])
def virusCheck():
	hosts = getHosts()
	r = request.form
	print(r)
	try : 
		id_host = int(r['id'])
		update  = bool(r['descargar'])
		virus = db.getVirus(id_host)

		if(virus == [] or update == True):
			virus = AlertasVirus(hosts[id_host])
			db.deleteVirus(id_host)
			if(virus[0]['para'] != "" and virus[0]['de'] !=""):
				for v in virus:
					s['id_host'] = 0		
				db.insertarVirus(virus)
			
		return {'success':'OK','status':200,'data':AlertasVirus(hosts[id_host])} 
	except:
		return {'success':'Error','status':400,'data':'NULL'} 



@page_inbox.route("/inboxLog/<tipo>")
def inboxLog(tipo="spam"):
	hosts = getHosts()
	if(tipo == str("spam")):
		spam = db.getSpam(0)
		if( spam == []):
			spam = SpamCheck(hosts[0])
			for s in spam:
				s['id_host'] = 0
			db.insertarSpam(spam)
		return render_template('analyze_spam.html',url=request.url_root,dic=spam,hosts=hosts)
	elif(tipo == str("virus")):
		
		virus = db.getVirus(0)

		if(virus == []):
			virus = AlertasVirus(hosts[0])
			db.deleteVirus(0)
			if(virus[0]['para'] != "" and virus[0]['de'] !=""):
				for v in virus:
					s['id_host'] = 0		
				db.insertarVirus(virus)

		return render_template('analyze_virus.html',url=request.url_root,dic=virus,hosts=hosts)