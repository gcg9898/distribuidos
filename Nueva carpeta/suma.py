#!/usr/bin/python

import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 15000)
sock.connect(server_address)
#recibo tam num 1
tam = sock.recv(1)
#recibo numero 1
a = sock.recv(int(tam.decode()))
num1 = int(a.decode())
print(str(num1))
#recibo tam num2
tam = sock.recv(1)
#recibo numero2
a = sock.recv(int(tam.decode()))
num2 = int(a.decode()) 
print(str(num2))
sum = num1 + num2
print(str(sum))
#envio tam resultado
sock.sendall(bytes(str(len(str(sum))),'utf-8'))
#enviar suma
sock.sendall(bytes(str(sum),'utf-8'))
sock.close()