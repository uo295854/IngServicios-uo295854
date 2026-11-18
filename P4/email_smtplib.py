import getpass
import smtplib
import email

server = "smtp.gmail.com"
port = 587
fromaddr = "articgmerpkmn@gmail.com"
toaddr = "articgmerpkmn@gmail.com"
subject = "Envia crudo - test p4 ej12 ingservicios"
data = "Esto es un email de prueba del ejercicio 12"

mensaje = email.message.EmailMessage()
mensaje['To']='<{}>'.format(toaddr)
mensaje['From']='<{}>'.format(fromaddr)
mensaje['Subject']='<{}>'.format(subject)
mensaje['Date']=email.utils.formatdate(localtime=True)
mensaje['Message-ID']=email.utils.make_msgid()
mensaje.set_content("{}\r\n. \r\n".format(data))

s = smtplib.SMTP(server, port)
s.set_debuglevel(1)
s.starttls()

username=input("Usuario: ")
password=getpass.getpass("Contraseña: ")
s.login(username,password)
s.sendmail(fromaddr,toaddr,mensaje.as_bytes())
s.quit()