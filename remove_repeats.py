import pandas as pd

id_set = {-1}
df = pd.read_csv("output/keywords_output_full_watson.csv")

count = 0
dropped = 0
for index, row in df.iterrows():
    if row['tweet id'] in id_set:
        # remove it from df
        df.drop(index, inplace=True)
        dropped = dropped + 1
    else:
        count = count + 1
        id_set.add(row['tweet id'])

    if count % 100 == 0:
        print(f"dropped: {dropped}")
        print(f"new total: {count}")
        print()

print(f"final dropped: {dropped}")
print(f"final new total: {count}")
df.to_csv('final_filename.csv', index = False)