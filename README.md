## Analizador de logs POSTFIX


\
Este es un proyecto creado para analizar logs del servidor de correo basado en postfix, teniendo como principal finalidad poder analizar los estados que presenta este servidor , teniendo como posibles estados :

 1. Sent
 2. Delivered
 3. Bounced
 4. Unknown
 
Estos estados siendo generados por postfix al momento de enviar un correo, teniendo como principal objetivo estos estados presentar si dicho correo fue entregado , rebotado y/o deliberado. 

## Herramientas que utiliza esta aplicación 

Como principales herramientas utilizadas en el desarrollo de esta aplicación se tuvo como principal lenguaje y/o Framework, el uso de flask con python, siendo esta la que permite generar un servidor web y diversas opciones que facilitan la creación de esta pagina web , añadiendo funcionalidades de reutilización de templates html , inserción de código python dentro de html y entre otras funcionalidades que permiten de manera sencilla realizar tareas que con otras herramientas seria mas "extenso".

En cuanto a librerias utilizadas en python existen varias que fueron vital para poder realizar la primera parte de funcionalidades de esta pagina web, ya que dentro de esta pagina se plantea el uso de "SSH" para realizar la descarga de los logs de postfix, con dicha co