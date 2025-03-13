from flask import Flask, render_template
import requests
import json
from config import API_URL, API_HEADERS

app = Flask(__name__)

# Cargar datos desde el archivo JSON
def cargar_datos():
    with open('datos_envios.json', 'r') as file:
        datos = json.load(file)
    return datos

# Función para obtener el nombre de la ciudad
def obtener_nombre_ciudad(codigo_ciudad, tipo="origen"):
    url=(
        "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesOrigen"
        if tipo == "origen" 
        else "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesDestino"  
    )

    try:
        response = requests.get(url, headers=API_HEADERS)
        response.raise_for_status()

        # Convertir la respuesta a JSON
        respuesta = response.json()

        # Verificar si la respuesta tiene la estructura esperada
        if "listaCiudadesOrigen" in respuesta:
            ciudades = respuesta["listaCiudadesOrigen"]
        elif "listaCiudadesDestino" in respuesta:
            ciudades = respuesta["listaCiudadesDestino"]
        else:
            return "Ciudad no encontrada"
        
        # Buscar la ciudad por su código
        for ciudad in ciudades:
            if ciudad["codigoCiudad"] == codigo_ciudad:
                return ciudad["nombreCiudad"]
            
            # Si no se encuentra la ciudad
        return "Ciudad no encontrada"
    except requests.exceptions.RequestException as err:
        return f"Error: {err}"
    
@app.route("/")
def mostrar_tarifas():
    #Cargar los datos desde el JSON
    datos = cargar_datos()

    #Lista para almacenar los resultados de cada envio
    resultados = []

    #Procesar cada envio
    for envio in datos:
        #Obtener el nombre de las ciudades
        nombre_origen = obtener_nombre_ciudad(envio["codigo_ciudad_origen"], tipo="origen")
        nombre_destino = obtener_nombre_ciudad(envio["codigo_ciudad_destino"], tipo="destino")

        # Datos del envio
        data = {
            "codigoCiudadOrigen": envio["codigo_ciudad_origen"],
            "codigoCiudadDestino": envio["codigo_ciudad_destino"],
            "codigoAgenciaDestino": 0,
            "codigoAgenciaOrigen": 0,
            "alto": envio["alto"],
            "ancho": envio["ancho"],
            "largo": envio["largo"],
            "kilos": envio["kilos"],
            "cuentaCorriente": "",
            "cuentaCorrienteDV": "",
            "rutCliente": envio["rut_cliente"]
        }

        # Hacer la solicitud POST para cotizar el envio
        try:
            response = requests.post(API_URL, json=data, headers=API_HEADERS)
            response.raise_for_status()
            respuesta = response.json()
            tarifas = respuesta.get("listaTarifas", [])
        except requests.exceptions.RequestException as err:
            tarifas = [{"error": f"Error en la solicitud: {err}"}]

        # Agregar el resultado a la lista
        resultados.append({
            "id": envio["id"],
            "nombre_origen": nombre_origen,
            "nombre_destino": nombre_destino,
            "tarifas": tarifas
        })

    # Renderizar la página con los resultados
    return render_template("resultados2.html", resultados=resultados)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True) 
