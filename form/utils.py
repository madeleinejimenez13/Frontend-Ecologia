# form/utils.py
"""
Funciones de utilidad para manejo de datos
"""
import json
import os

def load_data(data_file):
    """
    Carga datos desde el archivo JSON
    
    Args:
        data_file: Ruta del archivo JSON
        
    Returns:
        dict: Datos cargados o estructura vacía
    """
    if not os.path.exists(data_file):
        return {"dispositivos": []}
    
    with open(data_file, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"dispositivos": []}

def save_data(data_file, data):
    """
    Guarda datos en el archivo JSON
    
    Args:
        data_file: Ruta del archivo JSON
        data: Datos a guardar
    """
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def next_id(items):
    """
    Genera el siguiente ID disponible
    
    Args:
        items: Lista de elementos con 'id'
        
    Returns:
        int: Siguiente ID disponible
    """
    if not items:
        return 1
    return max(item.get('id', 0) for item in items) + 1

def find_by_id(items, _id):
    """
    Busca un elemento por ID
    
    Args:
        items: Lista de elementos
        _id: ID a buscar
        
    Returns:
        dict o None: Elemento encontrado o None
    """
    for item in items:
        if item.get('id') == _id:
            return item
    return None