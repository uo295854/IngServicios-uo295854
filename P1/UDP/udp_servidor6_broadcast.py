import socket, sys, random
    
if (len(sys.argv) < 2):
    puerto = 12345
else:
    puerto = int(sys.argv[2])
    
print("Puerto establecido: ", puerto)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("", puerto))

while True:
    datagrama, origen = s.recvfrom(1024)
    
    mensajeRecibido = datagrama.decode("utf8")
    mensajeRespuesta = ""
    
    if (mensajeRecibido =="BUSCANDO HOLA"):
        mensajeRespuesta = "IMPLEMENTO HOLA"
        
    if (mensajeRecibido =="HOLA"):
        mensajeRespuesta = "HOLA IP " + str(origen[0])
        
        
    print("Datagrama recibido")
    print("Origen del datagrama: ", origen)
    print("Información: ", datagrama.decode("utf8"))
    s.sendto(mensajeRespuesta.encode("utf8"), origen)
    
    