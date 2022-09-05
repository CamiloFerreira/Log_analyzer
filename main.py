from flask import Flask,render_template,request,redirect
from werkzeug import exceptions
from datetime import datetime
from tools import *
import json,os,dateparser
#

app = Flask(__name__)

@app.route('/updateLog',methods=['POST'])
def updateLog():

	with open('hosts.json','r') as file:
		data = json.load(file)
	r = request.form
	
	if(len(r.getlist('id[]')) >= 1):

		##Actualiza para todos
		for val in r.getlist('id[]'):
			val = int(val)
			DescargarLog(data[val]['Hostname'],data[val]['IP'],data[val]['User'],data[val]['Pass'])
			
			date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
			date = str(dateparser.parse(date))

			data[val]['Update'] = date

		with open('hosts.json','w') as file:
			json.dump(data,file,indent=4)	
		
		return {'success':'OK','status':200} 
	else:
		###Caso para cuando se manda solo un id
		try :
			### Comprueba que sea un numero
			pos = int(r['id'])

			DescargarLog(data[pos]['Hostname'],data[pos]['IP'],data[pos]['User'],data[pos]['Pass'])

			hostname = data[pos]['Hostname']
			if(len(hostname.split(".")) > 1): 
				hostname = hostname.split(".")[0]
			

			contenido = os.listdir("Logs/"+hostname+"/")
			log_data = ProcesarLog(data[pos]['Hostname'],'mail.log')
			count_status = CountStatus(log_data)


			date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
			date = str(dateparser.parse(date))

			data[pos]['Update'] = date

			with open('hosts.json','w') as file:
				json.dump(data,file,indent=4)
			return {'success':'OK','status':200,'count':count_status,'data':log_data} 
		except (ValueError or Exception) as e :
			return {'success':'Error','status':400,'data':'NULL'} 
	###



@app.route('/checkConnection',methods=['POST'])
def checkConnection():
	'''
		Comprueba si es posible conectar
		arrojando los posibles errores
	'''
	r = request.form
	t = TestConection(r['ip'],r['user'],r['password'])
	return {'status':'OK','respuesta':t}



@app.route("/addDomain",methods=['POST'])
def addDomain():
	'''
		Agrega los nuevos dominios de smtp 
		al json 

	'''
	r = request.form
	with open('hosts.json','r') as file:
		data = json.load(file)

	date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
	date = str(dateparser.parse(date))

	if(data[0]['Hostname'] == "example.com"):
		data = [{'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':r['password'],"Update":date}]
	else:
		data.append({'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':r['password'],"Update":date})

	with open('hosts.json','w') as file:
		json.dump(data,file,indent=4)
	return redirect("/")


@app.route('/view', methods=['GET'])
def view():

	'''
		Pagina principal que contiene la tabla donde se mostraran los estados
		de los correos enviados

	'''
	
	try :
		pos = int(request.args.get('id'))
	except (ValueError or Exception) as e :
		pos = 0 
	
	with open('hosts.json','r') as file:
		data = json.load(file)

	hostname = data[pos]['Hostname']
	if(len(hostname.split(".")) > 1): 
		hostname = hostname.split(".")[0]
	

	contenido = os.listdir("Logs/"+hostname+"/")
	log_data = ProcesarLog(data[pos]['Hostname'],'mail.log')
	count_status = CountStatus(log_data)

	return render_template('view_log.html',dic=log_data,count=count_status)#,dic=log_data,data=data,contenido=contenido)

@app.route("/showLog")
def showLogFull():
	with open('hosts.json','r') as file:
		data = json.load(file)	


	hostname = str(data[0]['Hostname'].split(".")[0])

	contenido = os.listdir("Logs/"+hostname+"/")
	file = open("Logs/"+hostname+"/mail.log")
	aLines = [line.strip() for line in file.readlines()[::-1]]


	return render_template('show_full.html',data=data,log=aLines,file_list=contenido)

@app.route("/getLog",methods=['POST'])	
def getLog():

	r = request.form
	pos =int(r['id'])
	pos_file = int(r['log'])
	hostname =data[pos]['Hostname'].split(".")[0]
	contenido = os.listdir("Logs/"+hostname+"/")
	
	file = open("Logs/"+hostname+"/"+contenido[pos_file])
	aLines = [line.strip() for line in file.readlines()[::-1]]	

	return {'status':'ok','data':aLines}

@app.route("/")
def home():

	with open('hosts.json','r') as file:
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

@app.route("/dashboard")
def dashboard():
	log_data = ProcesarLog(data[0]['Hostname'],'mail.log')
	return render_template('dashboard.html',log_data=log_data)


if  __name__=="__main__":	
	global data 
	global firstExecution 

	data = []
	firstExecution = True


	date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
	date = str(dateparser.parse(date))
	if(os.path.exists("hosts.json") == False):
		data = [{'Hostname':'example.com','IP':'example','User':'example','Pass':'12345',"Update":date}]
		with open('hosts.json','w') as file:
			json.dump(data,file,indent=4)

	with open('hosts.json','r') as file:
		data = json.load(file)
	if(data[0]['Hostname'] != 'example.com'):
		DescargarLog(data[0]['Hostname'],data[0]['IP'],data[0]['User'],data[0]['Pass'])
		firstExecution = False

	app.debug = True
	app.run(port="5000",host="localhost")