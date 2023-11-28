from flask import Blueprint,Flask
from datetime import datetime

### Import routes
from route_index  import page_home
from route_view   import page_view
# from route_mailer import page_mailer
from route_log    import page_log
from route_logBox import page_inbox

app = Flask(__name__)

##Rutas
app.register_blueprint(page_home) # Pagina principal
app.register_blueprint(page_view) # view
# app.register_blueprint(page_mailer) # Mailer
app.register_blueprint(page_log) # Full log
app.register_blueprint(page_inbox) # Ver spam / Virus

#------------------------
### Funcion principal.-
#------------------------
if  __name__ =="__main__":	
	app.debug = True
	app.run(port="5000",host="0.0.0.0")

# root@149.50.133.152 ; UW3kpZhs8uvu
