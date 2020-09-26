#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import os
from pymongo import MongoClient
from time import time
import hashlib
from libreriagra import enviarNumero, recibirNumero, enviarTexto, recibirTexto
mongo_ip = "172.31.87.41"
http_ip = "172.31.86.59"
client_ip = "localhost"
#¢odigo suma = 2
#codigo leerfichero = 3 

ip = "localhost"
db = MongoClient(mongo_ip,port=27017)
mybd = db["distribuidos"]
ips = mybd["ip"]
ips.delete_many({})
ips.insert_one({'_id': '172.31.87.41', 'suma': 1, 'leerfichero': 1})
ips.insert_one({'_id': '172.31.81.77', 'suma': 1, 'leerfichero':1})

def comprobarSuma(db,ip):
    if( db.find_one({'_id': ip})['suma'] == 0):
        return False
    return True
def comprobarLeerFichero(db,ip):
    if( db.find_one({'_id': ip})['leerfichero'] == 0):
        return False
    return True
def enviarFichero(connection,nom):
    f = open(nom,'r')
    texto = f.read()
    tam = len(texto)
    enviarTexto(connection,texto)
    
    

def suma(num1,num2,connection,client_address):
    #enviar codigo suma
    enviarNumero(connection,2)
    if(comprobarSuma(ips,client_address)== False):
        ips.update_one({'_id': client_address}, {"$set":{ 'suma': 1}},True)
        enviarFichero(connection,"suma.py")
    #enviar num1 y num2
    enviarNumero(connection, num1)
    enviarNumero(connection, num2)
    #recibir resultado
    a = recibirNumero(connection)
    return a
def readFile(nombrefichero,connection,client_address):
    #enviar codigo leerfichero
    enviarNumero(connection,3)
    if(comprobarLeerFichero(ips,client_address)== False):
        ips.update_one({'_id': client_address},{ "$set":{'leerfichero': 1}},True) 
        enviarFichero(connection,"leerfichero.py")
    #enviar nombre fichero
    enviarTexto(connection,nombrefichero)
    #recibo texto del fichero
    lectura = recibirTexto(connection)   
    return lectura

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(3)
addr = []
try:
    # Wait for a connection
    print('waiting for a connection')
    #connection https
    connection1, client_address1 = sock.accept()
    print('connection from', client_address1)
    #connection cliente 1
    connection2, client_address2 = sock.accept()
    print('connection from', client_address2)
    ipcliente2 = client_address2[0]
    addr.append(ipcliente2)
    #connection cliente 2
    connection3, client_address3 = sock.accept()
    ipcliente3 = client_address3[0]
    print('connection from', client_address3)
    addr.append(ipcliente3)
    while True:
        data = recibirNumero(connection1)
        if(data == 0 ):
            num1 = recibirNumero(connection1)
            num2 = recibirNumero(connection1)
            resultado = suma(num1,num2,connection2,ipcliente2)          
            enviarNumero(connection1, resultado)
        elif(data== 1):  
            texto= readFile("texto.txt",connection2,ipcliente2)
            enviarTexto(connection1,texto)
        elif(data== 2):
            num1 = recibirNumero(connection1)
            num2 = recibirNumero(connection1)
            resultado = suma(num1,num2,connection3,ipcliente3)
            enviarNumero(connection1, resultado)
        elif(data== 3):  
            texto= readFile("texto.txt",connection3,ipcliente3)
            enviarTexto(connection1,texto)
        elif(data == 5):
            texto = recibirTexto(connection1)
            leido = readFile(texto,connection2,ipcliente2)
            enviarTexto(connection1,leido)
        elif(data == 6):
            texto = recibirTexto(connection1)
            leido = readFile(texto,connection3,ipcliente3)
            enviarTexto(connection1,leido)
        elif(data == 9):
            enviarNumero(connection2,9)
            tam1 = recibirNumero(connection2)
            enviarNumero(connection1,tam1)
            for i in range(tam1):
                text = recibirTexto(connection2)
                enviarTexto(connection1,text)
            enviarNumero(connection3,9)
            tam2 = recibirNumero(connection3)
            enviarNumero(connection1,tam2)
            for i in range(tam2):
                text = recibirTexto(connection3)
                enviarTexto(connection1,text)
        elif(data == 11):
            titulo = recibirTexto(connection1)
            contenido = recibirTexto(connection1)
            enviarNumero(connection2,6)
            enviarTexto(connection2,titulo)
            enviarTexto(connection2,contenido)
        elif(data == 12):
            titulo = recibirTexto(connection1)
            contenido = recibirTexto(connection1)
            enviarNumero(connection3,6)
            enviarTexto(connection3,titulo)
            enviarTexto(connection3,contenido)
finally:
    print('closing socket')
    sock.close()