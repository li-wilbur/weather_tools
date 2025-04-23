import pandas as pd
from pathlib import Path


class DataStorage:
    def __init__(self, storage_type: str = 'csv'):
        self.storage_type = storage_type.lower()
        self._storage_type_check(self.storage_type)

    def _storage_type_check(self, storage_type):
        if storage_type not in ['csv', 'sqlite']:
            raise ValueError('storage_type must be csv or sqlite')

    @staticmethod
    def save_csv(data: list, path: str = None):
        # 如果未指定路径,使用默认路径
        if path is None:
            # 获取项目根目录下的dist文件夹
            root_dir = Path(__file__).resolve().parent.parent.parent.parent.joinpath('dist')
            # 如果dist目录不存在则创建
            if not root_dir.exists():
                root_dir.mkdir(parents=True, exist_ok=True)
            csv_file = root_dir.joinpath('weather.csv')
        else:
            csv_file = Path(path)
            # 确保父目录存在
            csv_file.parent.mkdir(parents=True, exist_ok=True)

        # 将数据转换为DataFrame并追加到CSV文件
        df = pd.DataFrame([data])
        df.to_csv(
            csv_file,
            mode='a',
            header=not csv_file.exists(),
            index=False
        )
