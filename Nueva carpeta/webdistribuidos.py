#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,send_from_directory
from pymongo import MongoClient
import hashlib
from libreriagra import enviarNumero, recibirNumero, enviarTexto, recibirTexto
#mongo ip = 172.31.87.41
#http ip = 172.31.86.59
#codigo suma = 0
#codigo leerfichero = 1
import socket
import sys
import sys
import os
servidor = "localhost"
ip = "172.31.87.41"
db = MongoClient(ip,port=27017)
bds = db.list_database_names()
mybd = db["distribuidos"]
trabajadores = mybd["usuarios"]
def crearUsuario(nombre,contrasenia):
    trabajadores.insert_one({'user':nombre, 'pas':contrasenia})
def crearFichero(titulo, contenido):
    f =  open(titulo, 'w') 
    print( 'file opened')
    f.write(contenido)
app = Flask(__name__,template_folder='templates')
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = (servidor, 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/load", methods=['GET', 'POST'])
def usuario():
    if (request.method == 'POST'):
        print("jaj")
        data = request.form
        usuario = data["uname"]
        pws = hashlib.sha1(data["psw"].encode("utf-8")).hexdigest()
        cursor =trabajadores.find_one({'user':usuario})
    if(trabajadores.find_one({'user':usuario})):
        if(trabajadores.find_one({'user':usuario})["pas"] == pws):
            return render_template("menu.html")
    return render_template("createuser.html")
@app.route("/createUser", methods=[ 'POST'])
def crearU():
     if (request.method == 'POST'):
        print("jaj")
        data = request.form
        usuario = data["uname"]
        pws = hashlib.sha1(data["psw"].encode("utf-8")).hexdigest()
        crearUsuario(usuario,pws)
        return render_template("index.html")
@app.route("/inicio", methods=[ 'POST'])
def ir():
    if(request.method == 'POST'):
        data = request.form
        ipbd = mybd["ip"]
        ipsobj = ipbd.find()
        ips = []
        for x in ipsobj:
            ips.append(x["_id"])
            print(x["_id"])
        if(data.get("direcciones")):
            enviarNumero(sock,9)
            tam1 = recibirNumero(sock)
            
            dir1 = []
            dir2 = []
            for i in range(tam1):
                texto = recibirTexto(sock)
                dir1.append(texto)
            tam2 = recibirNumero(sock)
            for i in range(tam2):
                texto = recibirTexto(sock)
                dir2.append(texto)
            dicciona = {}
            dicciona["ips"] = ips
            dicciona["dir1"] = dir1 
            dicciona["dir2"] = dir2 
            return render_template("dir.html" , dicciona = dicciona)
        else:
            return render_template("services.html" , ips = ips)
@app.route("/crear", methods=[ 'POST'])
def crear():
    if (request.method == 'POST'):
        data = request.form 
        ip1 = data.get("ip1")
        ip2 = data.get("ip2")
        titulo = data["titulo"]
        contenido = data["contenido"]
        if(ip1):
            enviarNumero(sock,11)
            enviarTexto(sock,titulo)
            enviarTexto(sock,contenido)
        if(ip2):
            enviarNumero(sock,12)
            enviarTexto(sock,titulo)
            enviarTexto(sock,contenido)
        return("creado")
@app.route("/leer", methods=[ 'POST'])
def leerindicado():
    if (request.method == 'POST'):
        leido = {}
        data = request.form 
        indicado1 = data.getlist("listip1")
        indicado2 = data.getlist("listip2")
        for i in indicado1:
            enviarNumero(sock,5)
            enviarTexto(sock,i)
            a = recibirTexto(sock)
            leido[i + "1"] = a
        for i in indicado2:
            enviarNumero(sock,6)
            enviarTexto(sock,i)
            a = recibirTexto(sock)
            leido[i + "2"] = a
        return(str(leido))
@app.route("/descargar", methods=[ 'POST'])
def dascargar():
    if(request.method == 'POST'):      
        data = request.form 
        indicado1 = data.get("listip1")
        indicado2 = data.get("listip2")
        if(indicado1):
            enviarNumero(sock,5)
            enviarTexto(sock,indicado1)
            a = recibirTexto(sock)
            leido = a
            crearFichero(indicado1,leido)
            return send_from_directory(directory="./", filename=indicado1)
        elif(indicado2):
            enviarNumero(sock,6)
            enviarTexto(sock,indicado2)
            a = recibirTexto(sock)
            leido= a
            crearFichero(indicado2,leido)
            return send_from_directory(directory="./", filename=indicado2)
@app.route("/services", methods=[ 'POST'])
def analizar():
    if (request.method == 'POST'):
        ipbd = mybd["ip"]
        ipsobj = ipbd.find()
        ips = []
        for x in ipsobj:
            ips.append(x["_id"])
            print(x["_id"])
        data2 = request.form 
        print(data2)
        num1 = data2["num1"]
        num2 = data2["num2"]
        suma1 = data2.get(ips[0]+"pruebaclase")
        buclesuma1 = data2[ips[0]+"pruebaclase"+"1"]
        leerfichero1 = data2.get(ips[0]+"remotefile")
        buclesleerfichero1 = data2[ips[0]+"remotefile"+"2"]
        suma2 = data2.get(ips[1]+"pruebaclase")
        buclesuma2 = data2[ips[1]+"pruebaclase"+"1"]
        leerfichero2 = data2.get(ips[1]+"remotefile")
        buclesleerfichero2 = data2[ips[1]+"remotefile"+"2"]
        texto = "no hay texto"
        resultSuma1 = []
        resultSuma2 = []
        resulttexto1 = []
        resulttexto2 = []
        if(suma1):
            for x in range(int(buclesuma1)):
                print("suma")
                enviarNumero(sock,0)
                #envio numero 1 y 2
                enviarNumero(sock,num1)
                enviarNumero(sock,num2)
                #recibo la suma
                resultado = recibirNumero(sock)
                resultSuma1.append(resultado)
        if(leerfichero1):
            for x in range(int(buclesleerfichero1)):
                print("leer")
                enviarNumero(sock,1)
                texto = recibirTexto(sock)
                resulttexto1.append(texto)
        if(suma2):
            for x in range(int(buclesuma2)):
                print("suma")
                enviarNumero(sock,2)
                #envio numero 1 y 2
                enviarNumero(sock,num1)
                enviarNumero(sock,num2)
                #recibo la suma
                resultado = recibirNumero(sock)
                resultSuma2.append(resultado)
        if(leerfichero2):
            for x in range(int(buclesleerfichero2)):
                enviarNumero(sock,3)
                texto = recibirTexto(sock)
                resulttexto1.append(texto)
                resulttexto2.append(texto)
        return ("texto por maquina1: " + str(resulttexto1)+ " suma por maquina1 : " + str(resultSuma1)+ "texto por maquina2: " + str(resulttexto2)+ " suma por maquina2 : " + str(resultSuma2))
        
if __name__ == '__main__':
    app.run(debug = False, port = 80,host = '0.0.0.0')
