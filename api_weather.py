import requests, json, pycountry, os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

#Ensemble des pays
COUNTRIES = {c.name.lower() for c in pycountry.countries}
COUNTRIES.update({c.alpha_2.lower() for c in pycountry.countries})
COUNTRIES.update({c.alpha_3.lower() for c in pycountry.countries})

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.weatherapi.com/v1/current.json"
PEXELS_KEY = os.getenv("PEXELS_KEY")

def get_weather_info():                                     #Vérification du fonctionnement de l'API
    response = requests.get(API_URL)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data

        
weather_forecast = get_weather_info()
print(json.dumps(weather_forecast, indent=4))

#Flask PAGE 1
app = Flask(__name__)                                       #Route Flask site partie recherche
@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

#Flask PAGE 2 + Data
@app.route("/forecast", methods=["POST"])                   #Route Flask site partie recherche/data
def forecast():
    city = request.form["city"]
    return redirect(url_for("results", city=city))

def fetch_weather(city):                                    #Avoir les données météo de la ville
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    r = requests.get(API_URL, params=params)
    if not r.ok:                           
        return None, r.status_code
    return r.json(), None               

def fetch_city_images(city, n=3):                           #Générer 3 photos en lien avec la ville
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": f'{city} city', "per_page": n, "orientation": "landscape"}
    r = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=5)
    if not r.ok:
        return []                    
    data = r.json()
    return [p["src"]["medium"] for p in data.get("photos", [])]             
    
@app.route("/forecast/<city>", methods=["GET"])             #Route Flask site partie recherche
def results(city):                                          #Vérifier que la ville entré n'est pas un pays + renvoyer les résultats
    if city.lower() in COUNTRIES:
        return redirect(url_for("city_error", city=city, msg=f"{city} is a country not a city"))
    
    data, error  = fetch_weather(city)
    if error:
        return redirect(url_for("forecast_error", code_error=error, city=city))
    
    images = fetch_city_images(city)
    
    temp_c  = data["current"]["temp_c"]
    temp_f  = data["current"]["temp_f"]
    icon  = data["current"]["condition"]["icon"]
    text  = data["current"]["condition"]["text"]
    code = data["current"]["condition"]["code"]
    city_name = data["location"]["name"]
    region_name = data["location"]["region"]
    country_name = data["location"]["country"]
    tz_id = data["location"]["tz_id"]
    localtime = data["location"]["localtime"]
    wind_kph = data["current"]["wind_kph"]
    wind_mph = data["current"]["wind_mph"]
    wind_kt = wind_mph / 1.151
    wind_kt = round(wind_kt,ndigits=1)
    wind_dir = data["current"]["wind_dir"]
    pressure_mb = data["current"]["pressure_mb"]   
    pressure_in = data["current"]["pressure_in"]   
    precip_mm = data["current"]["precip_mm"]   
    precip_in = data["current"]["precip_in"] 
    humidity = data["current"]["humidity"] 
    cloud = data["current"]["cloud"] 
    feelslike_c = data["current"]["feelslike_c"] 
    feelslike_f = data["current"]["feelslike_f"] 
    windchill_c = data["current"]["windchill_c"] 
    windchill_f = data["current"]["windchill_f"] 
    
    return render_template(
        "forecast.html",
        city=city,
        temp_c=temp_c,
        temp_f=temp_f,
        icon=icon,
        text=text,
        code=code,
        city_name=city_name,
        region_name=region_name,
        country_name=country_name,
        tz_id=tz_id,
        localtime=localtime,
        wind_kph = wind_kph,
        wind_mph = wind_mph,
        wind_dir = wind_dir,
        pressure_mb=pressure_mb,
        pressure_in=pressure_in,
        precip_mm=precip_mm,
        precip_in=precip_in,
        humidity=humidity,
        cloud=cloud,
        feelslike_c=feelslike_c,
        feelslike_f=feelslike_f,
        windchill_c=windchill_c,
        windchill_f=windchill_f, 
        wind_kt=wind_kt,
        images=images,
     
    )

   
@app.route("/forecast/error", methods=["GET"])
def forecast_error():                                       #Message erreur mauvaise dactylographie
        code_error = request.args.get("code_error", 500, type=int)
        city = request.args.get("city", "")
        return render_template("error.html", code_error=code_error, city=city), code_error
    
@app.route("/forecast/city_error", methods=["GET"])
def city_error():                                           #Message erreur pays 
    city = request.args.get("city", "")
    return render_template("city_error.html", city=city)
    
    
    
if __name__ == "__main__":
    app.run()

    
#Docu importante icones différents temps (48) : https://www.weatherapi.com/docs/weather_conditions.json


