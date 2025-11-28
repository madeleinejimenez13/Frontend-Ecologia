# form/dispositivos.py - PARTE 1
"""
Blueprint para gestión de dispositivos
Incluye: creación, edición, eliminación y listado
"""

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from wtforms import Form, StringField, SelectField, TextAreaField, validators
from form.utils import load_data, save_data, next_id, find_by_id

# Crear Blueprint
dispositivos_bp = Blueprint(
    'dispositivos', 
    __name__, 
    template_folder='../templates', 
    url_prefix='/dispositivos'
)

# Formulario de Dispositivo
class DispositivoForm(Form):
    """Formulario para crear/editar dispositivos"""
    nombre = StringField(
        'Nombre', 
        [validators.InputRequired(), validators.Length(min=2, max=120)]
    )
    tipo = SelectField(
        'Tipo', 
        choices=[
            ('telefono', 'Teléfono'),
            ('laptop', 'Laptop'),
            ('monitor', 'Monitor'),
            ('tablet', 'Tablet')
        ], 
        validators=[validators.InputRequired()]
    )
    descripcion = TextAreaField(
        'Descripción breve', 
        [validators.Optional(), validators.Length(max=1000)]
    )
# form/dispositivos.py - PARTE 2
# AÑADE ESTO DESPUÉS DE LA PARTE 1

@dispositivos_bp.route('/')
def list_dispositivos():
    """
    Lista todos los dispositivos almacenados
    """
    data_file = current_app.config['DATA_FILE']
    data = load_data(data_file)
    dispositivos = data.get('dispositivos', [])
    return render_template('dispositivos_list.html', dispositivos=dispositivos)

@dispositivos_bp.route('/<int:dispositivo_id>/editar', methods=['GET', 'POST'])
def editar_dispositivo(dispositivo_id):
    """
    Edita un dispositivo existente
    
    Args:
        dispositivo_id: ID del dispositivo a editar
    """
    data_file = current_app.config['DATA_FILE']
    data = load_data(data_file)
    dispositivo = find_by_id(data.get('dispositivos', []), dispositivo_id)
    
    if not dispositivo:
        flash('⚠️ Dispositivo no encontrado.', 'danger')
        return redirect(url_for('dispositivos.list_dispositivos'))
    
    form = DispositivoForm(request.form, data=dispositivo)
    
    if request.method == 'POST' and form.validate():
        dispositivo['nombre'] = form.nombre.data
        dispositivo['tipo'] = form.tipo.data
        dispositivo['descripcion'] = form.descripcion.data
        save_data(data_file, data)
        flash('✅ Dispositivo actualizado correctamente.', 'success')
        return redirect(url_for('dispositivos.list_dispositivos'))
    
    return render_template('dispositivos_list.html', dispositivos=[dispositivo])

@dispositivos_bp.route('/<int:dispositivo_id>/eliminar', methods=['POST'])
def eliminar_dispositivo(dispositivo_id):
    """
    Elimina un dispositivo
    
    Args:
        dispositivo_id: ID del dispositivo a eliminar
    """
    data_file = current_app.config['DATA_FILE']
    data = load_data(data_file)
    dispositivos = data.get('dispositivos', [])
    dispositivo = find_by_id(dispositivos, dispositivo_id)
    
    if not dispositivo:
        flash('⚠️ Dispositivo no encontrado.', 'danger')
    else:
        dispositivos.remove(dispositivo)
        save_data(data_file, data)
        flash('✅ Dispositivo eliminado correctamente.', 'success')
    
    return redirect(url_for('dispositivos.list_dispositivos'))
# form/dispositivos.py - PARTE 3
# AÑADE ESTO DESPUÉS DE LA PARTE 2

# Datos predefinidos de dispositivos y etapas
TIPOS_DISPOSITIVOS_INFO = {
    'telefono': {
        'nombre': 'Smartphone', 
        'descripcion': 'Dispositivo móvil inteligente con múltiples funciones',
        'etapas': [
            {
                "nombre": "Extracción de Materias Primas", 
                "co2": 8.5, 
                "agua": 150.0, 
                "residuos": 3.2,
                "desc": "Minería de metales raros, litio, cobalto y otros materiales"
            },
            {
                "nombre": "Fabricación y Ensamblaje", 
                "co2": 12.3, 
                "agua": 220.0, 
                "residuos": 5.1,
                "desc": "Producción de componentes electrónicos y ensamblaje final"
            },
            {
                "nombre": "Distribución y Transporte", 
                "co2": 2.8, 
                "agua": 15.0, 
                "residuos": 0.8,
                "desc": "Transporte desde fábricas hasta puntos de venta"
            },
            {
                "nombre": "Uso y Consumo Energético", 
                "co2": 18.5, 
                "agua": 85.0, 
                "residuos": 1.2,
                "desc": "Consumo eléctrico durante la vida útil del dispositivo"
            },
            {
                "nombre": "Fin de Vida y Reciclaje", 
                "co2": 3.2, 
                "agua": 25.0, 
                "residuos": 2.5,
                "desc": "Gestión de residuos electrónicos y recuperación de materiales"
            }
        ]
    },
    'laptop': {
        'nombre': 'Laptop', 
        'descripcion': 'Computadora portátil para trabajo y entretenimiento',
        'etapas': [
            {
                "nombre": "Extracción de Materias Primas", 
                "co2": 45.0, 
                "agua": 800.0, 
                "residuos": 12.5,
                "desc": "Extracción de minerales para procesadores, memorias y baterías"
            },
            {
                "nombre": "Fabricación y Ensamblaje", 
                "co2": 125.0, 
                "agua": 1500.0, 
                "residuos": 28.0,
                "desc": "Manufactura de componentes y ensamblaje de la laptop"
            },
            {
                "nombre": "Distribución y Transporte", 
                "co2": 8.5, 
                "agua": 45.0, 
                "residuos": 2.1,
                "desc": "Logística y distribución global"
            },
            {
                "nombre": "Uso y Consumo Energético", 
                "co2": 180.0, 
                "agua": 350.0, 
                "residuos": 5.8,
                "desc": "Consumo energético durante 3-5 años de uso típico"
            },
            {
                "nombre": "Fin de Vida y Reciclaje", 
                "co2": 12.0, 
                "agua": 120.0, 
                "residuos": 15.2,
                "desc": "Desmontaje y recuperación de componentes valiosos"
            }
        ]
    },
    'monitor': {
        'nombre': 'Monitor', 
        'descripcion': 'Pantalla de visualización para computadoras',
        'etapas': [
            {
                "nombre": "Extracción de Materias Primas", 
                "co2": 32.0, 
                "agua": 650.0, 
                "residuos": 9.8,
                "desc": "Obtención de materiales para panel LCD/LED y circuitos"
            },
            {
                "nombre": "Fabricación y Ensamblaje", 
                "co2": 85.0, 
                "agua": 1200.0, 
                "residuos": 22.0,
                "desc": "Producción del panel de visualización y electrónica"
            },
            {
                "nombre": "Distribución y Transporte", 
                "co2": 6.2, 
                "agua": 35.0, 
                "residuos": 1.5,
                "desc": "Transporte y embalaje del producto"
            },
            {
                "nombre": "Uso y Consumo Energético", 
                "co2": 95.0, 
                "agua": 180.0, 
                "residuos": 3.2,
                "desc": "Energía consumida durante su vida útil"
            },
            {
                "nombre": "Fin de Vida y Reciclaje", 
                "co2": 8.5, 
                "agua": 90.0, 
                "residuos": 11.5,
                "desc": "Reciclaje de metales, plásticos y componentes electrónicos"
            }
        ]
    },
    'tablet': {
        'nombre': 'Tablet', 
        'descripcion': 'Dispositivo táctil versátil para múltiples usos',
        'etapas': [
            {
                "nombre": "Extracción de Materias Primas", 
                "co2": 15.0, 
                "agua": 280.0, 
                "residuos": 5.5,
                "desc": "Minería de materiales para pantalla táctil y batería"
            },
            {
                "nombre": "Fabricación y Ensamblaje", 
                "co2": 28.0, 
                "agua": 450.0, 
                "residuos": 9.2,
                "desc": "Fabricación de pantalla táctil y ensamblaje de componentes"
            },
            {
                "nombre": "Distribución y Transporte", 
                "co2": 4.2, 
                "agua": 25.0, 
                "residuos": 1.2,
                "desc": "Distribución desde centros de producción"
            },
            {
                "nombre": "Uso y Consumo Energético", 
                "co2": 32.0, 
                "agua": 120.0, 
                "residuos": 2.1,
                "desc": "Consumo energético durante 3-4 años de uso"
            },
            {
                "nombre": "Fin de Vida y Reciclaje", 
                "co2": 5.5, 
                "agua": 45.0, 
                "residuos": 4.8,
                "desc": "Recuperación de materiales y gestión de residuos"
            }
        ]
    }
}

# Decisiones genéricas de mejora ambiental
DECISIONES_GENERICAS = [
    {
        "id": 1, 
        "nombre": "Usar materiales reciclados", 
        "impacto": {"CO2": -0.8, "agua": -15.0, "residuos": -0.5}
    },
    {
        "id": 2, 
        "nombre": "Optimizar procesos productivos", 
        "impacto": {"CO2": -1.2, "agua": -25.0, "residuos": -0.8}
    },
    {
        "id": 3, 
        "nombre": "Energía renovable", 
        "impacto": {"CO2": -2.5, "agua": -10.0, "residuos": -0.3}
    },
    {
        "id": 4, 
        "nombre": "Diseño modular reparable", 
        "impacto": {"CO2": -1.5, "agua": -20.0, "residuos": -1.2}
    }
]
# form/dispositivos.py - PARTE 4 (FINAL)
# AÑADE ESTO DESPUÉS DE LA PARTE 3

@dispositivos_bp.route('/crear-automatico/<tipo>', methods=['GET'])
def crear_dispositivo_automatico(tipo):
    """
    Crea un dispositivo automáticamente con datos predefinidos
    
    Args:
        tipo: Tipo de dispositivo (telefono, laptop, monitor, tablet)
    """
    data_file = current_app.config['DATA_FILE']
    data = load_data(data_file)
    dispositivos = data.setdefault('dispositivos', [])
    new_id = next_id(dispositivos)

    # Validar tipo
    if tipo not in TIPOS_DISPOSITIVOS_INFO:
        flash('⚠️ Tipo de dispositivo no válido.', 'danger')
        return redirect(url_for('dispositivos.list_dispositivos'))

    # Obtener información del tipo
    info = TIPOS_DISPOSITIVOS_INFO[tipo]
    
    # Crear estructura del dispositivo
    dispositivo = {
        "id": new_id,
        "nombre": info['nombre'],
        "tipo": tipo,
        "numero_etapas": len(info['etapas']),
        "descripcion": info['descripcion'],
        "etapas": []
    }

    # Crear etapas con sus impactos
    for i, etapa_data in enumerate(info['etapas']):
        # Variar las decisiones disponibles según la etapa
        num_decisiones = 2 + (i % 3)  # Entre 2 y 4 decisiones
        
        etapa = {
            "id": i + 1,
            "nombre": etapa_data["nombre"],
            "impacto": {
                "CO2": etapa_data["co2"],
                "agua": etapa_data["agua"],
                "residuos": etapa_data["residuos"]
            },
            "descripcion": etapa_data.get("desc", f"Impactos ambientales de: {etapa_data['nombre']}"),
            "decisiones": DECISIONES_GENERICAS[:num_decisiones]
        }
        dispositivo["etapas"].append(etapa)

    # Guardar dispositivo
    dispositivos.append(dispositivo)
    save_data(data_file, data)
    
    flash(
        f'✅ Dispositivo "{info["nombre"]}" creado exitosamente con {len(info["etapas"])} etapas del ciclo de vida.', 
        'success'
    )
    
    return redirect(url_for('dispositivos.list_dispositivos'))