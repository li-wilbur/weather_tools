class SimpleView:
    def __init__(self, view_type='shell'):
        self.view_type = view_type


    def real_time_view(self,data):
        """
        显示天气数据的视图方法
        Args:
            data: 包含天气信息的数据字典
        """
        view_type = self.view_type
        print(view_type)  # 打印视图类型

        # 遍历数据源中的值
        for data_zip in zip(data[0].values(),data[1].values()):
            print('#' * 20)
            for single_data in data_zip:
                try:
                    # 尝试打印实时天气数据
                    for k,v in single_data['now'].items():
                        print(k,v)  # 打印键值对
                except KeyError:
                    # 如果没有'now'键,直接打印整个字典
                    for k,v in single_data.items():
                        print(k,v)  # 打印键值对

    def history_view(self,data):
        """
        显示历史天气数据的视图方法
        Args:
            data: 包含历史天气信息的数据字典,包括每日天气和逐小时天气数据
        """
        view_type = self.view_type
        print(view_type)  # 打印视图类型

        # 遍历数据源中的值
        for data_zip in zip(data[0].values(),data[1].values()):
            print('#' * 20)
            for single_data in data_zip:
                try:
                    # 打印每日天气数据
                    for k,v in single_data['weatherDaily'].items():
                        print(k,v)  # 打印每日天气的键值对
                    # 打印逐小时天气数据
                    for hourly_data in single_data['weatherHourly']:
                        print(hourly_data)  # 打印每小时天气数据
                except KeyError:
                    # 如果数据结构不符合预期,直接打印整个字典
                    for k,v in single_data.items():
                        print(k,v)  # 打印键值对