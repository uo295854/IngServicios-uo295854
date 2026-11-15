import paramiko
import base64
import getpass

HOST = "localhost"
USER = "alex"
clave = getpass.getpass("Clave? ")

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHyRj3lFV2yJkuFsTPjcx7SX0dG57HzBLkViy3a2iW91'))   # tu clave de host ed25519
client.get_host_keys().add(HOST, 'ssh-ed25519', key)
client.connect(HOST, username=USER, password=clave)

sftp = client.open_sftp()
for nombre in sftp.listdir():
    print(nombre)

sftp.close()
client.close()