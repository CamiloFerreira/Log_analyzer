import os,paramiko,re,dateparser
import smtplib,socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scp import SCPClient
import pandas as pd
import dns.resolver
import json



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
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
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
    find_time  = re.compile(r'.*' + hostname + ' ')
    #find_date = re.compile(r'\w[\w.]+\s+\d.\s.\d.\d..\d.')
    
    with open('Logs/'+hostname+"/"+log,"r") as f:

        lines = f.readlines()
        frm_text = ""
        for mline in lines:
            lm = {}

            ##Busca de donde salen
            if(mline.find("postfix/qmgr") > -1):
                frm = find_from.match(mline)
                #Obtiene de donde fueron enviados los correos
                if (frm != None):
                    frm_text = frm.group(1)
                    #print(frm.group(1))

            status = ""
            if(mline.find("status=") > -1):

                to = find_to.match(mline)
                status = find_status.match(mline)
                relay = find_relay.match(mline)
                date = str(dateparser.parse(mline.split(hostname)[0].strip()))
                if status != None : 
                    status = status.group(1)
                else:
                    status = "unknown"


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
                    to = "Unknown"

                if relay != None:
                    relay = relay.group(1)
                else:
                    relay = "Unknown"
                

                if(to != "Unknown" or relay != "Unknown" or status != "unknown"):
                    lm['fecha'] = date
                    lm['para'] = to
                    lm['de'] = frm_text
                    lm['estado'] = status
                    lm['relay'] = relay
                
                    data.append(lm)
    if( len(data) == 0 ):
        data = [{'fecha':'N/A','de':'N/A','para':'N/A','estado':'N/A','relay':'N/A'}]
    
    data = data[::-1]

    return data



def SpamCheck(hostname,Log="mail.log"):
    '''
        Funcion que realiza el analisis a los correos recibidos
        por el dominio seleccionado, analiza los correos spam y 
        correos que fueron rechazados
    '''

    #Expresiones regulares necesarias
    data = []
    host_full = hostname
    hostname = hostname.split(".")[0]
    find_to = re.compile(r'.*to=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
    find_from = re.compile(r'.*from=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
    find_rcpt = re.compile(r'RCPT .*]:')
    find_error  = re.compile(r'\>:.*;')
    find_time  = re.compile(r'.*' + hostname + ' ')
    find_result = re.compile(r'result: .* -')
    find_user = re.compile(r'user=.*,u')
    find_mid = re.compile(r'mid=<.*>')


    spamd = "";user="";frm_text=""
    isSpam = False
    with open("Logs/"+hostname+"/"+Log,"r") as f:
        line = f.readlines()
        
        for mline in line:
            lm   = {}
            tim = find_time.findall(mline)
            
            if(len(tim) > 0 ) : 
                tim = str(tim[0]).split(hostname)[0].strip()
                date = str(dateparser.parse(tim))

            ### Informa los correos rechazados ####
            if ( mline.find("reject") > -1):
                to  = find_to.findall(mline)
                err = find_error.findall(mline)
                frm = find_from.findall(mline)
                rcpt = find_rcpt.findall(mline)

                if(len(frm) == 0):frm = "None";
                else:frm = frm[0]
                
                if(len(err) == 0): err = "None"
                else: err = err[0]

                if(len(to) == 0): to  = "None" 
                else: to  = to[0]

                if(len(rcpt) == 0): rcpt = "None"
                else: rcpt = rcpt[0]

                #print(to[1],frm[1])
                
                err = err[2:len(err)].strip()
                
                lm['fecha'] = date
                lm['para'] = user+"@"+host_full
                lm['de'] = frm_text
                lm['puntaje'] = "N/A"
                lm['estado'] = err
                lm['detalles'] = rcpt ## Quede aqui
                data.append(lm)


            if(isSpam):
                frm = find_from.findall(mline)
                if (len(frm) == 0):
                    frm = ['']
                last = len(data)-1

                data[last]['de'] = frm[0]
                isSpam = False


            #print(mline)
            #### Parte que informa alertas spam #####
            if(len(find_result.findall(mline)) > 0):



                spamd = find_result.findall(mline)[0].replace("result:","score spam:").split(":")[1].strip()
                user  = find_user.findall(mline)[0][:-2].split("user=")[1]


            if( len(spamd) > 0  ):
                #print(mline)
                frm = find_from.findall(mline)

                lm['fecha'] = date
                lm['para'] = user+"@"+host_full
                
                
                if(spamd[0] == "."):
                    
                    if (spamd[1:len(spamd)-1].strip().find("-") > -1):
                        spamd = -float("0."+spamd[1:len(spamd)-1].strip().replace("-",""))
                    else:
                        spamd = float("0."+spamd[1:len(spamd)-1].strip())
                else:
                    spamd = float(spamd[1:len(spamd)-1].strip())

                lm['de'] = "N/A"
                lm['puntaje'] = spamd
               
                lm['estado'] = "received"   
                

                if(spamd >= 5.0):
                    lm['detalle'] = "SPAM"
                else:
                    lm['detalle'] = "PASS"
                
                data.append(lm)
                spamd = ""
                user  = ""
                isSpam = True

        return data[::-1]


def AlertasVirus(hostname,Log="mail.log"):
    '''
        Funcion que realiza el analisis a los correos recibidos
        por el dominio seleccionado ( Tener en cuenta que se debe tener
        instalado CLAIMV y spamassesin)


    '''

    #Expresiones regulares necesarias
    data = []
    host_full = hostname
    hostname = hostname.split(".")[0]


    find_time  = re.compile(r'.*' + hostname + ' ')
    find_to = re.compile(r'.*to=<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
    find_correo = re.compile(r'<([a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+)>')
    spamd = ""
    user=""

    getFrom = False
    anterior = "AAA"
    with open("Logs/"+hostname+"/"+Log,"r") as f:
        line = f.readlines()
        
        for mline in line:
            lm   = {}

            tim = find_time.findall(mline)
            if(mline.find("INFECTED") > -1 and mline.find("amavis")):
                
                if(len(tim) > 0 ) : 
                    tim = str(tim[0]).split(hostname)[0].strip()
                    date = str(dateparser.parse(tim))
                lm['fecha'] = date
                correo = find_correo.findall(mline)

                if (len(correo) > 1):
                    lm['de'] = correo[0]
                    lm['para']   = correo[1]
                    lm['estado'] = 'Infected'
                    lm['ip'] = mline.split(",")[2].split(":")[0].strip()
                    lm['quarentine']=mline.split(",")[3].split(":")[1].strip()
                    lm['tamaño'] = mline.split(",")[8].split(":")[1].strip()
                    data.append(lm)

    if(len(data) == 0 ):
        data = [{'fecha':"",'para':'','de':'','estado':'','ip':'','quarentine':'','tamaño':''}]
    return data[::-1]


def CountStatus(data) -> dict:
    '''
        Funcion que se dedica a contar los estados que
        existen dentro de postfix

        param:
        data -> siendo el diccionario que arroja 'ProcesarLog' 

    ''' 
    #status = ['sent','deferred','bounced','Unknown'] 
    status = [data[i]['estado'] for i in range(len(data))]
    status = list(set(status))
    dic = {'sent': 0,'deferred':0,'bounced': 0,'rejected': 0,'user unknown': 0,'host unknown': 0 , 'unknown':0 }
    for i in range(len(data)):      
        for col in status:
            if(data[i]['estado'] == col and col != "" and col != "N/A"):
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

        print("Correo enviado")
        return {'success':'OK','status':200} 
    except socket.gaierror:
        return {'success':'ERORR',"msj":"Error en el hostname"} 
    except smtplib.SMTPAuthenticationError:
        return {'success':'ERORR',"msj":"Usuario o clave incorrecto!"}

if __name__ == '__main__':
    #DescargarLog("gomail.cl","179.43.126.3","root","mi29befiBU06gurobi")
    #print(ProcesarLog("gomail.cl","mail.log"))
    for spam in SpamCheck("gomailer.tk"):

        print(spam)
#AlertasVirus("gomailer.tk")
#for data in SpamCheck("gomailer.tk"):
#   print(data)