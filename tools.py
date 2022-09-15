import os,paramiko,re,dateparser
import smtplib,socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scp import SCPClient

def DescargarLog(hostname,ip,user,passwd) -> None:
	'''
		Descarga los logs que se encuentran en /var/log/mail.log,
		guardando en una carpeta llamada igual que el hostname

		param:
			hostname : dominio del servidor
			ip : IP del servidor
			user : usuario de ssh
			passwd : clave ssh


	'''
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


def ProcesarLog(hostname,log="mail.log"):
	'''
		Funcion que procesa el log obtenidos,
		obteniendo los datos principales para ser retornado
		como diccionario

		param:
			hostname : Nombre del dominio
			log : Log a utilizar ( default 'mail.log')
	'''


	data = []
	hostname = hostname.split(".")[0]
	find_to = re.compile(r'.*to=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
	find_from = re.compile(r'.*from=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
	find_message_id = re.compile(r'.*message-id=<(.*)>')
	find_status = re.compile(r'.*status=([a-zA-Z0-9-_.]+) (.*)?')
	find_relay = re.compile(r'.*relay=([a-zA-Z0-9-._]+)\[(.*)\]:([0-9]+)')
	find_client = re.compile(r'.*client=([a-zA-Z0-9-._]+)\[(.*)\]')
	#find_date = re.compile(r'\w[\w.]+\s+\d.\s.\d.\d..\d.')
	
	with open('Logs/'+hostname+"/"+log,"r") as f:

		lines = f.readlines()
		
		for mline in lines:

			status = ""
			if(mline.find("status=") > -1):
				#print(mline)
				lm = {}
				
				to = find_to.match(mline)
				status = find_status.match(mline)
				relay = find_relay.match(mline)
				date = str(dateparser.parse(mline.split(hostname)[0].strip()))
				if status != None : 
					status = status.group(1)
				else:
					status = "Unknown"


				### Cuando el status sea rebotado

				if ( status == "bounced"):
					err_code = mline.split("status=bounced")[1]

					if(err_code.find("Host or domain name not found") > -1):
						status = "host unknown"
					## Error de usuario
					if(err_code.find("User doesn't exist") > -1 or err_code.find("Requested action not taken: mailbox unavailable") > -1):
						status = "user unknown"
					## Erro de rejectado 
					if(err_code.find("Recipient address rejected") > -1):
						status = "rejected"

					## Error del tipo remitente no existe

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

def CountStatus(data) -> dict:
	'''
		Funcion que se dedica a contar los estados que
		existen dentro de postfix

		param:
		data -> siendo el diccionario que arroja 'ProcesarLog' 

	'''	
	#status = ['sent','deferred','bounced','Unknown'] 
	status = [data[i]['Status'] for i in range(len(data))]
	status = list(set(status))
	
	dic = {'user unknown': 0, 'rejected': 0, 'bounced': 0, 'host unknown': 0, 'sent': 0}
		
	for i in range(len(data)):		
		for col in status:
			if(data[i]['Status'] == col):
				dic[col] +=1
		
	return dic


def TestConection(ip,user,passwd) -> dict:

	'''
		Comprueba la conexion via ssh
		arrojando un diccionario con estados

		param:
			ip : ip del servidor
			user : usuario para iniciar en ssh
			passwd: clave para iniciar en ssh


	'''
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



def SendMail(host,user,passwd,from_,to,subject,content):

	try :
		server = smtplib.SMTP(host=host,port=587)
		server.ehlo()
		server.starttls()
		server.login(user,passwd)  
    
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = from_
	
		part1 = MIMEText(content,'html')
		msg.attach(part1)
		msg['To'] = to
		server.sendmail(msg['From'],msg['to'],msg.as_string())

		return {'success':'OK','status':200} 
	except socket.gaierror:
		return {'success':'ERORR',"msj":"Error en el hostname"} 
	except smtplib.SMTPAuthenticationError:
		return {'success':'ERORR',"msj":"Usuario o clave incorrecto!"}
