import pandas as py
import numpy as np
# from datetime import datetime
import json

FILE_PATH = 'data/data.json'

with open(FILE_PATH,'r') as f:
    data = json.load(f)
    
items = data['items']
# print(items)

df = py.DataFrame(items)
print(df.columns)
# print(df['timestamp'])

# df['timestamp'] = datetime.strptime(df['timestamp'], "%Y-%m-%d %H:%M:%S")
df['timestamp'] = py.to_datetime(
    df['timestamp'],
    format="%Y%m%d%H"
)

df = df.sort_values(by='timestamp')
print(df.head())

# 0
print(df.duplicated().sum())


df.to_csv('data/processed.csv', index=False)

print('File exported Successfully')