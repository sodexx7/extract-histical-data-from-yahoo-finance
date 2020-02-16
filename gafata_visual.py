import pandas as pd
# extract price of "Adjusted Close"
series = pd.DataFrame()

gafata = ['^GSPC', 'GOOG', 'AAPL', 'FB', 'AMZN', '0700.HK', 'BABA']

source_data_path = "/Users/data/"
dest_data_path = "/Users/data/"

df = pd.read_csv(
    f"{source_data_path}{gafata[0]}.csv"
)

number_of_rows = df.shape[0]
series['Date'] = df['Date'].tolist()

for symbol in gafata:
    series[f'{symbol}'] = pd.read_csv(f'{source_data_path}{symbol}.csv')['Adj Close'].tolist()

# add columns of "price change from the start"
gspc_pc, goog_pc, aapl_pc, fb_pc, amzn_pc, hk700_pc, baba_pc, base = [], [], [], [], [], [], [], []
for i in range(0, number_of_rows):
    gspc_pc.append(float(series.at[i, "^GSPC"])/float(series.at[0, "^GSPC"]) - 1)
    goog_pc.append(float(series.at[i, "GOOG"])/float(series.at[0, "GOOG"]) - 1)
    aapl_pc.append(float(series.at[i, "AAPL"])/float(series.at[0, "AAPL"]) - 1)
    fb_pc.append(float(series.at[i, "FB"])/float(series.at[0, "FB"]) - 1)
    amzn_pc.append(float(series.at[i, "AMZN"])/float(series.at[0, "AMZN"]) - 1)
    hk700_pc.append(float(series.at[i, "0700.HK"])/float(series.at[0, "0700.HK"]) - 1)
    baba_pc.append(float(series.at[i, "BABA"])/float(series.at[0, "BABA"]) - 1)
    base.append(0)

series['c^GSPC'], series['cGOOG'], series['cAAPL'], series['cFB'], series['cAMZN'], \
    series['c0700.HK'], series['cBABA'], series['base'] = \
    gspc_pc, goog_pc, aapl_pc, fb_pc, amzn_pc, hk700_pc, baba_pc, base

# assuming you're investing regularly, this column set the amount of total invested.
weekly_invested = 1000
total_invested = []
for i in range(0, number_of_rows):
    total_invested.append((i+1)*weekly_invested)
series['Total Invested'] = total_invested


# weekly bought shares
gspc_wb, goog_wb, aapl_wb, fb_wb, amzn_wb, hk700_wb, baba_wb = [], [], [], [], [], [], []
for i in range(0, number_of_rows):
    gspc_wb.append(weekly_invested / float(series.at[i, "^GSPC"]))
    goog_wb.append(weekly_invested / float(series.at[i, "GOOG"]))
    aapl_wb.append(weekly_invested / float(series.at[i, "AAPL"]))
    fb_wb.append(weekly_invested / float(series.at[i, "FB"]))
    amzn_wb.append(weekly_invested / float(series.at[i, "AMZN"]))
    hk700_wb.append(weekly_invested / float(series.at[i, "0700.HK"]))
    baba_wb.append(weekly_invested / float(series.at[i, "BABA"]))

series['wb^GSPC'], series['wbGOOG'], series['wbAAPL'], series['wbFB'], series['wbAMZN'], \
    series['wb0700.HK'], series['wbBABA'] = \
    gspc_wb, goog_wb, aapl_wb, fb_wb, amzn_wb, hk700_wb, baba_wb



# value accumulated
gspc_va, goog_va, aapl_va, fb_va, amzn_va, hk700_va, baba_va = [], [], [], [], [], [], []
for symbol in gafata:
    value_accumulated = []
    for i in range(0, number_of_rows):
        holding = 0
        for j in range(0, i+1):
            holding += series.at[j, f'wb{symbol}']
        value_accumulated.append(holding * series.at[i, f'{symbol}'] )
    series[f'va{symbol}'] = value_accumulated   


# value accumulated for gafata as whole
value_accumulated_gafata = []
for i in range(0, number_of_rows):
    value = 0
    for symbol in gafata[1:]:       # excluding ^GPSC
        value += series.at[i, f'va{symbol}']
    value_accumulated_gafata.append(value)
series['vaGAFATA'] = value_accumulated_gafata


# regularlin investing on each stock, profit rate of total invested. 

gspc_rivc, goog_rivc, aapl_rivc, fb_rivc, amzn_rivc, hk700_rivc, baba_rivc, gafata_rivc = [], [], [], [], [], [], [], []
for i in range(0, number_of_rows):
    gspc_rivc.append(float(series.at[i, "va^GSPC"])/ float(series.at[i, "Total Invested"]) - 1)
    goog_rivc.append(float(series.at[i, "vaGOOG"]) / float(series.at[i, "Total Invested"]) - 1)
    aapl_rivc.append(float(series.at[i, "vaAAPL"]) / float(series.at[i, "Total Invested"]) - 1)
    fb_rivc.append(float(series.at[i, "vaFB"]) / float(series.at[i, "Total Invested"]) - 1)
    amzn_rivc.append(float(series.at[i, "vaAMZN"]) / float(series.at[i, "Total Invested"]) - 1)
    hk700_rivc.append(float(series.at[i, "va0700.HK"]) / float(series.at[i, "Total Invested"]) - 1)
    baba_rivc.append(float(series.at[i, "vaBABA"]) / float(series.at[i, "Total Invested"]) - 1)
    gafata_rivc.append(float(series.at[i, "vaGAFATA"]) / (float(series.at[i, "Total Invested"]) * 6) - 1)

series['rivc^GSPC'], series['rivcGOOG'], series['rivcAAPL'], series['rivcFB'], series['rivcAMZN'], \
    series['rivc0700.HK'], series['rivcBABA'], series['rivcGAFATA'] = \
    gspc_rivc, goog_rivc, aapl_rivc, fb_rivc, amzn_rivc, hk700_rivc, baba_rivc, gafata_rivc


# draw the figure
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
series.plot(kind='line', linestyle='dotted', x='Date', y='base', ax=ax, figsize = (20,10), color="gray")
lines = ['cGOOG', 'cAMZN', 'cFB', 'cAAPL', 'c0700.HK', 'cBABA', 'rivcGAFATA']
for line in lines:
    series.plot(kind='line', linestyle='solid', x='Date', y=line, ax=ax, figsize = (20,10))

#plt.show()
plt.savefig(f"{dest_data_path}gafata_invest_change.png", transparent=True)