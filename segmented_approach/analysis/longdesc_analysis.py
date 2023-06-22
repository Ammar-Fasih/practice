#######################################################################################################################
# Following code is to perform basic analysis on the unique elements from long description

import pandas as pd

df = pd.read_csv('longdesc3_compare.csv')
print(len(df))

df_new = (df['heading']+' | '+df['desc'])
print(len(df_new))

df_new = pd.DataFrame(df_new,columns=['0'])
print(len(df_new))

analysis = df_new.groupby(['0']).value_counts()
print((analysis))

analysis.to_csv('aa.csv')


