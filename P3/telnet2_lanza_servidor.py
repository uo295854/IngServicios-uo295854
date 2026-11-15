import telnetlib
import time

HOST = "localhost"
USER = "alex"
PASSWORD = "1234"
SERVIDOR = "udp_servidor3_con_ok.py"

# 1. Se conecte usando telnetlib con el servidor Linux, usando la misma técnica que 
# en el ejercicio anterior, pero en esta ocasión sin preguntar al usuario nombre 
# y clave, sino incrustando éstas directamente en el código fuente (es una mala 
# práctica de cara a la seguridad, pero lo haremos así en igualmente para este ejercicio)
tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(USER.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode("ascii") + b"\n")

# 2. Una vez conectado, lee la respuesta del telnet usando read_until(b"$") esto leerá 
# lo que el shell remoto nos envía, hasta que se reciba un signo dólar. Ya que el signo 
# dólar es parte del prompt, al recibirlo sabremos que el shell remoto está listo para recibir comandos.
tn.read_until(b"$")

# 3. Envía el comando ps -ef\n que lista todos los procesos del usuario (¡no olvides enviar el \n al final!)
tn.write(b"ps -efww\n")

# 4. Usa de nuevo read_until() para esperar al próximo prompt y captura la respuesta en una variable. 
# Esa respuesta contendrá la salida del comando ps -ef que le habíamos pedido.
respuesta = tn.read_until(b"$").decode("utf-8")

# 5. Comprueba si la respuesta recibida contiene la cadena udp_servidor3_con_ok.py, lo que denotaría que el 
# servicio está en ejecución. En ese caso imprime “El servidor ya está en ejecución” y terminará.
if SERVIDOR in respuesta:
    print("El servidor ya está en ejecución")
    tn.write(b"exit\n")
    tn.read_all()
else:
# 6. Si esa cadena no está presente (el servidor no está en ejecución), lo lanzaremos, enviando por telnet 
# la orden nohup python3 udp_servidor3_con_ok.py &\n (¡no olvides el retorno de carro!).
# El & final es para que el shell devuelva el prompt y así poder lanzarle un exit después.
# El nohup inicial es para que el servidor siga corriendo cuando cerremos la conexión telnet 
# (de lo contrario, al estar lanzado desde esta “terminal”, moriría al cerrar telnet). 
# Se creará un fichero llamado nohup.out que contendrá la salida del comando, en lugar de ir a la terminal.
    tn.write(b"nohup python3 " + SERVIDOR.encode() + b" &\n")

# 7. Espera un segundo para dar tiempo a que el servidor arranque (time.sleep(1))
    time.sleep(1)
    
# 8. Envía el comando exit\n para terminar el shell remoto y por tanto la sesión telnet.
    tn.write(b"exit\n")
    
# 9. Recoge la respuesta del servidor con read_all() y muéstrala en pantalla para depuración.
    print(tn.read_all().decode("utf-8"))
    
tn.close()