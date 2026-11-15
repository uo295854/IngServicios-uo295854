import os
import sys
import paramiko
import base64
import getpass
from stat import S_ISDIR

HOST = "localhost"
USER = "alex"
carpeta = sys.argv[1] if len(sys.argv) > 1 else input("Carpeta remota: ")
clave = getpass.getpass("Clave? ")

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAA...'))
client.get_host_keys().add(HOST, 'ssh-ed25519', key)
client.connect(HOST, username=USER, password=clave)

sftp = client.open_sftp()
sftp.chdir(carpeta)

os.makedirs("descargas", exist_ok=True)   # carpeta local de destino
for nombre in sftp.listdir():
    if S_ISDIR(sftp.stat(nombre).st_mode):
        continue                            # saltar subcarpetas
    sftp.get(nombre, os.path.join("descargas", nombre))
    print("Descargado:", nombre)

sftp.close()
client.close()