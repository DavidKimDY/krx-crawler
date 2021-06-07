import coredotfinance.krx as krx

data = krx.get()
stock_list = list(data['종목코드'] + '^' + data['종목명'])
stock_txt = ''
for stock in stock_list:
    stock_txt += stock + '\n'
with open('stock_list.txt', 'w') as f:
    f.write(stock_txt)