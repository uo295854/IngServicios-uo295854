import socket, sys, random
    
if (len(sys.argv) < 2):
    puerto = 9999
else:
    puerto = int(sys.argv[2])
    
print("Puerto establecido: ", puerto)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

while True:
    datagrama, origen = s.recvfrom(1024)
    if (random.randint(0, 100) < 50):
        print("Simulando datagrama perdido")
        continue
    print("Datagrama recibido")
    print("Origen del datagrama: ", origen)
    print("Información: ", datagrama.decode("utf8"))
    