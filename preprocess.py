"""
Preprocess data

Make sure they are useable

Line data from 12306
url: https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0
path: raw/train_list.js

Station data from heywhale
url: https://www.heywhale.com/mw/dataset/600555c17ed5ab0015f00244/file
path: raw/cnstation.csv
"""

# %%
import json
import pandas as pd

from pathlib import Path
from tqdm.auto import tqdm

# %%
"""
Parse stations

It contains duplicates, however I believe they are miss typing of the dataset.
"""

p = Path('raw/cnstation.csv')
station = pd.read_csv(p)
station = station.drop_duplicates(subset=['站名'], keep='first')
station.index = range(len(station))
station['站名'] = station['站名'].map(lambda s: s.replace('站', ''))
station


# %%
"""
Parse lines
"""

p = Path('raw/train_list.js')
lineData = open(p, encoding='utf-8').read()
# In case it is too long
print(lineData[:80])

"""
The dct has the structure of

-- [date, like 2019-06-20, 2019-06-21, ...]
 | -- [type, like D, T, G, C, O, K, Z]
 | -- [type]
-- [date]
 | -- [type]
 | -- [type]
-- ...
 | ...

"""
dct = json.loads(lineData.replace('var train_list =', ''))

# Select the nearest date, although it helps little.
date = sorted([e for e in dct])[-1]
schedule = dct[date]

dfs = []
for tp, val in tqdm(schedule.items(), 'Fill dfs for types'):
    df = pd.DataFrame(val)
    df['type'] = tp
    dfs.append(df)

line = pd.concat(dfs, axis=0)
line['code'] = line['station_train_code'].map(lambda s: s.split('(')[0][1:])
line['src'] = line['station_train_code'].map(
    lambda s: s.split('(')[1].split('-')[0].strip().replace('站', ''))
line['dst'] = line['station_train_code'].map(
    lambda s: s.split('(')[1].split('-')[1][:-1].strip().replace('站', ''))
line.index = range(len(line))

line

# %%
"""
Cross check
"""
src = line['src'].to_list()
station['srcCount'] = station['站名'].map(lambda name: src.count(name))

st = station['站名'].to_list()
line['srcCount'] = line['src'].map(lambda name: st.count(name))
line['dstCount'] = line['dst'].map(lambda name: st.count(name))
line['completeCount'] = line['srcCount'] + line['dstCount']

# %%
"""
Cross check for lines with stations
"""
step1 = pd.merge(left=line, right=station, left_on='src',
                 right_on='站名', how='inner')

step1['srcProv'] = step1['省']
step1['srcAuth'] = step1['铁路局']
step1 = step1[['station_train_code', 'train_no',
               'type', 'code', 'dst', 'src', 'srcProv', 'srcAuth']]

step2 = pd.merge(left=step1, right=station, left_on='dst',
                 right_on='站名', how='inner')
step2['dstProv'] = step2['省']
step2['dstAuth'] = step2['铁路局']
step2 = step2[['station_train_code', 'train_no', 'type', 'code',
               'src', 'srcProv', 'srcAuth', 'dst', 'dstProv', 'dstAuth']]

parsed_line = step2

# %%
station

# %%
line

# %%
parsed_line

# %%
"""
Save
"""
station.to_csv(Path('src/station.csv'))
line.to_csv(Path('src/line.csv'))
parsed_line.to_csv(Path('src/parsed_line.csv'))


# %%
"""
Summary
"""
print('=======================================')
print('Summary: ')
print(station.columns)
print(line.columns)
print(parsed_line.columns)


# %%

# %%
