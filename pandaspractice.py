import pandas as pd
import matplotlib.pyplot as plt
import csv

data = pd.read_csv("complete.csv")
print(data.head())
print(data.info())

data = []
with open("complete.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)
    print(data[1])