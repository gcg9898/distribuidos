
import socket
import sys
import os
import threading
from libreriagra import enviarNumero, recibirNumero, enviarTexto, recibirTexto
servidor = "localhost"
def ejecutarSuma():
    os.system("python3 suma.py")
def ejecutarLeer():
    os.system("python3 leerfichero.py")
def recibirFichero(conn,nom):
    f =  open(nom, 'w') 
    print( 'file opened')
    tamdeltam = conn.recv(1)
    tam = conn.recv(int(tamdeltam.decode()))
    data = conn.recv(int(tam.decode()))
    f.write(data.decode())
def ficheroExiste(nom):
    return os.path.exists(nom)
def suma(result,connection):
    enviarNumero(connection,result)
def leerFichero(texto,connection):
    print(texto)
    enviarTexto(connection,texto)
def crearFichero(titulo, contenido):
    f =  open(titulo, 'w') 
    print( 'file opened')
    f.write(contenido)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('172.31.86.59', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
#creo el servidor para los clientes locales
server_address = ('0.0.0.0', 15000)
sock2.bind(server_address)
sock2.listen(2)
while(True):
    op = recibirNumero(sock)
    if(op == 2):
        if(not(ficheroExiste("suma.py"))):
            recibirFichero(sock,"suma.py")
        num1 = recibirNumero(sock)
        num2 = recibirNumero(sock)
        #envio resultado
        x = threading.Thread(target=ejecutarSuma)
        x.start()
        connection,a = sock2.accept()
        print("conexion suma creada")
        enviarNumero(connection, num1)
        enviarNumero(connection, num2)
        result = recibirNumero(connection)
        connection.close()
        suma(result,sock)
    if(op == 3):
        if(not(ficheroExiste("leerfichero.py"))):
            recibirFichero(sock,"leerfichero.py")
        texto = recibirTexto(sock)
        y = threading.Thread(target=ejecutarLeer)
        y.start()
        connection2,a = sock2.accept()
        print("conexion leer creada")
        #enviar nombre fichero
        enviarTexto(connection2,texto)
        lectura = recibirTexto(connection2)
        connection2.close()
        leerFichero(lectura,sock)
    if(op == 6):
        titulo = recibirTexto(sock)
        contenido = recibirTexto(sock)
        crearFichero(titulo,contenido)
    if(op == 9): 
        direc = os.listdir()
        enviarNumero(sock,len(direc))
        for i in os.listdir():
            enviarTexto(sock,i)   
        
