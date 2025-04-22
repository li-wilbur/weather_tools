import argparse
import os
from dotenv import load_dotenv
from api.weather_api import WeatherAPI
from data.storages import DataStorage

# Load environment variables from.env file
load_dotenv()
api_host = os.getenv('api_host')
api_key = os.getenv('api_key')
if api_host is None or api_key is None:
    raise ValueError("API host or key not found in environment variables")


def init_args():
    parser = argparse.ArgumentParser(description='Weather API Client')
    # parser.add_argument('-l','--location', type=str,required=True, help='Location name')
    parser.add_argument('-l', '--location', type=str,
                        default='nanshan', help='Location name')
    parser.add_argument('-r', '--range', type=str,
                        default='cn', help='Range of locations')
    parser.add_argument('-a', '--adm', type=str, default='shenzhen',
                        help='The superior administrative division of a city')
    parser.add_argument('-u', '--unit', type=str,
                        default='m', help='Unit of measurement')
    parser.add_argument('-L', '--lang', type=str,
                        default='zh', help='Language')
    parser.add_argument('-d', '--date', type=int, default=1,
                        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9], help='show history weather')
    return parser.parse_args()


if __name__ == '__main__':
    args = init_args()
    api = WeatherAPI(api_host, api_key)
    storage_tool = DataStorage('csv')
    rtw = api.real_time_weather(
        args.location, lang=args.lang, unit=args.unit, range=args.range, adm=args.adm)
    for l in rtw:
        for k, v in l['now'].items():
            print(k, ':', v)
    test = api.history_weather(args.location, date=args.date,
                               lang=args.lang, unit=args.unit, range=args.range, adm=args.adm)
    print(test)
    for l in test:
        for weatherHourly in l['weatherHourly']:
            #storage_tool.save_csv(weatherHourly)
            print(weatherHourly)
