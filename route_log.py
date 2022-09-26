from conf import *
from flask import Blueprint,render_template,request
import json,os

page_log = Blueprint('log',__name__,template_folder='templates')

## Variables globales
dir_hosts = get_hosts()
dir_smtp  = get_smtp()
key       = get_key()

@page_log.route("/getLog",methods=['POST'])	
def getLog():
	"""
	Funcion que retorna la lista de logs existentes de un hostname
    que fue descargado 

	Returns:
		data : contiene la lista de logs de ese host 
	"""
	with open(dir_hosts,'r') as file:
		data = json.load(file)	
	r = request.form
	pos =int(r['id'])
	pos_file = int(r['log'])
	hostname =data[pos]['Hostname'].split(".")[0]
	contenido = os.listdir("Logs/"+hostname+"/")
	
	file = open("Logs/"+hostname+"/"+contenido[pos_file])
	aLines = [line.strip() for line in file.readlines()[::-1]]	

	return {'status':'ok','data':aLines}
