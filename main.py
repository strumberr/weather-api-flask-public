import requests
import geopy
from geopy.geocoders import Nominatim
import json
import schedule
import time
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os
url_mail = os.environ['url_mail']
api_mail = os.environ['api_mail']
openweathermap_key = os.environ['openweathermap_key']
tomorrow_key = os.environ['tomorrow_key']
app = Flask(__name__)


@app.route('/') # Route the Function
def main(): # Run the function
    print("Your schedule is running!")
    return "<p>Website Running!</p>"




def send_simple_message(today_temp, today_weather2, today_humidity, today_rain, today_uv_health_concern, today_weather, current_temp, current_air_quality, current_fire):
    return requests.post(
        url_mail,
        auth=("api", api_mail),
        data={"from": "Aboutoday <code.bot.guy@gmail.com>",
            "to": "storm <code.bot.guy@gmail.com>",
            "subject": "Today!",
            "text": today_temp + "\n" + today_weather2 + "\n" + today_humidity + "\n" + today_rain + "\n" + today_uv_health_concern + "\n" + today_weather + "\n" + current_temp + "\n" + current_air_quality + "\n" + current_fire})


def send_simple_message2(subject, message):
    return requests.post(
        url_mail,
        auth=("api", api_mail),
        data={"from": "Aboutoday <code.bot.guy@gmail.com>",
            "to": "storm <code.bot.guy@gmail.com>",
            "subject": subject,
            "text": message})


# Tom´s comment

#input_address = input("Input address: \n")
#address=input_address
#geolocator = Nominatim(user_agent="Your_Name")
#location = geolocator.geocode(address)
#print(location.address)
#LAA = ((location.latitude, location.longitude))
#LAA2 = str(LAA)
#remove = LAA2.replace(')', '')
#remove2 = remove.replace('(', '')
#print(remove2)


def func_temp():
    url = "https://api.tomorrow.io/v4/timelines"

    querystring = {
    "location":"41.417, 1.9197",
    "fields":["temperature", "cloudCover", "humidity", "precipitationProbability", "uvHealthConcern", "weatherCodeDay", "fireIndex"],
    "units":"metric",
    "timesteps":"1d",
    "apikey":tomorrow_key}

    response = requests.request("GET", url, params=querystring)

    try:
        results = response.json()['data']['timelines'][0]['intervals']
    except:
        print("-----An error has occurred while getting the data. Please try again later.------")




    temp = round(results[0]['values']['temperature'])
    
    temp_to_string = str(temp)
    final_output = (" - Today's temperature", "will be", temp_to_string, "degrees celsius\n")
    join_final = " ".join(final_output)




    #humidity = round(results[0]['values']['humidity'])

    #humidity_to_string = str(humidity)
    #final_output2 = (" - Today's humidity will be", humidity_to_string, "%\n")
    #join_final2 = " ".join(final_output2)
    #print(str(final_output2))



    rain = round(results[0]['values']['precipitationProbability'])

    rain_to_string = str(rain)
    final_output3 = (" - Today's chance of rain is", rain_to_string, "%\n")
    join_final3 = " ".join(final_output3)

    rain_to_int = int(rain)
    if rain_to_int >= 80:
        send_simple_message2("It's going to rain today!", "It's going to rain today!! (" + rain_to_int + "%)")



    uv_health_concern = round(results[0]['values']['uvHealthConcern'])

    uvhc_to_string = str(uv_health_concern)
    final_output4 = (" - Today's UV light is", uvhc_to_string, """
    0-2: Low
    3-5: Moderate
    6-7: High
    8-10: Very High
    11+: Extreme\n""")
    join_final4 = " ".join(final_output4)





    wc_health_concern = round(results[0]['values']['weatherCodeDay'])

    weather_code_to_string = str(wc_health_concern)
    final_output5 = (" - Today's wheather is", weather_code_to_string, "\n")
    join_final5 = " ".join(final_output5)




    weather_codes =  '''{
        "0": "Unknown",
    "10000": "Clear, Sunny",
    "11000": "Mostly Clear",
    "11010": "Partly Cloudy",
    "11020": "Mostly Cloudy",
    "10010": "Cloudy",
    "11030": "Partly Cloudy and Mostly Clear",
    "21000": "Light Fog",
    "21010": "Mostly Clear and Light Fog",
    "21020": "Partly Cloudy and Light Fog",
    "21030": "Mostly Cloudy and Light Fog",
    "21060": "Mostly Clear and Fog",
    "21070": "Partly Cloudy and Fog",
    "21080": "Mostly Cloudy and Fog",
    "20000": "Fog",
    "42040": "Partly Cloudy and Drizzle",
    "42030": "Mostly Clear and Drizzle",
    "42050": "Mostly Cloudy and Drizzle",
    "40000": "Drizzle",
    "42000": "Light Rain",
    "42090": "Mostly Clear and Rain",
    "42080": "Partly Cloudy and Rain",
    "42100": "Mostly Cloudy and Rain",
    "40010": "Rain",
    "42110": "Mostly Clear and Heavy Rain",
    "42020": "Partly Cloudy and Heavy Rain",
    "42120": "Mostly Cloudy and Heavy Rain",
    "42010": "Heavy Rain",
    "51150": "Mostly Clear and Flurries",
    "51160": "Partly Cloudy and Flurries",
    "51170": "Mostly Cloudy and Flurries",
    "50010": "Flurries",
    "51000": "Light Snow",
    "51020": "Mostly Clear and Light Snow",
    "51030": "Partly Cloudy and Light Snow",
    "51040": "Mostly Cloudy and Light Snow",
    "51220": "Drizzle and Light Snow",
    "51050": "Mostly Clear and Snow",
    "51060": "Partly Cloudy and Snow",
    "51070": "Mostly Cloudy and Snow",
    "50000": "Snow",
    "51010": "Heavy Snow",
    "51100": "Drizzle and Snow",
    "51080": "Rain and Snow",
    "51140": "Snow and Freezing Rain",
    "51120": "Snow and Ice Pellets",
    "60000": "Freezing Drizzle",
    "60030": "Mostly Clear and Freezing drizzle",
    "60020": "Partly Cloudy and Freezing drizzle",
    "60040": "Mostly Cloudy and Freezing drizzle",
    "62040": "Drizzle and Freezing Drizzle",
    "62060": "Light Rain and Freezing Drizzle",
    "62050": "Mostly Clear and Light Freezing Rain",
    "62030": "Partly Cloudy and Light Freezing Rain",
    "62090": "Mostly Cloudy and Light Freezing Rain",
    "62000": "Light Freezing Rain",
    "62130": "Mostly Clear and Freezing Rain",
    "62140": "Partly Cloudy and Freezing Rain",
    "62150": "Mostly Cloudy and Freezing Rain",
    "60010": "Freezing Rain",
    "62120": "Drizzle and Freezing Rain",
    "62200": "Light Rain and Freezing Rain",
    "62220": "Rain and Freezing Rain",
    "62070": "Mostly Clear and Heavy Freezing Rain",
    "62020": "Partly Cloudy and Heavy Freezing Rain",
    "62080": "Mostly Cloudy and Heavy Freezing Rain",
    "62010": "Heavy Freezing Rain",
    "71100": "Mostly Clear and Light Ice Pellets",
    "71110": "Partly Cloudy and Light Ice Pellets",
    "71120": "Mostly Cloudy and Light Ice Pellets",
    "71020": "Light Ice Pellets",
    "71080": "Mostly Clear and Ice Pellets",
    "71070": "Partly Cloudy and Ice Pellets",
    "71090": "Mostly Cloudy and Ice Pellets",
    "70000": "Ice Pellets",
    "71050": "Drizzle and Ice Pellets",
    "71060": "Freezing Rain and Ice Pellets",
    "71150": "Light Rain and Ice Pellets",
    "71170": "Rain and Ice Pellets",
    "71030": "Freezing Rain and Heavy Ice Pellets",
    "71130": "Mostly Clear and Heavy Ice Pellets",
    "71140": "Partly Cloudy and Heavy Ice Pellets",
    "71160": "Mostly Cloudy and Heavy Ice Pellets",
    "71010": "Heavy Ice Pellets",
    "80010": "Mostly Clear and Thunderstorm",
    "80030": "Partly Cloudy and Thunderstorm",
    "80020": "Mostly Cloudy and Thunderstorm",
    "80000": "Thunderstorm"}'''

    weather_codes2 = json.loads(weather_codes)

    if weather_code_to_string in weather_codes2:
        join_final66 = weather_codes2.get(weather_code_to_string)
        join_final6 = " - 1st source: Today it will be " + join_final66 + "!\n"


    
    fire = round(results[0]['values']['fireIndex'])
    
    fire_to_string = str(fire)
    phrase_format = ("Today's fire risk: ", fire_to_string, """
    very low (0.0 – 5.2)
    low (5.2 – 11.2)
    moderate (11.2 – 21.3)
    high (21.3 – 38.0)
    very high (38.0 – 50.0)
    extreme (50.0 – 100.0)""")
    join_final11 = " ".join(phrase_format)

    




    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = "corbera de llobregat"
    API_KEY = openweathermap_key
    # updating the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the requesttt
    if response.status_code == 200:
    # getting data in the json format
        data = response.json()

    # getting the main dict block
        main = data['main']
    # getting temperature
        temperature = main['temp']
        temperature2 = str(temperature)
        temperature3 = float(temperature2)
        temperature4 = temperature3 - 273.15
        temperature5 = round(temperature4)
        temperature6 = str(temperature5)
        join_final8 = " - The current temperature is " + temperature6 + " degrees celsius\n"
    # getting the humidity
        humidity = main['humidity']
        humidity2 = str(humidity)
        join_final2 = " - The current humidity is " + humidity2 + "%\n"
    # getting the pressure
        pressure = main['pressure']
    # weather report
        report = data['weather']
        report2 = report[0]['description']
        report3 = str(report2)
        join_final9 = " - 2nd source:" + " Today there/it will be " + report3 + "\n"

    else:
    # showing the error message
        print("Error in the HTTP request")



    BASE_URL2 = "http://api.openweathermap.org/data/2.5/air_pollution?"
    URL2 = BASE_URL2 + "lat=" + "41.4202" + "&lon=" + "1.9246" + "&appid=" + API_KEY
    # HTTP request
    response2 = requests.get(URL2)
    # checking the status code of the request
    if response2.status_code == 200:
    # getting data in the json format
        data2 = response2.json()

    # getting the main dict block
        data2_to_string = str(data2)
        data2_to_string2 = data2_to_string.split()
        data2_to_string3 = data2_to_string2[8]
        data2_to_string4 = data2_to_string3.replace("}", "")
        data2_to_string5 = data2_to_string4.replace(",", "")
        join_final10 = "The current Air Quality (AQI) is " + data2_to_string5 + """
        1 = Good
        2 = Fair
        3 = Moderate
        4 = Poor
        5 = Very Poor\n"""
        print("14400 seconds until next run")









    send_simple_message(join_final6, join_final9, join_final, join_final2, join_final3, join_final4, join_final8, join_final10, join_final11)

scheduler = BackgroundScheduler(timezone="Europe/Madrid")
scheduler.add_job(func=func_temp, trigger="interval", seconds=14400)
scheduler.start()






def fire_checker():
    url = "https://api.tomorrow.io/v4/timelines"

    querystring = {
    "location":"41.417, 1.9197",
    "fields":["fireIndex", "precipitationProbability"],
    "units":"metric",
    "timesteps":"1d",
    "apikey":tomorrow_key}

    response = requests.request("GET", url, params=querystring)

    try:
        results = response.json()['data']['timelines'][0]['intervals']
    except:
        print("-----An error has occurred while getting the data. Please try again later.------")


    fire = round(results[0]['values']['fireIndex'])
    if fire >= 30:
        fire_to_string = str(fire)
        fire_final = "Today, there's a high risk of fires near your home!" + "(" + fire_to_string + ")" + """
        very low (0.0 – 5.2)
        low (5.2 – 11.2)
        moderate (11.2 – 21.3)
        high (21.3 – 38.0)
        very high (38.0 – 50.0)
        extreme (50.0 – 100.0)"""
        send_simple_message2("High fire risk today!", fire_final)

    
    rain = round(results[0]['values']['precipitationProbability'])

    rain_to_string = str(rain)
    final_output3 = (" - Today's chance of rain is", rain_to_string, "%\n")
    join_final3 = " ".join(final_output3)

    rain_to_int = int(rain)
    if rain_to_int >= 80:
        send_simple_message2("It's going to rain today!", "It's going to rain today!! (" + rain_to_int + "%)")



scheduler = BackgroundScheduler(timezone="Europe/Madrid")
scheduler.add_job(func=fire_checker, trigger="interval", seconds=7200)
scheduler.start()







func_temp()
fire_checker()






app.run(host='0.0.0.0', port=5100, debug=True) # Run the Application (in debug mode)