import os,paramiko,re,dateparser,pytz,json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from scp import SCPClient




def DescargarLog(hostname,ip,user,passwd):
	files = []
	ssh = paramiko.SSHClient()
	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	ssh.connect(ip,username=user,password=passwd)
	stdin, stdout, stderr = ssh.exec_command(' ls /var/log/')	


	for line in iter(stdout.readline,""):
		if(line.find("mail.log") > -1 and line.find(".gz") == -1):
			files.append(line)

	if(len(hostname.split(".")) > 1):
		hostname = hostname.split(".")[0]
	

	#-------------------------------
	# Crea la carpeta.-
	# ------------------------------
	try:
		os.mkdir("Logs/"+hostname)
	except OSError as e:
		pass



	with SCPClient(ssh.get_transport()) as scp:
		for name in files :
			dir_file = "Logs/"+hostname+"/"+name.strip()
			scp.get("/var/log/"+name.strip(),dir_file)
	ssh.close()


def ProcesarLog(hostname,log):
	data = []
	hostname = hostname.split(".")[0]

	find_to = re.compile(r'.*to=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
	find_from = re.compile(r'.*from=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
	find_message_id = re.compile(r'.*message-id=<(.*)>')
	find_status = re.compile(r'.*status=([a-zA-Z0-9-_.]+) (.*)?')
	find_relay = re.compile(r'.*relay=([a-zA-Z0-9-._]+)\[(.*)\]:([0-9]+)')
	find_client = re.compile(r'.*client=([a-zA-Z0-9-._]+)\[(.*)\]')
	find_date = re.compile(r'\w[\w.]+\s+\d.\s.\d.\d..\d.')
	
	with open('Logs/'+hostname+"/"+log,"r") as f:

		lines = f.readlines()
		
		for mline in lines:

			status = ""
			if(mline.find("status=") > -1):
				#print(mline)
				lm = {}
				date = find_date.match(mline)
				to = find_to.match(mline)
				status = find_status.match(mline)
				relay = find_relay.match(mline)


				if date != None: 
					date = date.group(0)
					date = str(dateparser.parse(date)) #datetime.strptime(date,"")
					
				if status != None : 
					status = status.group(1)
				else:
					status = "Unknown"

				if to != None:
					to = to.group(1)
				else:
					to = "Unknow"

				if relay != None:
					relay = relay.group(1)
				else:
					relay = "Unknow"

				lm['Date'] = date
				lm['To'] = to
				lm['Status'] = status
				lm['Relay'] = relay
				
				data.append(lm)
	data = data[::-1]
	
	return data

def CountStatus(data):
	'''
		Funcion que se dedica a contar los estados que
		existen dentro de postfix,siendo

		1. Sent
		2. Deferred
		3. Bounced
		

		param:

		data -> siendo el diccionario que arroja 'ProcesarLog' 

	'''	
	status = ['sent','deferred','bounced','Unknown']

	dic = {'sent':0,'deferred':0,'bounced':0,'unknown':0}
	for i in range(len(data)):		
		
		if(data[i]['Status'] == 'sent'):dic['sent'] +=1
		elif (data[i]['Status'] == 'deferred'):dic['deferred'] +=1
		elif(data[i]['Status'] == 'bounced'):dic['bounced'] +=1
		else:dic['unknown'] +=1

	return dic


def TestConection(ip,user,passwd):
	ssh = paramiko.SSHClient()
	
	try:

		ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
		ssh.connect(ip,username=user,password=passwd)

		return {'conexion':'OK'}
	except (paramiko.ssh_exception.BadHostKeyException) as e:
		return {'conexion':e}
	except (paramiko.ssh_exception.AuthenticationException) as e:
		return {'conexion':'Usuario o Clave incorrecto!'}
	except (paramiko.ssh_exception.SSHException) as e:
		cad = user+"@"+ip
		return {'conexion': "Debes iniciar primero en ssh desde tu terminal!!! <br> ejecuta ssh "+ cad}
	except (TimeoutError) as e:
		return {'conexion':'Error en el host o conexion a internet'}

# aJson = ProcesarLog("pruebasdeconceptos.com","mail.log")
# print(aJson)
# with open("data.json","w") as f:
# 	json.dump(aJson,f,indent=4)