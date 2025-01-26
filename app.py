from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Sustituye con tu clave de API de WeatherAPI
API_KEY = "7a29880691ab473287b181141252601"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    """Obtener clima y mostrar resultados"""
    city = request.form.get('city')

    if not city:
        return render_template('error.html', message="Por favor, ingresa el nombre de una ciudad.")

    # Hacer solicitud a la API de WeatherAPI para obtener el clima de la ciudad
    url = f"{WEATHER_API_URL}?key={API_KEY}&q={city}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto generará una excepción si la respuesta es un error (código 4xx o 5xx)
        data = response.json()

        if "error" in data:
            return render_template('error.html', message=f"No se encontró información para la ciudad: {city}.")

        # Extraemos la información del clima
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']

        return render_template('result.html', city=city, temperature=temperature, description=description, humidity=humidity)

    except requests.exceptions.RequestException as e:
        # Si ocurre cualquier error en la solicitud, mostramos un mensaje genérico
        return render_template('error.html', message="Hubo un error al conectar con WeatherAPI. Intenta más tarde.")
    except Exception as e:
        # Si ocurre un error inesperado, lo mostramos en un mensaje
        return render_template('error.html', message=f"Ocurrió un error inesperado: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
