import requests

class City:
    def __init__(self, name, lat, lon, units="imperial"):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.units = units
        self.get_data()

    def get_data(self):
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?units={self.units}&lat={self.lat}&lon={self.lon}&appid=N/A")

        except: 
            print("No internet access.")

        self.response_json = response.json()

        self.temp = self.response_json["main"]["temp"]
        self.temp_min = self.response_json["main"]["temp_min"]
        self.temp_max = self.response_json["main"]["temp_max"]

    def temp_print(self):
        units_symbol = "F"
        if self.units == "metric":
            units_symbol = "C"
        print(f"In {self.name} it is currently {self.temp}° {units_symbol}")
        print(f"Today's High: {self.temp_max}° {units_symbol}")
        print(f"Today's Low: {self.temp_min}° {units_symbol}")

my_city = City("Fort Lauderdale", 26.122438, -80.137314)
my_city.temp_print()

home_city = City("Jacksonville", 30.332184, -81.655647)
home_city.temp_print()
# print(home_city.response_json)
