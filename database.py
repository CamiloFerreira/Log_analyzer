import sqlite3
from dateutil.parser import parse
from datetime import datetime

class Database:

	def __init__(self):
		self.__con = sqlite3.connect("logs.db",check_same_thread=False) 
		self._cur  = self.__con.cursor()
		self._id_host = 0
	def createServidores(self):
		query = '''
			CREATE TABLE IF NOT EXISTS  Servidor( id_host int  not null, 
							       hostname varchar(100) , 
								   ip varchar(100),
								   usuario varchar(100), 
								   clave varchar(100), 
								   fecha_act date, 
								   PRIMARY KEY (id_host));
		'''
		self._cur.execute(query)
	def createEstados(self):
		query = '''
			CREATE TABLE IF NOT EXISTS Estados( id_host int not null,
												id_log int not null,
											    fecha date,
											    para varchar,
											    de varchar,
											    estado varchar, 
											    relay varchar)
		'''
		self._cur.execute(query)
	def createSpam(self):
		query= '''
			CREATE TABLE IF NOT EXISTS Alertas_Spam( id_host int not null,
													 fecha date,
													 para varchar,
													 de varchar,
													 puntaje varchar,
													 estado varchar,
													 detalle varchar
													 )
		'''
		self._cur.execute(query)
	def createVirus(self):
		query= '''
			CREATE TABLE IF NOT EXISTS Alertas_Virus( id_host int not null,
													 fecha date,
													 para varchar,
													 de varchar,
													 estado varchar,
													 ip varchar,
													 quarentine varchar,
													 tamaño varchar
													 )
		'''
		self._cur.execute(query)

	#------------Insert -------------#
	def insertarServidores(self,row):
		query = ''' 
					INSERT INTO Servidor(
									id_host,
					                hostname,
					                ip,
					                usuario,
					                clave,
					                fecha_act) VALUES (?,?,?,?,?,?)
		'''


		t = (self.id_host,row['hostname'],row['ip'],row['usuario'],row['clave'],row['fecha_act'])
		#print(t)
		self._cur.execute(query,t)
		self.__con.commit()
		return self.id_host

	def insertarSpam(self,data):
		query = ''' 
					INSERT INTO Alertas_Spam (
									 id_host,
									 fecha ,
									 para,
									 de,
									 puntaje,
									 estado,
									 detalle) VALUES (?,?,?,?,?,?,?)
		'''

		for row in data:
			t = (row['id_host'],row['fecha'],row['para'],row['de'],row['puntaje'],row['estado'],row['detalle'])
			self._cur.execute(query,t)
		self.__con.commit()

	def insertarEstados(self,data):

		query= '''
			INSERT INTO Estados( id_host,
								 id_log,
								 fecha,
								 para,
								 de,
							     estado, 
						         relay) VALUES (?,?,?,?,?,?,?)
		'''
		for row in data:
			t = (row['id_host'],row['id_log'],row['fecha'],row['para'],row['de'],row['estado'],row['relay'])
			self._cur.execute(query,t)
		self.__con.commit()
		
	def insertarVirus(self,data):
		query = ''' 
					INSERT INTO Alertas_Virus (
									 id_host,
									 fecha ,
									 para,
									 de,
									 estado,
									 ip,
									 quarentine,
									 tamaño) VALUES (?,?,?,?,?,?,?,?)
		'''

		for row in data:
			t = (row['id_host'],row['fecha'],row['para'],row['de'],row['estado'],row['ip'],row['quarentine'],row['tamaño'])
			self._cur.execute(query,t)
		self.__con.commit()	

	#------------ Update --------------#
	def updateFecha(self,id_host,fecha):
		try:
			id_host = int(id_host)
		except :
			id_host = 0 

		try:
			fecha = parse(fecha)
		except:
			fecha = str(datetime.now())
		

		query = f"update Servidor set fecha_act='{fecha}' where id_host ='{id_host}';"
		self._cur.execute(query)
		self.__con.commit()
	#------------ Get ------------------#	
	def getSpam(self,id_host):

		query = f"SELECT * FROM Alertas_Spam where id_host = '{id_host}'"
		data = []
		self._cur.execute(query)

		rows = self._cur.fetchall()


		keys = ['id_host','fecha','para','de','puntaje','estado','detalle']
	
		for row in rows:
			dic = {}
			for i in range(len(row)):
				dic[keys[i]] = row[i]
			data.append(dic)
		return data
	def getServidores(self):

		query = '''
			SELECT * FROM Servidor;
		'''
		data = []
		self._cur.execute(query)

		rows = self._cur.fetchall()


		keys = ['id_host','hostname','ip','usuario','clave','fecha_act']
	
		for row in rows:
			dic = {}
			for i in range(len(row)):
				dic[keys[i]] = row[i]
			data.append(dic)
		return data	
	def getEstados(self,id_host=0,id_log=0):
		try :
			id_host = int(id_host)
			id_log  = int(id_log)
		except:
			id_host = 0
			id_log  = 0

		data = []
		query = f'SELECT * FROM Estados where id_host ="{id_host}" and id_log="{id_log}" ';
		
		self._cur.execute(query)
		rows = self._cur.fetchall()
		keys = ['id_host','id_log','fecha','para','de','estado','relay']
		for row in rows:
			dic ={}
			for i in range(len(row)):
				dic[keys[i]] = row[i]
			data.append(dic)
		return data
	def getVirus(self,id_host):
		query = f"SELECT * FROM Alertas_Virus WHERE id_host='{id_host}' "
		data = []
		self._cur.execute(query)

		rows = self._cur.fetchall()


		keys = ['id_host','fecha','para','de','estado','ip','quarentine','tamaño']
	
		for row in rows:
			dic = {}
			for i in range(len(row)):
				dic[keys[i]] = row[i]
			data.append(dic)
		return data		


	#--------------- Delete --------------#
	def deleteEstado(self,id_host,id_log):
		try:
			id_host = int(id_host)
			query = f"DELETE FROM Estados where id_host='{id_host}' and id_log ='{id_log}'"
			self._cur.execute(query)
			self.__con.commit()
		except:
			pass
	def deleteSpam(self,id_host):
		try:
			id_host = int(id_host)
			query = f"DELETE FROM Alertas_Spam where id_host='{id_host}'"
			self._cur.execute(query)
			self.__con.commit()
		except:
			pass
	def deleteVirus(self,id_host):
		try:
			id_host = int(id_host)
			query = f"DELETE FROM Alertas_Virus where id_host='{id_host}'"
			self._cur.execute(query)
			self.__con.commit()
		except:
			pass
	def deleteServer(self,hostname):
		try:

			query = f"SELECT id_host FROM Servidor where hostname='{hostname}'"
			self._cur.execute(query)

			rows = self._cur.fetchall()		
			if(len(rows) > 0):

				id_host = int(rows[0][0])
				query = f"DELETE FROM Servidor where id_host='{id_host}'"
				self._cur.execute(query)
				self.__con.commit()

				query = f"DELETE FROM Estados where id_host='{id_host}'"
				self._cur.execute(query)
				self.__con.commit()

				query = f"DELETE FROM Alertas_Spam where id_host='{id_host}'"
				self._cur.execute(query)
				self.__con.commit()

				query = f"DELETE FROM Alertas_Virus where id_host='{id_host}'"
				self._cur.execute(query)
				self.__con.commit()

		except:
			pass

	#--------- Getter y Setters ----------#
	@property
	def id_host(self):
		query = '''
			SELECT id_host FROM Servidor order by id_host DESC ;
		'''
		val = 0
		self._cur.execute(query)
		resp = self._cur.fetchone() 
		if (resp == None):
			val = 0
		else:
			val = resp[0]
			val +=1

		return val
	@id_host.setter
	def id_host(self,id):
		self._id = id

if __name__ == '__main__':
	
	db = Database()
	# db.createSpam()
	# db.createVirus()
	# db.createEstados()
	# db.createServidores()
	#db.deleteServer("fhsecurity.cl")

