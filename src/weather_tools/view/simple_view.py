class SimpleView:
    def __init__(self, view_type='shell'):
        self.view_type = view_type


    def view(self,data):
        """
        显示天气数据的视图方法
        Args:
            data: 包含天气信息的数据字典
        """
        view_type = self.view_type
        print(view_type)  # 打印视图类型

        # 遍历数据源中的值
        for z in zip(data[0].values(),data[1].values()):
            for d in z:
                try:
                    # 尝试打印实时天气数据
                    print('*' * 20)  # 分隔线
                    for k,v in d['now'].items():
                        print(k,v)  # 打印键值对
                    print('*' * 20)  # 分隔线
                except KeyError as e:
                    # 如果没有'now'键,直接打印整个字典
                    print('#' * 20)  # 分隔线
                    for k,v in d.items():
                        print(k,v)  # 打印键值对
                    print('#' * 20)  # 分隔线