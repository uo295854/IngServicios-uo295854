from flask import Blueprint

bienvenido = Blueprint("bienvenido", __name__)

from app.bienvenido import views