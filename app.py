from flask import Flask, render_template, request
import requests
from config import API_URL, API_HEADERS

app = Flask(__name__)


# Función para obtener el nombre de la ciudad
def obtener_nombre_ciudad(codigo_ciudad, tipo="origen"):
    url = (
        "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesOrigen"
        if tipo == "origen"
        else "https://restservices-qa.starken.cl/apiqa/starkenservices/rest/listarCiudadesDestino"
    )

    try:
        response = requests.get(url, headers=API_HEADERS)
        response.raise_for_status()

        # Convertir la respuesta a JSON
        respuesta = response.json()

        # Depuración: Imprimir la respuesta completa
        print(f"Respuesta de la API ({tipo}):", respuesta)

        # Verificar si la respuesta tiene la estructura esperada
        if "listaCiudadesOrigen" in respuesta:
            ciudades = respuesta["listaCiudadesOrigen"]
        elif "listaCiudadesDestino" in respuesta:
            ciudades = respuesta["listaCiudadesDestino"]
        else:
            return "Ciudad no encontrada"
        
        # Depuración: Imprimir la lista de ciudades
        print(f"Lista de ciudades ({tipo}):", ciudades)
        

        # Buscar la ciudad por su código
        for ciudad in ciudades:
            if ciudad["codigoCiudad"] == codigo_ciudad:
                return ciudad["nombreCiudad"]
            # Si no encuentra la ciudad
        return "Ciudad no encontrada"
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

# Ruta principal (formulario)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        codigo_ciudad_origen = int(request.form["codigo_ciudad_origen"])
        codigo_ciudad_destino = int(request.form["codigo_ciudad_destino"])
        alto = float(request.form["alto"])
        ancho = float(request.form["ancho"])
        largo = float(request.form["largo"])
        # peso = float(request.form["peso"])
        kilos = float(request.form["kilos"])
        rut_cliente = request.form["rut_cliente"]
        
        # Obtener nombres de las ciudades
        nombre_origen = obtener_nombre_ciudad(codigo_ciudad_origen, tipo="origen")
        nombre_destino = obtener_nombre_ciudad(codigo_ciudad_destino, tipo="destino")

        # Datos del envio
        data = {
            "codigoCiudadOrigen": codigo_ciudad_origen,
            "codigoCiudadDestino": codigo_ciudad_destino,
            "codigoAgenciaDestino": 0,
            "codigoAgenciaOrigen": 0,
            "alto": alto,
            "ancho": ancho,
            "largo": largo,
            "kilos": kilos,
            "cuentaCorriente": "",
            "cuentaCorrienteDV": "",
            "rutCliente": rut_cliente,
        }

        # Hacer la solicitud POST para cotizar el envio
        try:
            response = requests.post(API_URL, json=data, headers=API_HEADERS)
            response.raise_for_status()
            respuesta = response.json()
            tarifas = respuesta.get("listaTarifas",[])
        except requests.exceptions.RequestException as err:
            return f"Error en la solicitud: {err}"
        
        # Renderizar la página de resultados
        return render_template(
            "resultado.html",
            nombre_origen=nombre_origen,
            nombre_destino=nombre_destino,
            tarifas=tarifas
        )
    
    # Si es una solicitud GET, mostrar el formulario
    return render_template("index.html")

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
