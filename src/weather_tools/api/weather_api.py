import requests
import json

class WeatherAPI:
    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-QW-Api-Key': self.api_key,
        }
    
    def geocode(self, location,range='cn', lang='zh',adm=None):
        if adm is None:
            adm_param = '' # 如果 adm 为 None，则不添加 adm 参数
        else:
            adm_param = '&adm={}'.format(adm)
        url = '{}/geo/v2/city/lookup?'.format(self.api_host) + '&location={}'.format(location) + '&range={}'.format(range) + '&lang={}'.format(lang) + adm_param
        #print(url)
        try:
            # 发送 GET 请求
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查响应状态码，如果不是 200 会抛出异常
            data = response.json()  # 直接使用 requests 的 json 方法解析响应
            #print(len(data['location']))
            return data['location']
        except requests.RequestException as e:
            # 处理请求异常
            raise Exception(f'请求发生错误: {e}')
        except (KeyError, IndexError):
            # 处理响应数据格式异常
            raise Exception('响应数据格式不符合预期，无法获取位置 ID')
        except Exception as e:
            # 处理其他异常
            raise Exception(f'发生未知错误: {e}')

    def real_time_weather(self, location, lang='zh', unit='m',range='cn',adm=None):
        urls = []
        for location in self.geocode(location,lang=lang,range=range,adm=adm,):
            location_code = location['id']
            url = '{}/v7/weather/now?'.format(self.api_host) + '&location={}'.format(location_code) + '&lang={}'.format(lang) + '&unit={}'.format(unit)
            urls.append(url)
        try:
            # 发送 GET 请求
            responses = [requests.get(url, headers=self.headers, timeout=10) for url in urls]
            #responses.raise_for_status()  # 检查响应状态码，如果不是 200 会抛出异常
            data = [response.json() for response in responses]  # 直接使用 requests 的 json 方法解析响应
            return data
        except requests.RequestException as e:
            # 处理请求异常
            raise Exception(f'请求发生错误: {e}')
