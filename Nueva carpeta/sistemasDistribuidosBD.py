from pymongo import MongoClient
import json
import hashlib
db = MongoClient('localhost',port=27017)
bds = db.list_database_names()
mybd = db["distribuidos"]
trabajadores = mybd["usuarios"]
name = "Graciano Carmona Grarcia"
user= "gcg9898"
con = "1234"
con = hashlib.sha1(con.encode("utf-8")).hexdigest()
if(trabajadores.find() == 0):
    trabajadores.insert_one({'user': user, 'name':name , "pas":con})
else:
    trabajadores.update_one({'user' : user}, {"$set":{'user': user, 'name':name , "pas":con}},upsert = True)
