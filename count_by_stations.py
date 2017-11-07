import csv
filepath = 'datos_paradigmas_without_manual_limited.csv'
# filepath = 'datos_paradigmas_test_1000.csv'
# filepath =  'datos_paradigmas_testing.csv'
with open(filepath, newline='') as source:
    reader = csv.DictReader(source)
    count = 0
    station = 0
    for row in reader:
        if row['IDSTATION']!= station :
            station = row['IDSTATION']
            print(str(station) + ":" + str(count))
        count= count+1
    print(count)
