import os
import cryptocode

str_encoded = cryptocode.encrypt("I am okay","key")
## And then to decode it:
#str_decoded = cryptocode.decrypt(str_encoded, "wow")
print(str_encoded)
#cad = "Sep  5 21:01:26 mailercyber2 postfix/smtp[56923]: D81D6641510: to=<test-0c9pct64s@srv1.mail-tester.com>, relay=reception.mail-tester.com[94.23.206.89]:25, delay=0.7, delays=0.12/0.02/0.28/0.28, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 6A017A9B16)"

	
#file = open("Logs/pruebasdeconceptos/mail.log")

#aLines = [line.strip() for line in file.readlines()[::-1]]

#contenido = os.listdir("Logs/pruebasdeconceptos/")

#print(contenido[0])