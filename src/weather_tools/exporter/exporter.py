from prometheus_client import Gauge,Counter,Summary,start_http_server


real_temp = Gauge('qweather_real_temp',"和风天气实时温度")
requests_counter = Counter('qweather_requests_counter',"API请求次数")
weather_status = Summary('qweather_weather_status',"天气状态")


if __name__ == '__main__':
    start_http_server(8000)
