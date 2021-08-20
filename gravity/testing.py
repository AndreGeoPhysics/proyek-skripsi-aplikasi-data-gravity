import pandas as pd 

csv_file = "C:/Users/ASUS/Desktop/data_dummy.csv"
raw = pd.read_csv(csv_file, sep=",")

for a in raw['x']:
    print(a)