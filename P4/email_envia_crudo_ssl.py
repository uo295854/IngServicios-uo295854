import socket
import sys
import ssl
import base64
import getpass

# 1. Define una función denominada RecvReply con dos parámetros: un socket y un código 
# (cadena de bytes). Esta función debe recibir hasta un máximo de 1024 bytes del 
# socket e imprimir por pantalla lo recibido. A continuación, extraerá los tres 
# primeros caracteres (bytes) de lo que ha recibido y verificará si coinciden con 
# el código recibido como parámetro. En caso de que no coincidan imprimirá por pantalla 
# un error y terminará el programa (sys.exit()). Si quieres, puedes imprimir también 
# la respuesta recibida por el socket, para depuración.
def RecvReply(sock, codigo):
 respuesta=sock.recv(1024).decode()
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
server = "smtp.gmail.com"
port = 587
fromaddr = "articgmerpkmn@gmail.com"
toaddr = "articgmerpkmn@gmail.com"
subject = "Envia crudo - test p4 ej11 ingservicios"
data = "Esto es un email de prueba del ejercicio 11"
message = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s\r\n.\r\n" % (
    toaddr, fromaddr, subject, data)

# 3. Crea una conexión de tipo TCP al servidor usando las variables creadas.
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((server,port))
RecvReply(s,"220")

# 4. A través de ese socket ya conectado, envía los comandos SMTP 
# necesarios para enviar el correo electrónico. Tras cada comando 
# llama a la función RecvReply para recibir la respuesta y verificar 
# que es correcta. Puede servirte de ayuda el ejemplo de diálogo SMTP 
# que aparece en Wikipedia.
s.sendall("EHLO {}\r\n".format(socket.gethostname()).encode())
RecvReply(s, "250")

s.sendall(b"STARTTLS\r\n")
RecvReply(s, "220")

# A partir de aquí todo va por el socket cifrado (sc)
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

sc.sendall("EHLO {}\r\n".format(socket.gethostname()).encode())
RecvReply(sc, "250")

sc.sendall(b"AUTH LOGIN\r\n")
RecvReply(sc, "334")

#login
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

sc.sendall(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, "334")

sc.sendall(base64.b64encode(password.encode("utf8")) + b"\r\n")
RecvReply(sc, "235")

sc.sendall("MAIL FROM: <{}>\r\n".format(fromaddr).encode())
RecvReply(sc, "250")

sc.sendall("RCPT TO: <{}>\r\n".format(toaddr).encode())
RecvReply(sc, "250")

sc.sendall(b"DATA\r\n")
RecvReply(sc, "354")

sc.sendall(message.encode("utf-8"))
RecvReply(sc, "250")

sc.sendall(b"QUIT\r\n")
RecvReply(sc, "221")

sc.close()