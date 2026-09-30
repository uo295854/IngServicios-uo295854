import socket, sys, time

def recvall(s, bytes_recibidos):
    iterador = 0
    mensaje = b""
    while iterador < bytes_recibidos:
        datos = s.recv(bytes_recibidos - iterador)
        mensaje = mensaje + datos
        iterador = len(mensaje)
    return mensaje

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


# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

if len(sys.argv)<2:
    puerto = 9999
else:
    puerto = int(sys.argv[1])

# Asignarle puerto
s.bind(("", puerto))
print("Puerto asignado: ", puerto)

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    time.sleep(1)
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        mensaje = recibe_mensaje(sd)
        
        mensaje = str(mensaje, "utf-8")

        linea = mensaje[:-2]
        
        linea = linea[::-1]
        
        sd.sendall(bytes(linea+"\r\n", "utf-8"))

        if mensaje=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif mensaje=="FINAL\r\n":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % mensaje)
            
s.close()