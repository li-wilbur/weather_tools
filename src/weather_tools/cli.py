import argparse
import os
from dotenv import load_dotenv
from api.weather_api import WeatherAPI

# Load environment variables from.env file
load_dotenv()
api_host = os.getenv('api_host')
api_key = os.getenv('api_key')


def init_args():
    parser = argparse.ArgumentParser(description='Weather API Client')
    #parser.add_argument('-l','--location', type=str,required=True, help='Location name')
    parser.add_argument('-l','--location', type=str, default='nanshan', help='Location name')
    parser.add_argument('-r','--range', type=str, default='cn', help='Range of locations')
    parser.add_argument('-a','--adm', type=str, default='shenzhen', help='The superior administrative division of a city')
    parser.add_argument('-u','--unit', type=str, default='m', help='Unit of measurement')
    parser.add_argument('-L','--lang', type=str, default='zh', help='Language')
    return parser.parse_args()

if __name__ == '__main__':
    args = init_args()
    api = WeatherAPI(api_host, api_key)
    rtw = api.real_time_weather(args.location, lang=args.lang, unit=args.unit, range=args.range, adm=args.adm)
    for l in rtw:
        for k,v in l['now'].items():
            print(k,':',v)