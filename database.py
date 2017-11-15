import psycopg2

class _Db(object):
	"""docstring for Db"""
	def __init__(self, connexion_string):
		super(_Db, self).__init__()
		self.connexion = psycopg2.connect(connexion_string)
		#check if connexion succeeds
		self.cursor = None#self.connexion.cursor()

	def select(self, sql_string, args = None, quantity = "one"):
		self.cursor = self.connexion.cursor()
		self.cursor.execute(sql_string, args)
		result = 0
		if (quantity == "one"):
			result = self.cursor.fetchone()
		else:
			result = self.cursor.fetchall()
		self.cursor.close()
		return (result)

	def insert(self, sql_string, args = None):
		self.cursor = self.connexion.cursor()
		self.cursor.execute(sql_string, args)
		result = self.cursor.rowcount
		self.connexion.commit()
		self.cursor.close()
		return (result)

	def update(self, sql_string, args = None):
		self.cursor = self.connexion.cursor()
		self.cursor.execute(sql_string, args)
		result = self.cursor.rowcount
		self.connexion.commit()
		self.cursor.close()
		return (result)

	def close(self):
		self.connexion.close()
		return (None)

DB = None

def NewConn(connexion_string):
	global DB
	print("NEWCONN")
	DB = _Db(connexion_string)
	#DB = "new connexion"
	print(DB)

"""def test():
	global DB
	print("TEST:", DB)"""