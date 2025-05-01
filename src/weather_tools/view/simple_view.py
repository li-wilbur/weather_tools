class SimpleView:
    def __init__(self, view_type):
        self.view_type = view_type

    @staticmethod
    def _city_view(data):
        # print(data)
        print('城市名称: {}'.format(data['name']))
        print('城市ID: {}'.format(data['id']))
        print('纬度: {}'.format(data['lat']))
        print('经度: {}'.format(data['lon']))
        print('所属省份: {}'.format(data['adm1']))
        print('所属城市: {}'.format(data['adm2']))
        print('时区: {}'.format(data['tz']))
        print('天气类型: {}'.format(data['type']))
        print('天气链接: {}'.format(data['fxLink']))
        print('*' * 100)

    def simple_view(self, data, weather_type):
        if weather_type == 'real_time':
            return self.real_time_view(data)
        elif weather_type == 'history':
            return self.history_view(data)
        else:
            return None

    def real_time_view(self, data):
        for d in data:
            for v in d.values():
                try:
                    # print(v)
                    now = v['now']
                    print('*' * 100)
                    print('时间: {}'.format(now['obsTime']))
                    print('温度: {}°'.format(now['temp']))
                    print('体感温度: {}°'.format(now['feelsLike']))
                    print('天气状况: {}'.format(now['text']))
                    print('风向: {}'.format(now['windDir']))
                    print('风力: {}'.format(now['windScale']))
                    print('风速: {}km/h'.format(now['windSpeed']))
                    print('相对湿度: {}%'.format(now['humidity']))
                    print('降水量: {}mm'.format(now['precip']))
                    print('气压: {}hPa'.format(now['pressure']))
                    print('能见度: {}km'.format(now['vis']))
                    print('云量: {}%'.format(now['cloud']))

                except KeyError:
                    self._city_view(v)

    def history_view(self, data):
        for d in data:
            for v in d.values():
                try:
                    weather_daily = v['weatherDaily']
                    print('*' * 100)
                    print('时间: {}'.format(weather_daily['date']))
                    print('最高温: {}'.format(weather_daily['tempMax']))
                    print('最低温: {}'.format(weather_daily['tempMin']))
                    print('相对湿度: {}%'.format(weather_daily['humidity']))
                    print('降水量: {}mm'.format(weather_daily['precip']))
                    weather_hourly = v['weatherHourly']
                    for h in weather_hourly:
                        print(h)

                except KeyError:
                    self._city_view(v)
