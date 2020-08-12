import pandas as pd

def remove_newline(x):
    return x.rstrip('\n')

df = pd.read_csv("keywords_output_1.csv")
df['search query'] = df['search query'].apply(remove_newline)
df.reset_index(drop=True, inplace=True)
df.to_csv('filename.csv', index = False)