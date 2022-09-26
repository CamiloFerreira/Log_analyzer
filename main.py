from conf import *
from flask import Blueprint,Flask
from tools import DescargarLog
from datetime import datetime
import json,dateparser,os,cryptocode


### Import routes
from route_index  import page_home
from route_view   import page_view
from route_mailer import page_mailer
from route_log    import page_log

## Variables globales
dir_hosts = get_hosts()
dir_smtp  = get_smtp()
key       = get_key()


app = Flask(__name__)

##Rutas
app.register_blueprint(page_home) # Home
app.register_blueprint(page_view) # view
app.register_blueprint(page_mailer) # Mailer
app.register_blueprint(page_log) # Full log


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
	if(os.path.exists(dir_hosts) == False):
		data = [{'Hostname':'example.com','IP':'example','User':'example','Pass':'12345',"Update":date}]
		with open(dir_hosts,'w') as file:
			json.dump(data,file,indent=4)

	with open(dir_hosts,'r') as file:
		data = json.load(file)
	if(data[0]['Hostname'] != 'example.com'):
		password = cryptocode.decrypt(data[0]['Pass'], key)
		DescargarLog(data[0]['Hostname'],data[0]['IP'],data[0]['User'],password)
		firstExecution = False

	app.debug = True
	app.run(port="5000",host="localhost")