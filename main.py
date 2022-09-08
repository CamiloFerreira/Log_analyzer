from flask import Flask,render_template,request,redirect
from datetime import datetime
from tools import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json,os,dateparser
import smtplib,ssl
import cryptocode

#------------------------
### Variables globales.-
#------------------------
app = Flask(__name__)
key = "key_1"

#------------------------
### Apartado showLog
#------------------------
@app.route("/showLog")
def showLogFull():
	"""
		Funcion para cargar show_full.html
		Carga los logs sin ningun tipo de filtro
	"""
	with open('hosts.json','r') as file:
		data = json.load(file)	


	hostname = str(data[0]['Hostname'].split(".")[0])

	contenido = os.listdir("Logs/"+hostname+"/")
	file = open("Logs/"+hostname+"/mail.log")
	aLines = [line.strip() for line in file.readlines()[::-1]]


	return render_template('show_full.html',data=data,log=aLines,file_list=contenido)

@app.route("/selLog",methods=["POST"])
def selLog():
    '''
		Funcion que retorna el log seleccionado,
		Esta funcion siendo llamada en el onchange de "sel_log"
  
		log_id -> posicion del log a seleccionar
		id -> posicion del hostname a seleccionar
    
    '''
    r = request.form
    try:
        log_id = int(r['log_id'])
        pos  = int(r['id'])
        hostname = data[pos]['Hostname']
        if(len(hostname.split(".")) > 1): 
            hostname = hostname.split(".")[0]
        
        contenido = os.listdir("Logs/"+hostname+"/")
        log_data = ProcesarLog(data[pos]['Hostname'],contenido[log_id])
        count_status = CountStatus(log_data)        
        
        return {'success':'OK','status':200,'count':count_status,'data':log_data} 
    except (ValueError or Exception) as e :
        return {'success':'Error','status':400,'data':'NULL'} 
    
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

	return render_template('view_log.html',dic=log_data,count=count_status,log_list = contenido)#,dic=log_data,data=data,contenido=contenido)
#--------------------------
### Apartado ver logs
#---------------------------
@app.route("/getLog",methods=['POST'])	
def getLog():
	"""
	Funcion que retorna la lista de logs existentes de un hostname
    que fue descargado 

	Returns:
		data : contiene la lista de logs de ese host 
	"""
	with open('hosts.json','r') as file:
		data = json.load(file)	
	r = request.form
	pos =int(r['id'])
	pos_file = int(r['log'])
	hostname =data[pos]['Hostname'].split(".")[0]
	contenido = os.listdir("Logs/"+hostname+"/")
	
	file = open("Logs/"+hostname+"/"+contenido[pos_file])
	aLines = [line.strip() for line in file.readlines()[::-1]]	

	return {'status':'ok','data':aLines}


#-----------------------------
### Apartado de index
#------------------------------
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

@app.route('/checkConnection',methods=['POST'])
def checkConnection():
	'''
		Comprueba si es posible conectar
		arrojando los posibles errores
	'''
	r = request.form
	t = TestConection(r['ip'],r['user'],r['password'])
	return {'status':'OK','respuesta':t}

## Tambien se utiliza en apartado ver logs
@app.route('/updateLog',methods=['POST'])
def updateLog():
	"""
		Descarga y actualiza los logs, esta funcion
		puede ser llamada desde el index o en el view_log
  
		para el caso del index
	
		id[] -> obtendra un lista por post, lista de los indices para descargar los logs
  
		para el caso de view_log
  
		id -> obtendra un int , para descargar solamente los logs de un "Hostname"
	
 	"""
	with open('hosts.json','r') as file:
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

		with open('hosts.json','w') as file:
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

			with open('hosts.json','w') as file:
				json.dump(data,file,indent=4)
			return {'success':'OK','status':200,'count':count_status,'data':log_data} 
		except (ValueError or Exception) as e :
			return {'success':'Error','status':400,'data':'NULL'} 
	###

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

	password = cryptocode.encrypt(r['password'],key) 
	

	if(data[0]['Hostname'] == "example.com"):
		data = [{'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':password,"Update":date}]
	else:
		data.append({'Hostname':r['hostname'],'IP':r['ip'],'User':r['user'],'Pass':password,"Update":date})

	with open('hosts.json','w') as file:
		json.dump(data,file,indent=4)
	return redirect("/")

#--------------------------------
#### Apartado de mailer 
#---------------------------------

@app.route("/mailer")
def mailer():
	return render_template('mailer.html')

@app.route("/addSMTP",methods=['POST'])
def addSMTP():

	return {'status':'ok','data':""}

@app.route("/sendMail",methods=["POST"])
def sendMail():

	r = request.form  

	server = smtplib.SMTP(host="smtp.mailercyber2.com",port=587)
	server.ehlo()
	server.starttls()
	server.login("contacto@mailercyber2.com","Cyber4775.")  
    
	msg = MIMEMultipart('alternative')
	msg['Subject'] = r['subject']
	msg['From'] = r['from']
	part1 = MIMEText(r['content'],'html')
	msg.attach(part1)
	msg['To'] = r['to']
	server.sendmail(msg['From'],r['to'],msg.as_string())



	return {'success':'OK','status':200,'data':r} 


#------------------------
### Funcion principal.-
#------------------------
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
		password = cryptocode.decrypt(data[0]['Pass'], key)
		DescargarLog(data[0]['Hostname'],data[0]['IP'],data[0]['User'],password)
		firstExecution = False

	app.debug = True
	app.run(port="5000",host="localhost")