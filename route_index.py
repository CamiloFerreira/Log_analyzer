from flask import Blueprint,render_template,request,redirect
from conf import db,key
from tools import *
from datetime import datetime
from os import path 
import cryptocode

page_home = Blueprint('home',__name__,template_folder='templates')



@page_home.route("/")
def home():
	firstExecution = True 
	data = [{'id_host': 0,'hostname':'example','ip':'none','usuario':'none','clave':'none','fecha_act':'none'}]
	count = 0

	#Comprueba si es la primera ejecucion del programa
	db.createServidores()
	db.createEstados()
	db.createSpam()
	db.createVirus()

	if(db.getServidores() != []):
		firstExecution = False
		count = len(db.getServidores())
		data = db.getServidores()

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
  	
 	"""
	r = request.form
	data = db.getServidores()
	if(len(r.getlist('id[]')) >= 1):
		##Actualiza para todos
		for val in r.getlist('id[]'):
			val = int(val)
			password = cryptocode.decrypt(data[val]['clave'], key)
			DescargarLog(data[val]['hostname'],data[val]['ip'],data[val]['usuario'],password)
			date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
			date = str(dateparser.parse(date))
			db.updateFecha(val,date)		
		
		return {'success':'OK','status':200} 
	###

@page_home.route("/addDomain",methods=['POST'])
def addDomain():
	'''
		Agrega los nuevos dominios de smtp 
		al json 

	'''
	r = request.form

	date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
	date = str(dateparser.parse(date))
	password = cryptocode.encrypt(r['password'],key) 

	row = {'hostname':r['hostname'],'ip':r['ip'],'usuario':r['user'],'clave':password,"fecha_act":date}
	id_host = db.insertarServidores(row)
	
	DescargarLog(r['hostname'],r['ip'],r['user'],r['password'])

	hostname = str(r['hostname'].split(".")[0])
	contenido = os.listdir("Logs/"+hostname+"/")
	estados = ProcesarLog(r['hostname'])

	date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
	date = str(dateparser.parse(date))
	db.updateFecha(id_host,date)
	db.deleteEstado(id_host,0)

	for est in estados:
		est['id_host'] = id_host
		est['id_log']  = 0

	db.insertarEstados(estados)


	return redirect("/")
