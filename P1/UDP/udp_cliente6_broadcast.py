import socket, sys

if (len(sys.argv) == 2 or len(sys.argv) > 3):
    print("USO: python3 udp_cliente1.py <IP> <Puerto>")
    exit(1)

if (len(sys.argv) == 3):
    ip = sys.argv[1]
    puerto = int(sys.argv[2])
else:
    ip = "127.0.0.1"
    puerto = 12345

print("IP y puerto establecidos: ", ip, ":", puerto)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

mensaje = input("# ")


while True and mensaje != "FIN":
    checksum = s.sendto(mensaje.encode("utf-8"),(ip, puerto))
    
    s.settimeout(1)
    try:
        datagrama, origen = s.recvfrom(1024) # Tamaño máximo a recibir
        datagrama = datagrama.decode("utf8")
        print(datagrama)
    except socket.timeout:
        print("Error -> No hay mas respuestas disponibles")
    
    mensaje = input("# ")
print("Chat cerrado")