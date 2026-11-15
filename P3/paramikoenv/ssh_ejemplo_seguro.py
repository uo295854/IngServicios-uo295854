import paramiko
import time
import base64

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHyRj3lFV2yJkuFsTPjcx7SX0dG57HzBLkViy3a2iW91'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
client.connect('localhost', username='alex', password='1234')
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()