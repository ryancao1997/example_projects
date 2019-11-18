import clarus
import datetime
def read_csv(name):
    import csv
    data = []
    with open(name) as file1:
        file = csv.reader(file1)
        for row in file:
            data.append(row)
    return data

file = read_csv("FIN451_homework4.csv")
print(file)