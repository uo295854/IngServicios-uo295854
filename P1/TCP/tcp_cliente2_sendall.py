import socket, sys

if len(sys.argv)<3:
    puerto = 9999
    addr = '127.0.0.1'
else:
    puerto = int(sys.argv[2])
    addr = sys.argv[1]
    
s=socket.socket()
s.connect((addr, puerto))
mensaje = "ABCDE"

for i in range(5):
    respuesta = s.sendall(mensaje.encode("utf-8"))
    print("Enviado mensaje ", i, " de ", len(mensaje))
s.send("FINAL".encode("utf-8"))
print("Mensaje FINAL enviado")
s.close()