import os


file = open("Logs/pruebasdeconceptos/mail.log")

aLines = [line.strip() for line in file.readlines()[::-1]]

contenido = os.listdir("Logs/pruebasdeconceptos/")

print(contenido[0])