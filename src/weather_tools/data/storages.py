import json
from pathlib import Path

test1 = [{'name': 'liwy', 'age': 20}, {'name': 'liwy2', 'age': 21}]

root_dir = Path(__file__).resolve(
).parent.parent.parent.parent.joinpath('data')
if root_dir.exists():
    csv_file = root_dir.joinpath('weather.csv')
else:
    Path.mkdir(root_dir)
    csv_file = root_dir.joinpath('weather.csv')

print(csv_file)

for i in test1:
    with open(csv_file, 'a', encoding='utf-8') as f:
        json.dump(i, f, ensure_ascii=False)
        f.write('\n')