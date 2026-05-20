import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WeatherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Integer)
    description = db.Column(db.String(100))
    icon = db.Column(db.String(20))


def get_weather(city_name):
    API_KEY = "2fb25f5376fa1929f54ea60aed416d21"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ru"

    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return {
                "city": response["name"],
                "temp": round(response["main"]["temp"]),
                "desc": response["weather"][0]["description"],
                "icon": response["weather"][0]["icon"]
            }
    except Exception as e:
        print(f"Ошибка API: {e}")
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    current_weather = None
    if request.method == 'POST':
        city_name = request.form.get('city')
        if city_name:
            data = get_weather(city_name)
            if data:
                current_weather = data
                # Сохраняем поиск в базу данных
                new_search = WeatherHistory(
                    city=data['city'],
                    temp=data['temp'],
                    description=data['desc'],
                    icon=data['icon']
                )
                db.session.add(new_search)
                db.session.commit()
    history = WeatherHistory.query.order_by(WeatherHistory.id.desc()).limit(5).all()
    return render_template('index.html', weather=current_weather, history=history)


@app.route('/clear')
def clear_history():
    db.session.query(WeatherHistory).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)