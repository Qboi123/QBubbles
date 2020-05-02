# import required modules
import requests

# Enter your API key here
API_KEY = "ae0b207ae9b9b71f313481e733b8b912"


class TempKelvin(object):
    def __init__(self, kelvin):
        self._temp = kelvin

    def celsius(self):
        return self._temp - 272.15

    def kelvin(self):
        return self._temp

    def fahrenheit(self):
        return self._temp * 9 / 5 - 459.67


class TempCelsius(object):
    def __init__(self, kelvin):
        self._temp = kelvin

    def celsius(self):
        return self._temp

    def kelvin(self):
        return self._temp + 272.15

    def fahrenheit(self):
        return self._temp * 9 / 5 + 32


class TempFahrenheit(object):
    def __init__(self, kelvin):
        self._temp = kelvin

    def celsius(self):
        return (self._temp - 32) * 5/9

    def kelvin(self):
        return (self._temp + 459.67) * 5/9

    def fahrenheit(self):
        return self._temp


# Python program to find current
# weather details of any city
# using openweathermap api

# base_url variable to store url
base_url = "https://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "q=" + city_name + "&APPID=" + API_KEY

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
print(x)
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = TempKelvin(y["temp"])

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidiy = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    # print following values
    print(" Temperature (in celsius unit) = " +
          str(current_temperature.celsius()) +
          "\n atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n humidity (in percentage) = " +
          str(current_humidiy) +
          "\n description = " +
          str(weather_description))

else:
    print(" City Not Found ")
