# main.py
from flask import Flask, render_template
from form.dispositivos import dispositivos_bp
from form.etapas import etapas_bp
from form.decisiones import decisiones_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'simuvidatech-secret-key-2025'
    app.config['DATA_FILE'] = os.path.join(app.root_path, 'data', 'dispositivos.json')
    
    # Asegurar que existe el directorio y archivo de datos
    os.makedirs(os.path.dirname(app.config['DATA_FILE']), exist_ok=True)
    if not os.path.exists(app.config['DATA_FILE']):
        import json
        with open(app.config['DATA_FILE'], 'w') as f:
            json.dump({"dispositivos": []}, f)
    
    app.register_blueprint(dispositivos_bp)
    app.register_blueprint(etapas_bp)
    app.register_blueprint(decisiones_bp)
    return app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)