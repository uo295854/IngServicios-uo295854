import socket, sys, time
def recibe_longitud(s):
    i = 0
    buffer = []
    n = ""
    r = ""
    while n != b"\n":
        b = s.recv(1)
        if len(b) == 0:
            return b
        elif b == b"\n":
            n = b
        buffer.append(b)
    return b"".join(buffer)
def recibe_resto_mensaje(s, longitud):
    #prueba
	mensaje=s.recv(longitud)
	return mensaje

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

#Comprobacion de si el puerto esta introducido como parametro o no
if len(sys.argv) < 2:
        puerto = 9999
else:
        puerto = int(sys.argv[1], 10)

# Asignarle puerto
s.bind(("", puerto))
print("Puerto asginado: ", puerto)
# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()
# Bucle principal de espera por clientes
while True:
	print("Esperando un cliente")
	sd, origen = s.accept()
	time.sleep(1)
	print("Nuevo cliente conectado desde %s, %d" % origen)
	continuar = True
	# Bucle de atención al cliente conectado
	while continuar:
		# Primero recibir el mensaje del cliente
		longitud= recibe_longitud(sd)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
		longitud = str(longitud, "utf8") # Convertir los bytes a caracteres
		# Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
		longitud = longitud[:-1]  # slice desde el principio hasta el final -2
		mensaje = recibe_resto_mensaje(sd,int(longitud)) 
		#Convertir los bytes a caracteres
		mensaje=str(mensaje, "utf8")
		# Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
		#linea = mensaje[:-2]  # slice desde el principio hasta el final -2
		# Tercero, darle la vuelta
		linea = mensaje[::-1]
		# Finalmente, enviarle la respuesta con un fin de línea añadido
		sd.sendall(bytes(linea+"\r\n", "utf8"))
		# Observa la transformación en bytes para enviarlo
		#En este ejemplo se asume que el texto recibido es ascii puro
		if mensaje=="":  # Si no se reciben datos, es que el cliente cerró el socket
			print("Conexión cerrada de forma inesperada por el cliente")
			sd.close()
			continuar = False
		elif mensaje=="ADIOS":
			print("Recibido mensaje de finalización")
			sd.close()
			continuar = False
		else:
			print("Recibido mensaje: %s" % mensaje)
