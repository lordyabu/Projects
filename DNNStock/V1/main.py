import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras

data_file_path = "V0.062 Townsend Data - Sheet1.csv"

mkt_data = pd.read_csv(data_file_path)

mkt_data["Target"] = mkt_data.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])["Close"]
for i in range(0, 11202):
  if mkt_data["Close"][i] / mkt_data["1"][i] > 1.0011:
    mkt_data.loc[i, 'Target'] = 1
  else:
    mkt_data.loc[i, 'Target'] = 0

copy = []
for i in mkt_data['Target']:
    copy.append(i)

dict = {'Target' : copy}

dictdf = pd.DataFrame(dict)

dictdf.to_csv("TargetHeman1_0011.csv")