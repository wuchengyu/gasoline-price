import requests
import bs4
from pandas import DataFrame
import matplotlib.pyplot as plt
import re

if __name__ == "__main__":

  res = requests.post('https://price.nat.gov.tw/p/zh_tw/power_content', data={'tag': 'E1'}, headers={'Referer': 'https://price.nat.gov.tw/p/zh_tw/energy'})
  doc = bs4.BeautifulSoup(res.text, "html.parser")

  d = []
  p92 = []
  p95 = []
  p98 = []
  topic = 'cpc2' # 中油
  # topic = 'fpcc2' # 台塑

  content = doc.find('div', id='con_one_2')
  if content:
    tb = content.find('table', id=topic)
    if tb:
      trs = tb.find_all('tr')
      trs.reverse()
      trs.pop()
      for tr in trs:
        tds = tr.find_all('td')
        if tds:
          pattern = re.compile('\d+(.\d+)?')
          d.append(tds[0].text)
          p98.append(float(pattern.match(tds[1].text).group()))
          p95.append(float(pattern.match(tds[2].text).group()))
          p92.append(float(pattern.match(tds[3].text).group()))

      df = DataFrame({
        'date': d,
        '92': p92,
        '95': p95,
        '98': p98
      })

      df.plot(kind='line')
      plt.xticks(df.index, df['date'])
      plt.show()