import dns.resolver

respuesta = dns.resolver.query('apple.com')

for I in respuesta:
    print(I.address)
