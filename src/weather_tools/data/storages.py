import pandas as pd
from pathlib import Path


class DataStorage:
    def __init__(self, storage_type: str = 'csv'):
        self.storage_type = storage_type.lower()
        self._storage_type_check(self.storage_type)

    def _storage_type_check(self, storage_type):
        if storage_type not in ['csv', 'sqlite']:
            raise ValueError('storage_type must be csv or sqlite')

    def save_csv(self, data: list,path: str = None):
        if path is None:
            root_dir = Path(__file__).resolve(
            ).parent.parent.parent.parent.joinpath('dist')
            if root_dir.exists():
                csv_file = root_dir.joinpath('weather.csv')
            else:
                Path.mkdir(root_dir)
                csv_file = root_dir.joinpath('weather.csv')
        else:
            csv_file = path
        df = pd.DataFrame(data)
        df.to_csv(csv_file, mode='a', header=not Path(csv_file).exists(), index=False)
