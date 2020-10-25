import pandas as pd
import numpy as np
import csv
import googletrans

from googletrans import Translator

headers = ['Context']
data = pd.read_csv('translated_spanish_edited.csv')
translator = Translator()
# Init empty dataframe with much rows as `data`
df = pd.DataFrame(index=range(0,len(data)), columns=headers)

def translate_row(row):
    ''' Translate elements A and B within `row`. '''
    a = translator.translate(row[0], dest='en')
    #b = translator.translate(row[1], dest='Fr')
    return pd.Series([a.text], headers)

for i, row in enumerate(data.values):
    # Fill empty dataframe with given serie.
    print(i)
    df.loc[i] = translate_row(row)
    df.to_csv("context_final.csv")
    


print(df)


