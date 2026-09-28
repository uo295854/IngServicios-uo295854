import socket, sys

mensajesEnviados = 0

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
timeout_time = 0.1
while True and mensaje != "FIN":
    mensajesEnviados += 1
    mensaje = str(mensajesEnviados) + ": " + mensaje 
    s.send(mensaje.encode("utf8"))
    
    s.settimeout(timeout_time)
    while timeout_time < 2:
        try:
            datagrama, origen = s.recvfrom(1024) # Tamaño máximo a recibir
            datagrama = datagrama.decode("utf8")
            if datagrama=="OK":
                print("Recibida confirmación")
            else:
                print("Recibido datagrama no esperado")
        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega | timeout_time = ", timeout_time)
            if (timeout_time < 2):
                timeout_time *= 2
                continue
        except:    # Otras posibles excepciones dejamos que las maneje el usuario
            raise
    if (timeout_time >= 2):
        print("Se ha superado el tiempo máximo de espera, es posible que el servidor esté caído o conexón sea inestable.")
        break
    
    timeout_time = 0.1
    mensaje = input("# ")
print("Chat cerrado")