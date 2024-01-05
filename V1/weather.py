import requests
import json
url_c = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd:&lang=tc"
response = requests.get(url_c).text

new_dict = json.loads(response)

print(response, file=open("test.json5", "a"))

def getForecast(dayNum, attribute):
    if attribute == '':
        return new_dict.get("weatherForecast")[dayNum]
    else:
        return new_dict.get("weatherForecast")[dayNum].get(attribute)

def getGeneralSituation():
    return new_dict.get("generalSituation")

print(getGeneralSituation())
print(getForecast(0, "week"))