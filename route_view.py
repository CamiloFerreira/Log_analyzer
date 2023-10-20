from flask import Blueprint,render_template,request
from tools import *
from datetime import datetime
from conf import db,key
import cryptocode,os

page_view = Blueprint('view',__name__,template_folder='templates')


@page_view.route("/updateOne",methods=['POST'])
def updateOne():
	r = request.form

	id_host = int(r['id'])
	id_log  = int(r['id_log'])
	descargar = bool(r['descargar'])

	servidores = db.getServidores()
	password = cryptocode.decrypt(servidores[id_host]['clave'], key)	
	
	if(descargar == True):
		DescargarLog(servidores[id_host]['hostname'],servidores[id_host]['ip'],servidores[id_host]['usuario'],password)

		hostname = str(servidores[id_host]['hostname'].split(".")[0])
		contenido = os.listdir("Logs/"+hostname+"/")


		date = datetime.now().strftime("%d %B, %Y %H:%M:%S")
		date = str(dateparser.parse(date))
		db.updateFecha(id_host,date)
		db.deleteEstado(id_host,id_log)
		estados = ProcesarLog(servidores[id_host]['hostname'],contenido[id_log])
		count_status = CountStatus(estados)

		for est in estados:
			est['id_host'] = id_host
			est['id_log']  = id_log

		db.insertarEstados(estados)
	else:
		estados = db.getEstados(id_host,id_log)
		count_status = CountStatus(estados)

	return {'success':'OK','status':200,'estados':estados,'count':count_status}
	  

@page_view.route('/view', methods=['GET'])
def view():
	'''
		Pagina principal que contiene la tabla donde se mostraran los estados
		de los correos enviados
	'''
	
	try :
		pos = int(request.args.get('id'))
	except (ValueError or Exception) as e :
		pos = 0 
	
	hostname = db.getServidores()[pos]['hostname']

	if(db.getEstados(pos) == []):
		estados = ProcesarLog(hostname,'mail.log')
		if(estados[0]['fecha'] != "N/A"):

			for est in estados:
				est['id_host'] = pos
				est['id_log']  = 0
			db.insertarEstados(estados)
	else:
		estados = db.getEstados(pos,0)

	if(len(hostname.split(".")) > 1): 
		hostname = hostname.split(".")[0]
	

	contenido = os.listdir("Logs/"+hostname+"/")
	count_status = CountStatus(estados)

	return render_template('view_log.html',dic=estados,count=count_status,log_list = contenido)

