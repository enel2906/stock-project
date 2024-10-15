from polygon import RESTClient
import config
import json
from typing import cast
from urllib3 import HTTPResponse
from plotly import graph_objects as go
import pandas as pd
# import talib
import numpy as np
from pymongo import MongoClient

client = RESTClient(config.API_KEY)

mongo_client = MongoClient("mongodb://localhost:27017/") 
db = mongo_client['stock_db']
collection = db['apple_aggs']

aggs = cast(
    HTTPResponse,
    client.get_aggs(
        'AAPL',
        1,
        'day',
        '2022-05-20',
        '2023-11-11',
        raw=True
        ),
    
    )

data = json.loads(aggs.data)

for item in data:
    if item == 'results':
        rawData = data[item]

closeList = []
openList = []
highList = []
lowList = []
timeList = []

for bar in rawData:
    for category in bar:
        if category == 'c':
            closeList.append(bar[category])
        elif category == 'h':
            highList.append(bar[category])
        elif category == 'l':
            lowList.append(bar[category])
        elif category == 'o':
            openList.append(bar[category])
        elif category == 't':
            timeList.append(bar[category])

closeList = np.array(closeList)

# upper, middle, lower = talib.BBANDS(closeList, timeperiod = 20, nbdevdn = 2, matype = 0)
# print(upper)

times = []
for time in timeList:
    times.append(pd.Timestamp(time, tz = 'GMT', unit = 'ms'))

for i in range(len(timeList)):
    record = {
        "ticker": "AAPL",
        "date": pd.Timestamp(timeList[i], tz='GMT', unit='ms').strftime('%Y-%m-%d %H:%M:%S'),
        "open": openList[i],
        "high": highList[i],
        "low": lowList[i],
        "close": closeList[i]
    }
    collection.insert_one(record)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=times, open=openList, high=highList, low=lowList, close=closeList, name = 'Apple Market Data'))
# # fig.add_trace(go.Bar(x=times, volume=volumeList))
fig.update_layout(xaxis_rangeslider_visible=False, template = "plotly_dark")

fig.show()