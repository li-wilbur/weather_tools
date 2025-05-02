from prometheus_client import Gauge,Counter,Summary,start_http_server


real_temp = Gauge('qweather_real_temp',"和风天气实时温度")
requests_counter = Counter('qweather_requests_counter',"API请求次数")
weather_status = Summary('qweather_weather_status',"天气状态")

def start_metrics_server(port):
    start_http_server(port)
    print("metrics server start at port {}".format(port))
