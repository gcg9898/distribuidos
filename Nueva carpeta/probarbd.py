from pymongo import MongoClient
import hashlib
#mongo ip = 172.31.87.41
#http ip = 172.31.86.59
#codigo suma = 0
#codigo leerfichero = 1
import socket
import sys
servidor = "localhost"
ip = "172.31.87.41"
db = MongoClient(ip,port=27017)
bds = db.list_database_names()
mybd = db["distribuidos"]

ipbd = mybd["ip"]
ipsobj = ipbd.find()
ips = []
for x in ipsobj:
    ips.append(x["_id"])
    print(x["_id"])