import requests
import json
import datetime


class WeatherAPI:
    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-QW-Api-Key': self.api_key,
        }

    def geocode(self, location, geo_range='cn',lang='zh', adm=None):
        if adm is None:
            adm_param = ''  # 如果 adm 为 None，则不添加 adm 参数
        else:
            adm_param = '&adm={}'.format(adm)
        url = '{}/geo/v2/city/lookup?&location={}'.format(self.api_host, location) + '&range={}'.format(
            geo_range) + '&lang={}'.format(lang) + adm_param
        try:
            # 发送 GET 请求
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 检查响应状态码，如果不是 200 会抛出异常
            data = response.json()  # 直接使用 requests 的 json 方法解析响应
            data['location'][0]['elapsed'] = response.elapsed.total_seconds()
            #print(data['location'])
            # print(len(data['location']))
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

    def _make_url(self, api, data, **kwargs):
        """
        根据提供的 API 路径、位置数据和额外参数生成完整的请求 URL。

        :param api: 接口的相对路径，用于拼接完整的请求 URL。
        :param data: 包含位置信息的列表，每个元素是一个字典，至少包含 'id' 键。
        :param kwargs: 可变关键字参数，用于添加到 URL 中的查询参数。
        :return: 一个字典，键为位置 ID，值为包含完整 URL 的位置信息字典。
        """
        # 初始化一个空字典，用于存储每个位置的信息和对应的完整 URL
        location_info = {}
        # 遍历位置数据列表
        for location in data:
            # 拼接完整的请求 URL，将 API 主机地址、API 路径、位置 ID 和额外参数组合在一起
            url = self.api_host + api + location['id'] + '&' + '&'.join("{}={}".format(k, v) for k, v in kwargs.items())
            # 将生成的 URL 添加到当前位置信息字典中
            location['url'] = url
            # 创建一个临时字典，键为位置 ID，值为包含完整 URL 的位置信息字典
            location_single = {
                location['id']: location
            }
            # 将临时字典的内容更新到最终的位置信息字典中
            location_info.update(location_single)
        return location_info

    def _api_request(self, location_info):
        """
        向多个 URL 发送 GET 请求并返回响应数据。

        :param location_info: 一个字典，键为位置 ID，值为包含完整 URL 的位置信息字典。
        :return: 一个字典，键为位置 ID，值为对应的 API 响应数据。
        """
        try:
            # 初始化一个空字典，用于存储每个位置的 API 响应数据
            resp_data = {}
            # 遍历 location_info 中的每个位置信息
            for single_url in location_info.values():
                # 发送 GET 请求并将响应数据解析为 JSON 格式
                resp = requests.get(single_url['url'], headers=self.headers, timeout=10)
                resp_json = resp.json()
                resp_json['elapsed'] = resp.elapsed.total_seconds()
                # 创建一个临时字典，键为位置 ID，值为对应的 API 响应数据
                resp_single = {
                    single_url['id']: resp_json
                    #single_url['elapsed']: resp.elapsed.total_seconds()
                }
                #print(resp_single)
                #print(resp.elapsed.total_seconds())
                # 将临时字典的内容更新到最终的响应数据字典中
                resp_data.update(resp_single)
            return resp_data
        except requests.RequestException as e:
            # 处理请求过程中发生的异常，如网络错误、超时等
            raise Exception(f'请求发生错误: {e}')
        except Exception as e:
            # 处理其他未知异常
            raise Exception(f'发生未知错误: {e}')

    def real_time_weather(self, location, lang='zh', unit='m', geo_range='cn', adm=None):
        """
        获取指定位置的实时天气信息。

        :param location: 要查询天气的位置信息，可以是城市名称、经纬度等。
        :param lang: 返回数据的语言，默认为中文 'zh'。
        :param unit: 温度单位，默认为公制 'm'。
        :param geo_range: 地理范围，默认为中国 'cn'。
        :param adm: 行政区划信息，默认为 None。
        :return: 一个字典，键为位置 ID，值为对应的实时天气 API 响应数据。
        """
        # 调用 geocode 方法，将输入的位置信息转换为地理编码数据
        geo_data = self.geocode(location, lang=lang, geo_range=geo_range, adm=adm)
        # 调用 make_url 方法，根据地理编码数据和 API 路径生成完整的请求 URL
        # 调用 api_request 方法，向生成的 URL 发送请求并获取响应数据
        location_info = self._make_url(api='/v7/weather/now?&location=', data=geo_data)
        resp_data = self._api_request(location_info)
        return resp_data,location_info

    def history_weather(self, location, date, lang='zh', unit='m', geo_range='cn', adm=None):
        """
        获取指定位置的历史天气数据。

        :param location: 要查询天气的位置信息，可以是城市名称、经纬度等
        :param date: 要查询的历史日期，以天为单位的整数，表示距今天的天数
        :param lang: 返回数据的语言，默认为中文 'zh'
        :param unit: 温度单位，默认为公制 'm'
        :param geo_range: 地理范围，默认为中国 'cn'
        :param adm: 行政区划信息，默认为 None
        :return: 一个字典，键为位置 ID，值为对应的历史天气 API 响应数据
        """
        # 将输入的天数转换为具体的日期格式(YYYYMMDD)
        date = (datetime.date.today() -
                datetime.timedelta(days=date)).strftime("%Y%m%d")
        # 调用 geocode 方法获取地理编码数据
        geo_data = self.geocode(location, lang=lang, geo_range=geo_range, adm=adm)
        # 生成历史天气API的请求URL
        location_info = self._make_url(api='/v7/historical/weather?&location=', data=geo_data, date=date)
        # 发送API请求并获取响应数据
        resp_data = self._api_request(location_info)
        return resp_data,location_info

