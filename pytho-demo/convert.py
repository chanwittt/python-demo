#from os import replace, write
#import numpy as np
import pandas as pd
#from xlrd import XLRDError

#read data from excel
df = pd.read_excel(r'1608280489731_261215.xls', skiprows=1, converters={
                          'empNo': str, 'eventTime': str})
#reorder column

# without = df[df['empNo']== 'NaN' ].index
# df.drop(without, inplace = True) 
df = df[df['empNo'].notna()]
print(df)  

#print dataframe and save to text file
#print(df.to_csv(r'test.txt', header=None,index=False, sep='\t'))
#print(df)



