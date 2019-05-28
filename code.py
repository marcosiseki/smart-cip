import sys
import csv
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    sys.exit('Usage: python2 %s filename.csv start_year stop_year' % sys.argv[0])

filename = sys.argv[1]
start_year = sys.argv[2]
stop_year = sys.argv[3]
ipcs = '[A-H]'

try:
	csvfile = open(filename,"r")
	dialect = csv.Sniffer().sniff(csvfile.readline())
	csvfile.seek(0)
except:
	dialect.delimiter = '\t'

df = pd.read_csv(filename,sep=dialect.delimiter,encoding='utf-8')

df.columns = df.columns.str.strip().str.replace(' ', '_')

df.Application_Date = pd.to_datetime(df.Application_Date,dayfirst=True)

df2 = pd.DataFrame()

for year in range (int(start_year), int(stop_year)+1):

    df1 = df[(df['Application_Date'] >= str(year)+'-01-01') & (df['Application_Date'] <= str(year)+'-12-31')]

    str1 = ""

    for j, ind in enumerate(df1.index.values):
        str1 = str1 + df1.IPCR_Classifications[ind]

    str1 = str1.encode('utf-8')
    regex = ipcs + r'\d{2}\w'
    #regex = r'H04W|A01B|G08G'
    #regex = r"\b(?=\w)" + ipcs# + r"\b(?=\w)"
    fnd = re.findall(regex,str1)

    cnt = Counter()

    for word in fnd:
        cnt[word] += 1
    
    for ipc, freq in cnt.items():
        df2.at[ipc,year] = freq

df2 = df2.fillna(0)
df2 = df2.sort_index(axis=0)
df2 = df2.sort_index(axis=1)
df2 = df2.astype(int)
df2 = df2.drop([filename.upper()],errors='ignore')
df2.to_csv('all_icps_' + filename + '_updated2.csv',sep=',',encoding='utf-8')
