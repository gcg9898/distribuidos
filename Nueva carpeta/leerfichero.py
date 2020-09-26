#!/usr/bin/python

import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 15000)
sock.connect(server_address)
tam = sock.recv(1)
tam = int(tam.decode()) 
lentexto = sock.recv(tam)
texto = sock.recv(int(lentexto.decode()))
print(str(tam))
print(texto.decode())
texto = texto.decode()
archivo = open(texto)
texto = archivo.read()
#enviar texto
print(texto)
sock.sendall(bytes(str(len(str(len(texto)))), 'utf-8'))
sock.sendall(bytes(str(len(texto)), 'utf-8'))
sock.sendall(bytes(texto, 'utf-8'))
sock.close()