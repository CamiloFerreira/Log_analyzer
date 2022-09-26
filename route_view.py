from flask import Blueprint,render_template,request
from tools import *
from datetime import datetime
from conf import *
import json,os

page_view = Blueprint('view',__name__,template_folder='templates')

## Variables globales
dir_hosts = get_hosts()
dir_smtp  = get_smtp()
key       = get_key()

@page_view.route("/showLog")
def showLogFull():
	"""
		Funcion para cargar show_full.html
		Carga los logs sin ningun tipo de filtro
	"""
	with open(dir_hosts,'r') as file:
		data = json.load(file)	


	hostname = str(data[0]['Hostname'].split(".")[0])

	contenido = os.listdir("Logs/"+hostname+"/")
	file = open("Logs/"+hostname+"/mail.log")
	aLines = [line.strip() for line in file.readlines()[::-1]]


	return render_template('show_full.html',data=data,log=aLines,file_list=contenido)

@page_view.route("/selLog",methods=["POST"])
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
	
	with open(dir_hosts,'r') as file:
		data = json.load(file)

	hostname = data[pos]['Hostname']
	if(len(hostname.split(".")) > 1): 
		hostname = hostname.split(".")[0]
	

	contenido = os.listdir("Logs/"+hostname+"/")
	log_data = ProcesarLog(data[pos]['Hostname'],'mail.log')
	count_status = CountStatus(log_data)

	return render_template('view_log.html',dic=log_data,count=count_status,log_list = contenido)#,dic=log_data,data=data,contenido=contenido)