from pymongo import MongoClient
import datetime

# Change the link if you're using diffrent database
db_address = "mongodb://admin:password@localhost:8080/admin?authSource=admin"

class DB:

	def __init__(self):
		self.client = None
		self.col = None

	def connect(self):
		""" Get connected to database. """
		self.client = MongoClient(db_address)
		if self.client: print('Connected.')

	def select_database(self, db_name):
		""" Select database. """
		self.db = self.client[db_name]
		return self.db

	def comments_col(self):
		""" Select default collection as comments. """
		self.col = self.db.comments
		return self.col

	def items_col(self):
		""" Select default collection as items. """
		self.col = self.db.items
		return self.col

	def insert_one(self, doc):
		""" Insert into selected collection. """
		obj = self.col.insert_one(doc)
		return obj

	def find_one(self, item):
		""" Find in selected collection. """
		return self.col.find_one(item)

	def get_databases(self):
		""" Get list of databases. """
		dbs = self.client.list_database_names()
		return dbs

	def refweb(self, datetime, website):
		""" Update datetime in refweb. """
		db = self.client['REFWebsites']
		col = db.websites
		doc = {'LastUpdateDate': datetime, 'WebLink': website}
		return col.insert_one(doc)

	def save(self, doc):
		return self.col.save(doc)
		
