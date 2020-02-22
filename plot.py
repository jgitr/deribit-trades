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
    #strikes.append(i['instrument_name'].split('BTC-28FEB20-')[1])

def mkplot(x, y, fname, title):
    fig = plt.figure()
    plt.scatter(x, y)
    plt.title(title)
    fig.savefig(fname + '.png', transparent=True)

mkplot(call_strikes, call_prices, 'Calls-28Feb2020', 'Calls-28Feb2020 Prices vs. Strikes')
mkplot(put_strikes, put_prices, 'Puts-28Feb2020', 'Puts-28Feb2020 Prices vs. Strikes')

# fig = plt.figure()
# plt.scatter(call_strikes, call_prices)
# plt.subplot(2,1,2)
# plt.scatter(put_strikes, put_prices)
# plt.show()
#fig.savefig('temp.png', transparent=True)



# fig, (ax1, ax2) = plt.subplots(2)
# fig.suptitle('Aligning x-axis using sharex')
# ax1.plt.scatter(call_strikes, call_prices)
# ax2.plt.scatter(put_strikes, put_prices)
# plt.show()