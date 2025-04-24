from ..api.weather_api import WeatherAPI

class SimpleView:
    def __init__(self, data):
        self.data = data

    def view(self):
        print(self.data)


if __name__ == '__main__':
    pass