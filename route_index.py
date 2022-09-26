from flask import Blueprint,render_template,request,redirect

from conf import *
from tools import *
from datetime import datetime

import json , cryptocode


## Variables globales
dir_hosts = get_hosts()
dir_smtp  = get_smtp()
key       = get_key()

page_home = Blueprint('home',__name__,template_folder='templates')

@page_home.route("/")
def home():

	with open(dir_hosts,'r') as file:
		data = json.load(file)


	if(data[0]['Hostname'] != 'example.com'):
		firstExecution = False
	else:
		firstExecution = True


	count = {
		'cantidad':len(data),
		'update' : data[0]['Update']
	}

	return render_template('index.html',first=firstExecution, count=count,data=data)

@page_home.route('/checkConnection',methods=['POST'])
def checkConnection():
	'''
		Comprueba si es posible conectar
		arrojando los posibles errores
	'''
	r = request.form
	t = TestConection(r['ip'],r['user'],r['password'])
	return {'status':'OK','respuesta':t}

## Tambien se utiliza en apartado ver logs
@page_home.route('/updateLog',methods=['POST'])
def updateLog():
	"""
		Descarga y actualiza los logs, esta funcion
		puede ser llamada desde el index o en el view_log
  
		para el caso del index
	
		id[] -> obtendra un lista por post, lista de los indices para descargar los logs
  
		para el caso de view_log
  
		id -> obtendra un int , para descargar solamente los logs de un "Hostname"
	
 	"""
	with open(dir_hosts,'r') as file:
		data = json.load(file)
	r = request.form
	
	if(len(r.getlist('id[]')) >= 1):

		##Actualiza para todos
		for val in r.getlist('id[]'):
			val = int(val)
			password = cryptocode.decrypt(data[val]['Pass'], key)
			DescargarLog(data[val]['Hostname'],data[val]['IP'],data[val]['User'],password)
			date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
			date = str(dateparser.parse(date))

			data[val]['Update'] = date

		with open(dir_hosts,'w') as file:
			json.dump(data,file,indent=4)	
		
		return {'success':'OK','status':200} 
	else:
		###Caso para cuando se manda solo un id
		try :
			### Comprueba que sea un numero
			pos = int(r['id'])
			log_id = int(r['id_log'])
			password = cryptocode.decrypt(data[pos]['Pass'], key)
			DescargarLog(data[pos]['Hostname'],data[pos]['IP'],data[pos]['User'],password)

			hostname = data[pos]['Hostname']
			if(len(hostname.split(".")) > 1): 
				hostname = hostname.split(".")[0]
			

			contenido = os.listdir("Logs/"+hostname+"/")
			log_data = ProcesarLog(data[pos]['Hostname'],contenido[log_id])
			count_status = CountStatus(log_data)


			date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
			date = str(dateparser.parse(date))

			data[pos]['Update'] = date

			with open(dir_hosts,'w') as file:
				json.dump(data,file,indent=4)
			return {'success':'OK','status':200,'count':count_status,'data':log_data} 
		except (ValueError or Exception) as e :
			return {'success':'Error','status':400,'data':'NULL'} 
	###

@page_home.route("/addDomain",methods=['POST'])
def addDomain():
	'''
		Agrega los nuevos dominios de smtp 
		al json 

	'''
	r = request.form
	with open(dir_hosts,'r') as file:
		data = json.load(file)

	date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
	date = str(dateparser.parse(date))

	password = cryptocode.encrypt(r['password'],key) 
	

	if(data[0]['Hostname'] == "example.com"):
		data = [{'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':password,"Update":date}]
	else:
		data.append({'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':password,"Update":date})

	with open(dir_hosts,'w') as file:
		json.dump(data,file,indent=4)
	return redirect("/")
