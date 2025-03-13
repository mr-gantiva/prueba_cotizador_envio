# main.py

import requests
from config import API_URL, API_CREDENTIALS  # Importar configuración



# Datos del envío (body del request)
data = {
    "codigoCiudadOrigen": 1,          # Código de ciudad de origen
    "codigoCiudadDestino": 98,        # Código de ciudad de destino
    "codigoAgenciaDestino": 0,        # Siempre 0
    "codigoAgenciaOrigen": 0,         # Siempre 0
    "alto": 59.12,                    # Alto en cm
    "ancho": 59.12,                   # Ancho en cm
    "largo": 59.12,                   # Largo en cm
    "kilos": 14.6,                    # Peso en kg
    "cuentaCorriente": "",            # Opcional
    "cuentaCorrienteDV": "",          # Opcional
    "rutCliente": "247919686"                  # Opcional
}

# Hacer la solicitud POST
try:
    response = requests.post(API_URL, json=data, headers=API_CREDENTIALS)
    response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

except requests.exceptions.HTTPError as err:
    print(f"Error HTTP: {err}")
    print(response.text) # Mostrar el mensaje de error
except requests.exceptions.RequestException as err:
    print(f"Error en la solicitud: {err}")
else:
    #Procesar la respuesta JSON
    respuesta = response.json()
    print("Respuesta de la API:", respuesta)


#Extraer y mostrar el costo total del envio
if respuesta.get("codigoRespuesta") == 1: # Si la busqueda fue exitosa
    tarifas = respuesta.get("listaTarifas", [])
    for tarifa in tarifas:
        print(f"Costo total: {tarifa['costoTotal']}")
        print(f"Días de entrega: {tarifa['diasEntrega']}")
        print(f"Tipo de Entrega: {tarifa['tipoEntrega']['descripcionTipoEntrega']}")
        print(f"Tipo de Servicio: {tarifa['tipoServicio']['descripcionTipoServicio']}")
        print("---")
