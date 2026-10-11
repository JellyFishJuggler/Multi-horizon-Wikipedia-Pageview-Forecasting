import pandas as py
import numpy as np
import matplotlib.pyplot as mp

df = py.read_csv('data/processed.csv')

df['timestamp'] = py.to_datetime(df['timestamp'])
df['days'] = df['timestamp'].dt.day
# print(df['days'])

mp.figure(figsize=(8,8))
mp.plot(df['days'], df['views'])
mp.xlabel('Timestamp')
mp.ylabel('Views')
mp.show()
