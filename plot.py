import matplotlib.pyplot as plt
import json

filename = 'dict.txt'
sep = '\n'
with open(filename, "r") as f:
        out = []
        for line in f:
            print(f)
            values = line.split(sep)
            out.append(eval(values[0]))

# Isolate prices and strikes
call_prices = []
put_prices = []
call_strikes = []
put_strikes = []
for i in out:
    splt = i['instrument_name'].split('BTC-28FEB20-')[-1]
    if splt[-1] == 'C':
        call_prices.append(i['price'])
        call_strikes.append(int(splt[:-2]))
    else:
        put_prices.append(i['price'])
        put_strikes.append(int(splt[:-2]))

def mkplot(x, y, fname, title):
    fig = plt.figure()
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel('Strike')
    plt.ylabel('Price')
    fig.savefig(fname + '.png', transparent=True)

mkplot(call_strikes, call_prices, 'Calls-28Feb2020', 'Calls-28Feb2020 Prices vs. Strikes')
mkplot(put_strikes, put_prices, 'Puts-28Feb2020', 'Puts-28Feb2020 Prices vs. Strikes')

