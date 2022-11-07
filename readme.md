# China realway stations data

It has train travelling data and station data.

- Train travelling data from 12306

  - url: https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0
  - path: raw/train_list.js
  - parsed: src/line.csv

- Station data from heywhale
  - url: https://www.heywhale.com/mw/dataset/600555c17ed5ab0015f00244/file
  - path: raw/cnstation.csv
  - parsed: src/station.csv

After parsing, the [parsed_line.csv](src/parsed_line.csv) is generated recording the starts and destinations of the train pairs.

To be clear, I believe the analysis method is solid, but the data is out-of-date. I am not sure if they are correct.
