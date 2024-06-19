from flask import Flask , render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))


@app.route("/")
def hello():
    return render_template("index(ml).html")

@app.route("/predict", methods = ['GET','POST'])


def predict():
    wind_kph = request.form.get('wind_kph')
    pressure_in = request.form.get('pressure_in')
    precip_mm = request.form.get('precip_mm')
    humidity = request.form.get('humidity')
    air_quality_Nitrogen_dioxide = request.form.get('air_quality_Nitrogen_dioxide')

    try:
        wind_kph = float(wind_kph)
        pressure_in = float(pressure_in)
        precip_mm = float(precip_mm)
        humidity = float(humidity)
        air_quality_Nitrogen_dioxide = float(air_quality_Nitrogen_dioxide)
    except ValueError:
        # Handle potential conversion errors (e.g., user entering non-numeric data)
        return render_template("index(ml).html", error="Invalid form data")

    prediction = model.predict([[wind_kph, pressure_in, precip_mm, humidity, air_quality_Nitrogen_dioxide ]])
    output = round(prediction[0], 2)
    return render_template("index(ml).html" , prediction_text=f'Temperature predicted in degree C is {output} ')


if __name__ == "__main__":
    app.run(debug=True)



