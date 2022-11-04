from conf import db
from flask import Blueprint,render_template,request
import os

page_log = Blueprint('log',__name__,template_folder='templates')


@page_log.route("/showLog")
def showLogFull():
	"""
		Funcion para cargar show_full.html
		Carga los logs sin ningun tipo de filtro
	"""
	data = db.getServidores()
	hostname = str(data[0]['hostname'].split(".")[0])

	contenido = os.listdir("Logs/"+hostname+"/")
	file = open("Logs/"+hostname+"/mail.log")
	aLines = [line.strip() for line in file.readlines()[::-1]]
	return render_template('show_full.html',data=data,log=aLines,file_list=contenido)



@page_log.route("/getLog",methods=['POST'])	
def getLog():
	"""
	Funcion que retorna la lista de logs existentes de un hostname
    que fue descargado 

	Returns:
		data : contiene la lista de logs de ese host 
	"""
	data = db.getServidores()
	r = request.form
	pos =int(r['id'])
	pos_file = int(r['log'])
	hostname =data[pos]['hostname'].split(".")[0]
	contenido = os.listdir("Logs/"+hostname+"/")
	
	file = open("Logs/"+hostname+"/"+contenido[pos_file])
	aLines = [line.strip() for line in file.readlines()[::-1]]	

	return {'status':'ok','data':aLines}
