import requests
from config import API_URL, API_HEADERS  # Importar configuración

# Funcion para obtener el nombre de la ciudad
def obtener_nombre_ciudad(codigo_ciudad, tipo="origen"):
    # Configurar la URL de la API
    url = (
        "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesOrigen"
        if tipo == "origen"
        else "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesDestino"
    )

    try:
        # Realizar la solicitud a la API
        response = requests.get(url, headers=API_HEADERS)
        response.raise_for_status()

        # Convertir la respuesta a JSON
        respuesta = response.json()

        # Verirficar si la respuesta tiene la estructura esperada
        if "listaCiudadesOrigen" in respuesta:
            ciudades = respuesta["listaCiudadesOrigen"]
        elif "listaCiudadesDestino" in respuesta:
            ciudades = respuesta["listaCiudadesDestino"]
        else:
            print("Error: La respuesta no contiene la lista de ciudades.")
            return "Ciudad no encontrada"
        
        # Buscar la ciudad por su código
        for ciudad in ciudades:
            if ciudad["codigoCiudad"] == codigo_ciudad:
                return ciudad["nombreCiudad"]
            
        # Si no se encuentra la ciudad
        return "Ciudad no encontrada"
    
    except requests.exceptions.RequestException as err:
        print(f"Error al obtener ciudades: {err}")
        return "Error"



# Datos del envío (body del request)
data = {
    "codigoCiudadOrigen": 1,          # Código de ciudad de origen
    "codigoCiudadDestino": 4,        # Código de ciudad de destino
    "codigoAgenciaDestino": 0,        # Siempre 0
    "codigoAgenciaOrigen": 0,         # Siempre 0
    "alto": 59.12,                    # Alto en cm
    "ancho": 59.12,                   # Ancho en cm
    "largo": 59.12,                   # Largo en cm
    "kilos": 14.6,                    # Peso en kg
    "cuentaCorriente": "",            # Opcional
    "cuentaCorrienteDV": "",          # Opcional
    "rutCliente": "13061694"                  # Opcional
}

## Obtener nombres de las ciudades
nombre_origen = obtener_nombre_ciudad(data["codigoCiudadOrigen"], tipo="origen")
nombre_destino = obtener_nombre_ciudad(data["codigoCiudadDestino"], tipo="destino")

print(f"Ciudad de origen: {nombre_origen}")
print(f"Ciudad de destino: {nombre_destino}")

# Hacer la solicitud POST para cotizar el envio
try:
    response = requests.post(API_URL, json=data, headers=API_HEADERS)
    response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

except requests.exceptions.HTTPError as err:
    print(f"Error HTTP: {err}")
    print(response.text) # Mostrar el mensaje de error
except requests.exceptions.RequestException as err:
    print(f"Error en la solicitud: {err}")
else:
    #Procesar la respuesta JSON
    respuesta = response.json()
    # print("Respuesta de la API:", respuesta)

#Extraer y mostrar el costo total del envio
    if respuesta.get("codigoRespuesta") == 1: # Si la busqueda fue exitosa
        tarifas = respuesta.get("listaTarifas", [])
        for tarifa in tarifas:
            print(f"Costo total: {tarifa['costoTotal']}")
            print(f"Días de entrega: {tarifa['diasEntrega']}")
            print(f"Tipo de Entrega: {tarifa['tipoEntrega']['descripcionTipoEntrega']}")
            print(f"Tipo de Servicio: {tarifa['tipoServicio']['descripcionTipoServicio']}")
            print("---")
