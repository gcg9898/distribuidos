import socket


def enviarNumero(connection,num):
    print('Iniciar enviar numero: ' + str(num))
    #enviar tam num 
    print('Tam del numero: ' + str(num) + ' siendo enviado')
    connection.sendall(bytes(str(len(str(num))),'utf-8'))
    #print('Tam del numero: ' + str(num) + ' que es ' + str(len(str(num)) + ' enviado')
    #enviar num
    print("Num siendo enviado")
    connection.sendall(bytes(str(num),'utf-8'))
    print('Envio del numero ' + str(num)+ ' finalizado')
def recibirNumero(sock):
    print('Iniciar recibir numero')
    #recibo el tamaño
    tam = sock.recv(1)
    print("el tam del numero es " + str(tam))
    #recibo el numero
    a = sock.recv(int(str(tam.decode())))
    num = int(a.decode())
    print('el numero es: ' + str(num))
    print('recibir numero finalizado')
    return num
def enviarTexto(connection,text):
    print('Iniciar enviar texto: ' + text)
    #envio el tam del tam del texto
    #print('enviando el tam del tam del texto que es: '+str(len(str(len(texto))) )
    connection.sendall(bytes(str(len(str(len(text)))),'utf-8'))
    print('tam del tam enviado')
    #envio tam del texto
    #print('enviando el tam del tam del texto que es: '+str(len(str(len(texto))) )
    connection.sendall(bytes(str(len(text)),'utf-8'))
    print('tam enviado')
    #envio texto
    print('Enviando texto')
    connection.sendall(bytes(text, 'utf-8'))
    print('Texto enviado')
    print('Envio de texto finalizado')
def recibirTexto(sock):
    #recibo el tam del tam del texto
    print('Iniciar recibir texto')
    tam = sock.recv(1)
    print('Tam del tam del texto recibido es: ' + tam.decode())
    #recibo el tam del texto
    lentext = sock.recv(int(tam.decode()))
    print('tam del texto recibido es ' + lentext.decode())
    #recibo el texto
    text = sock.recv(int(lentext.decode()))
    print('texto recibido es: '+ text.decode())
    return text.decode()