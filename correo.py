import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tqdm import tqdm


html = '''
	<html >
		<head>
			
		</head>
		
		<body>
			<h1> Saludos a todos! </h1>
			<p> Esto es una prueba para ver como se recepciona el correo al momento de enviar desde distintos correos , espero que te llegue bien </p>
			<a href="www.google.com"> Has click aqui </a>
		</body>
	
	</html>
'''




aCorreos = ['camilo_ferre25@hotmail.com']

server = smtplib.SMTP(host="smtp.mailer-cf.com",port=587)
server.ehlo()
server.starttls()
server.login("lferreira@mailer-cf.tk","Camilo500@")  


for i in tqdm(range(1)):
	
	y = 0#random.randint(0,len(aCorreos)-1)
	
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Prueba n°  %d " % i
	msg['From'] = "Luis Ferreira <lferreira@mailer-cf.tk>"
	part1 = MIMEText(html,'html')
	msg.attach(part1)
	msg['To'] = aCorreos[0]
	#print(msg['To'])
	server.sendmail(msg['From'],aCorreos[y],msg.as_string())
server.quit()
