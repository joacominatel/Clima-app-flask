from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'API'  # API Key gratuita en https://openweathermap.org/appid

def obtener_clima(ciudad, pais):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if 'main' in data:
        temp = data['main'].get('temp', 'Desconocido')
        humidity = data['main'].get('humidity', 'Desconocido')
    else:
        temp = 'Desconocido'
        humidity = 'Desconocido'

    wind_speed = data.get('wind', {}).get('speed', 'Desconocido')
    wind_direction = data.get('wind', {}).get('deg', 'Desconocido')

    weather = data.get('weather', [{}])[0].get('main', 'Desconocido')

    return {
        'weather': weather,
        'temp': temp,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'humidity': humidity,
        'weather_class': get_weather_class(weather)
    }


def get_weather_class(weather):
    if weather == 'Clear':
        return 'sunny'
    elif weather == 'Clouds':
        return 'cloudy'
    elif weather == 'Rain':
        return 'rainy'
    else:
        return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        country = request.form['country']
        weather_data = obtener_clima(city, country)
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)