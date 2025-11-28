# form/decisiones.py
"""
Blueprint para gestión de decisiones de mejora ambiental
Este módulo está preparado para futuras funcionalidades
"""

from flask import Blueprint

decisiones_bp = Blueprint(
    'decisiones', 
    __name__, 
    template_folder='../templates', 
    url_prefix='/decisiones'
)

# Las decisiones actualmente se crean automáticamente con los dispositivos
# Aquí podrían añadirse rutas para crear, editar o eliminar decisiones manualmente