import csv
filepath = 'datos_paradigmas_without_manual_limited.csv'
# filepath =  'datos_paradigmas_testing.csv'
count = 0
with open(filepath, newline='') as source:
	reader = csv.DictReader(source)
	for row in reader:
		count = count +1;
	print( count)
