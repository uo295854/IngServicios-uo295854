import socket
import sys
import email.message, email.policy, email.utils

# 1. Define una función denominada RecvReply con dos parámetros: un socket y un código 
# (cadena de bytes). Esta función debe recibir hasta un máximo de 1024 bytes del 
# socket e imprimir por pantalla lo recibido. A continuación, extraerá los tres 
# primeros caracteres (bytes) de lo que ha recibido y verificará si coinciden con 
# el código recibido como parámetro. En caso de que no coincidan imprimirá por pantalla 
# un error y terminará el programa (sys.exit()). Si quieres, puedes imprimir también 
# la respuesta recibida por el socket, para depuración.
def RecvReply(socket, codigo):
 respuesta=socket.recv(1024).decode()
 print(respuesta)
 primeros=respuesta[:3]
 if codigo!=primeros:
     print("error: el codigo recibido no coincide con el esperado")
     print("recibido: " +  primeros)
     print("esperado: " +  codigo)
     sys.exit(1)
     
     
# 2. Dentro del programa principal define las siguientes variables y asígnales un 
# valor adecuado: server (dirección del servidor SMTP), port (puerto del servidor), 
# fromaddr (dirección de correo desde la que se envía), toaddr (dirección de correo
# a la que se envía), subject (asunto del mensaje), data (texto que va a contener el mensaje). 
# Configura el servidor como relay.uniovi.es y el puerto como 25. La dirección de envío y 
# la de recepción será la que tengas en uniovi.
server="relay.uniovi.es" 
port=25
fromaddr="uo295854@uniovi.es"
toaddr="uo295854@uniovi.es"
subject="Envia crudo - test p4.7 ingservicios"
data="Esto es una email de prueba del ejercicio7"
message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

# EJERCICIO 8 - construir el mensaje con email.message
mensaje = email.message.EmailMessage()
mensaje['To'] = 'Alex Braña <{}>'.format(toaddr)
mensaje['From'] = 'Alex Braña <{}>'.format(fromaddr)
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

binario = mensaje.as_bytes(policy=email.policy.SMTP) + b".\r\n"

# 3. Crea una conexión de tipo TCP al servidor usando las variables creadas.
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((server,port))
RecvReply(s,"220")

# 4. A través de ese socket ya conectado, envía los comandos SMTP 
# necesarios para enviar el correo electrónico. Tras cada comando 
# llama a la función RecvReply para recibir la respuesta y verificar 
# que es correcta. Puede servirte de ayuda el ejemplo de diálogo SMTP 
# que aparece en Wikipedia.
s.sendall("HELO {}\r\n".format(socket.gethostname()).encode())
RecvReply(s, "250")

s.sendall("MAIL FROM: <{}>\r\n".format(fromaddr).encode())
RecvReply(s, "250")

s.sendall("RCPT TO: <{}>\r\n".format(toaddr).encode())
RecvReply(s, "250")

s.sendall(b'DATA\r\n')
RecvReply(s,"354")

s.sendall(binario)
RecvReply(s,"250")

s.sendall(b"QUIT\r\n")
RecvReply(s, "221")

s.close()