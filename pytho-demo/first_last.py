#from os import replace, write
import numpy as np
import pandas as pd
#from xlrd import XLRDError

# read data from excel
df1 = pd.read_excel(r'logs.xls', converters={
    'empNo': str, 'eventTime': pd.to_datetime})

df2 = pd.read_excel(r'logs.xls', converters={
    'empNo': str, 'eventTime': pd.to_datetime})
# reorder column
df1['new_date'] = [d.date() for d in df1['eventTime']]
df1['new_time'] = [d.time() for d in df1['eventTime']]


df2['new_date'] = [d.date() for d in df2['eventTime']]
df2['new_time'] = [d.time() for d in df2['eventTime']]

df1 = df1.sort_values(by=['new_date'])
df2 = df2.sort_values(by=['new_date'])

first_scan = df1.drop_duplicates(subset=['empNo', 'new_date'], keep="first")
last_scan = df2.drop_duplicates(subset=['empNo', 'new_date'], keep="last")


new_column = ['empNo', 'eventTime', 'new_date', 'new_time']
first_scan = first_scan[new_column]
last_scan = last_scan[new_column]

first_scan['eventTime'] = first_scan['eventTime'].dt.strftime(
    '% Y % m % d % r')
last_scan['eventTime'] = last_scan['eventTime'].dt.strftime('% Y % m % d % r')

first_scan['eventTime'] = first_scan['eventTime'].str.replace(r'\D', '')
last_scan['eventTime'] = last_scan['eventTime'].str.replace(r'\D', '')

res_concat = pd.concat([first_scan, last_scan])
res_concat = res_concat.sort_values(by=['new_date'])
#res_concat['10space'] = '\s'

remove_newdatetime = ['empNo','eventTime']
res = res_concat[remove_newdatetime]


# print(first_scan.to_csv(r'first_last1.txt', index=False, sep='\t'))
# print(last_scan.to_csv(r'first_last2.txt', index=False, sep='\t'))
print(res.to_csv(r'first_last.txt', header=None, index=False, sep='\t'))
np.savetxt('np_save.txt', res, delimiter='          ', fmt="%s")

