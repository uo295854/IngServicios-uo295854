import socket,sys

s=socket.socket()
if len(sys.argv) < 3:
        puerto=9999
        addr='127.0.0.1'
else:
        puerto= int(sys.argv[2],10)
        addr=sys.argv[1]
        
s.connect((addr,puerto))
mensaje="HOLA"
longitud  = "%d\n" % len(bytes(mensaje, "utf8")) 
todo=longitud+mensaje
print(todo)
s.sendall(bytes(todo, "utf8"))
print(s.recv(1024).decode('utf8'))
mensaje='ADIOS'
longitud="%d\n" % len(bytes(mensaje, "utf8"))
s.sendall(bytes(longitud+mensaje,"utf8"))
print(s.recv(1024).decode('utf8'))
