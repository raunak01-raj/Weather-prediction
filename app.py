from flask import Flask , render_template, request
import pickle
from datetime import datetime
import pandas as pd



app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

prophet_model = pickle.load(open('prophet.pkl', 'rb'))


@app.route("/")
def hello():
    return render_template("index(ml).html")

<<<<<<< HEAD
@app.route("/first", methods = ['GET','POST'])
def first():
=======
@app.route("/predict", methods = ['GET','POST'])
<<<<<<< HEAD
=======


>>>>>>> 500e6db0b4cc5b9c12a4f9a9ec275135094deff0
def predict():
>>>>>>> ff011ae75bd4fa9cc9a10261d7bc6c4d6a1c2d10
    wind_kph = request.form.get('wind_kph')
    pressure_in = request.form.get('pressure_in')
    precip_mm = request.form.get('precip_mm')
    humidity = request.form.get('humidity')
    air_quality_Nitrogen_dioxide = request.form.get('air_quality_Nitrogen_dioxide')
    feels_like_celsius = request.form.get('feels_like_celsius')


    try:
        wind_kph = float(wind_kph)
        pressure_in = float(pressure_in)
        precip_mm = float(precip_mm)
        humidity = float(humidity)
        air_quality_Nitrogen_dioxide = float(air_quality_Nitrogen_dioxide)
        feels_like_celsius = float(feels_like_celsius)

    except ValueError:
        # Handle potential conversion errors (e.g., user entering non-numeric data)
        return render_template("index(ml).html", error="Invalid form data")

    prediction = model.predict([[wind_kph, pressure_in, precip_mm, humidity, air_quality_Nitrogen_dioxide, feels_like_celsius ]])
    output = round(prediction[0], 2)

    return render_template("index(ml).html" , prediction_text=f'Temperature predicted in degree C is {output} ')


@app.route("/second", methods=['GET', 'POST'])
def second():
    if request.method == 'POST':
        location = request.form.get('city')
        date_time = request.form.get('datetime')
        try:
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
            
        except ValueError:
            return render_template("index(fb).html", error="Invalid date and time format. Please enter YYYY-MM-DDTHH:MM.")

        # Convert to DataFrame
        user_date = date_time.date()
        prediction_date = pd.DataFrame({'ds': [user_date]})

        # Make the prediction
        one_day_forecast = prophet_model.predict(prediction_date)
        predicted_temp = one_day_forecast["yhat"].values[0]

        return render_template("index(fb).html", pred_text=f'Temperature predicted in degree C is {predicted_temp:.2f}')
    return render_template("index(fb).html")



if __name__ == '__main__':
    app.run(debug=True)





