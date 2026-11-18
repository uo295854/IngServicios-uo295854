import dns.resolver

respuesta = dns.resolver.query('gmail.com', "MX")
respuesta = sorted(respuesta)

for i in respuesta:
    respuesta_ip = dns.resolver.query(i.exchange)
    print(str(i.preference) + " " + str(i.exchange) + " " + str(respuesta_ip[0].address))
