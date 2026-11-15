# instance/config.py
import os
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://amigosuser:amigospass@172.18.0.2/amigosdb" #modo pruebas
#SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://") #modo contenedorizado