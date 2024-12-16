# app/config.py

import configparser

# Función para cargar la configuración desde el archivo config.ini
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Asegúrate de que la configuración necesaria esté presente
    if 'network' not in config:
        config['network'] = {'ipAddress': '127.0.0.1'}
    
    return config

# Puedes acceder a la configuración como:
config = load_config()

# Obtener valores de configuración
ip_address = config.get('network', 'ipAddress')
print(f"Dirección IP configurada: {ip_address}")
