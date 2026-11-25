import socket
import sys
import ssl
import base64
import getpass

def RecvReply(sock, codigo):
 respuesta=sock.recv(1024).decode()
 print(respuesta)
 primeros=respuesta[:3]
 if codigo!=primeros:
     print("error: el codigo recibido no coincide con el esperado")
     print("recibido: " +  primeros)
     print("esperado: " +  codigo)
     sys.exit(1)
     
server = "smtp.gmail.com"
port = 587
fromaddr = "articgmerpkmn@gmail.com"
toaddr = "uo295854@uniovi.es"
subject = "Envia crudo - test autoría ingservicios"
data = "Esto es un email de prueba del test autoría ingservicios"
message = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s\r\n.\r\n" % (
    toaddr, fromaddr, subject, data)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((server,port))
RecvReply(s,"220")

s.sendall("EHLO {}\r\n".format(socket.gethostname()).encode())
RecvReply(s, "250")

s.sendall(b"STARTTLS\r\n")
RecvReply(s, "220")

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