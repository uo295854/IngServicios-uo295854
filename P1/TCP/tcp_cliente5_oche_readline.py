import socket, sys, time

def recibe_mensaje(socket):
    fichero = socket.makefile(encoding="utf-8", newline="\r\n")
    datamensaje = fichero.readline()
    return datamensaje


if len(sys.argv)<3:
    puerto = 9999
    addr = '127.0.0.1'
else:
    puerto = int(sys.argv[2])
    addr = sys.argv[1]
    
s=socket.socket()
s.connect((addr, puerto))

s.send("Hola!\r\n".encode("utf-8"))
print(recibe_mensaje(s))
s.send("test!\r\n".encode("utf-8"))
print(recibe_mensaje(s))

s.close()