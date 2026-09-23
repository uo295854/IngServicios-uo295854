import socket, sys

if (len(sys.argv) == 2 or len(sys.argv) > 3):
    print("USO: python3 udp_cliente1.py <IP> <Puerto>")
    exit(1)

if (len(sys.argv) == 3):
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "localhost"
    puerto = 9999

print("IP y puerto establecidos: ", ip, ":", puerto)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((ip, puerto))
mensaje = input("# ")
while True and mensaje != "FIN":
    s.send(mensaje.encode("utf8"))
    mensaje = input("# ")
print("Chat cerrado")