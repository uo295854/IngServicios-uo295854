import socket, sys, time

def recibe_mensaje(socket):
    buffer = []
    byte_recibido = ""
    marca_r = ""
    marca_n = ""
    while marca_n!=b"\n" or marca_r!=b"\r":
        byte_recibido = socket.recv(1)
        buffer.append(byte_recibido)
        if byte_recibido==b"\n":
            marca_n = byte_recibido
        elif byte_recibido==b"\r":
            marca_r = byte_recibido
        elif len(byte_recibido)==0:
            return byte_recibido
        buffer.append(byte_recibido)
    return b"".join(buffer)


if len(sys.argv)<3:
    puerto = 9999
    addr = '127.0.0.1'
else:
    puerto = int(sys.argv[2])
    addr = sys.argv[1]
    
s=socket.socket()
s.connect((addr, puerto))
s.send("Hola!\r\n".encode("utf-8"))
print(recibe_mensaje(s).decode("utf-8"))
s.send("test!\r\n".encode("utf-8"))
print(recibe_mensaje(s).decode("utf-8"))


s.close()