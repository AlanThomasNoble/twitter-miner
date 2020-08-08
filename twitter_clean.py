import glob, os 
import pandas as pd 
import re
def cleanData(text):
    cleaned = str(text)
    cleaned = re.sub(r'@[A-Za-z0-9]+', '', cleaned)  # Removes mentions
    cleaned = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',cleaned) # Removes hyperlink  
    cleaned = re.sub(r'(\bNaN\b)|(\bnan\b)','',cleaned) # Removes NaN values 
    cleaned = re.sub(r'[\s]+', ' ', cleaned)  # Removes additional white spaces
    cleaned = cleaned.strip('\'"').lstrip().rstrip() # Trim
    return cleaned

df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('', "output/KSO/*.csv"))))

total = len(df)
print(f"Total Entries: {total}")
df.drop_duplicates(subset='tweet id')
print(f"***{total - len(df)} Duplicate Entries Removed***")
total = len(df)
df.dropna(subset=['account status'], inplace=True)
print(f"***{total - len(df)} nan Entries Removed***")
total = len(df)
df['account status'] = df['account status'].apply(cleanData)
df['account status'].replace('',float('nan'),inplace=True)
df.dropna(subset=['account status'], inplace=True)
print(f"***{total - len(df)} Empty Entries Removed***")
print(f"New Total: {len(df)}\n")

df.to_csv('output/KSO/keywordFULL_watsoncleaned.csv')
import pdb; pdb.set_trace()