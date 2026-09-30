import socket, sys

if len(sys.argv)<3:
    puerto = 9999
    addr = '127.0.0.1'
else:
    puerto = int(sys.argv[2])
    addr = sys.argv[1]
    
s=socket.socket()
s.connect((addr, puerto))
s.send("Hola!\r\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))
s.send("test!\r\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))
s.close()