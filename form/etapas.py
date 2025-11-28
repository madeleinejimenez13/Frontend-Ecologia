# form/etapas.py
"""
Blueprint para gestión de etapas del ciclo de vida
"""

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from wtforms import Form, StringField, FloatField, TextAreaField, validators
from form.utils import load_data, save_data, find_by_id

etapas_bp = Blueprint('etapas', __name__, template_folder='../templates', url_prefix='/etapas')

class EtapaForm(Form):
    """Formulario para crear/editar etapas"""
    nombre = StringField('Nombre de la etapa', [validators.InputRequired(), validators.Length(min=2, max=120)])
    co2 = FloatField('CO2 (kg)', [validators.InputRequired()])
    agua = FloatField('Agua (L)', [validators.InputRequired()])
    residuos = FloatField('Residuos (kg)', [validators.InputRequired()])
    descripcion = TextAreaField('Descripción', [validators.Optional(), validators.Length(max=1000)])

@etapas_bp.route('/<int:dispositivo_id>/crear', methods=['GET','POST'])
def crear_etapa(dispositivo_id):
    """
    Crea una nueva etapa para un dispositivo
    
    Args:
        dispositivo_id: ID del dispositivo al que pertenece la etapa
    """
    form = EtapaForm(request.form)
    data_file = current_app.config['DATA_FILE']
    data = load_data(data_file)
    dispositivo = find_by_id(data.get('dispositivos', []), dispositivo_id)
    
    if not dispositivo:
        flash('⚠️ Dispositivo no encontrado.', 'danger')
        return redirect(url_for('dispositivos.list_dispositivos'))
    
    if request.method == 'POST' and form.validate():
        etapas = dispositivo.setdefault('etapas', [])
        etapa_id = 1 if not etapas else max(e.get('id',0) for e in etapas) + 1
        etapa = {
            "id": etapa_id,
            "nombre": form.nombre.data,
            "impacto": {
                "CO2": form.co2.data, 
                "agua": form.agua.data, 
                "residuos": form.residuos.data
            },
            "descripcion": form.descripcion.data,
            "decisiones": []
        }
        etapas.append(etapa)
        dispositivo['numero_etapas'] = len(etapas)
        save_data(data_file, data)
        flash('✅ Etapa creada exitosamente.', 'success')
        return redirect(url_for('dispositivos.list_dispositivos'))
    
    return render_template('dispositivos_list.html', dispositivos=[dispositivo])