import socket
import sys
import email.message, email.policy, email.utils
import getpass
import smtplib
import email
import ssl

#Ejercicio 13 email_pop3_recibe_crudo.py

#Vamos a realizar un programa en python que, usando el protocolo POP3, reciba 
# correo electrónico de una cuenta de gmail. En primer lugar entra a través de 
# la aplicación web de gmail y vete a la configuración (icono de engranaje en la
# parte superior derecha y opción “Ver todos los ajustes”). Sobre la opción “Reenvío
# y correo POP/IMAP”, habilita POP para la recepción de mensajes. Ahora utiliza 
# algunos de los programas anteriores para enviar varios correos a esa cuenta de 
# correo. Con la configuración establecida de POP3 solo se accederá a los nuevos 
# correos enviados.

#Ahora escribe un programa en python llamado email_pop3_recibe_crudo.py que 
# reciba el correo electrónico. Para ello sigue los siguientes pasos:

# 1. Define una función denominada RecvReply con un parámetro: un socket. Esta 
# función debe recibir hasta un máximo de 1024 bytes e imprimir por pantalla lo recibido, 
# para depuración. A continuación, extraerá los tres primeros bytes recibidos y verificará 
# si coinciden con el código de éxito: b"+OK". En caso de que no coincidan imprimirá por 
# pantalla un error y terminará el programa (sys.exit()).

def RecvReply(sock):
    codigo = b"+OK"
    respuesta = sock.recv(1024)                     
    print(respuesta.decode("utf-8", errors="replace"))
    primeros = respuesta[:3]
    if codigo != primeros:
        print("error: el codigo recibido no coincide con el esperado")
        print("recibido:", primeros)
        print("esperado:", codigo)
        sys.exit(1)
    return respuesta  


# 2. Dentro del programa principal define las siguientes variables: server (dirección 
# del servidor POP3) y port (puerto del servidor). Configura el servidor como pop.gmail.com 
# y el puerto como 995.
server = "pop.gmail.com"
port = 995

# 3. Añade el código para leer el nombre de usuario y la contraseña por teclado 
# igual que en ejemplos anteriores.
username=input("Usuario: ")
password=getpass.getpass("Contraseña: ")

# 4. Crea la conexión del socket y establece el canal seguro:

s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Tras la conexión con éxito el servidor enviará un primer mensaje que debes
# leer con RecvReply()
RecvReply(sc)

# 5. Envía el comando USER y PASS para entrar en sesión (leyendo la respuesta 
# del servidor tras cada uno).
sc.sendall("USER {}\r\n".format(username).encode("utf-8"))
RecvReply(sc)
sc.sendall("PASS {}\r\n".format(password).encode("utf-8"))
RecvReply(sc)

# 6. Envía el comando STAT y verifica cuantos correos hay disponibles.
sc.sendall(b"STAT\r\n")
num_correos = int(RecvReply(sc).decode().split()[1])    
print("Numero de correos:", num_correos)

# 7. Lee el contenido del primer correo. Implementa un bucle para recibir el 
# correo completo. Recuerda que debe terminar en \r\n.\r\n.
sc.sendall(b"RETR 1\r\n")
datos = RecvReply(sc)                                     # "+OK ..." y quizá parte del mensaje
while not datos.endswith(b"\r\n.\r\n"):
    datos += sc.recv(4096)
    
texto = datos.decode("utf-8", errors="replace")

# 8. Extrae de las cabeceras el campo “Subject” y el campo “From” e imprímelo
# por pantalla.#

cabeceras = texto.split("\r\n\r\n")[0]
print("EXTRAEMOS LAS CABECERAS...")
for linea in cabeceras.split("\r\n"):
    if linea.startswith("Subject:") or linea.startswith("From:"):
        print(linea)

sc.sendall(b"QUIT\r\n")
sc.close()