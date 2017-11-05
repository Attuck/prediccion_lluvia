import csv
from numpy import mean
filepath = 'datos_paradigmas_without_manual_limited.csv'
# filepath = 'datos_paradigmas_test_1000.csv'
# filepath =  'datos_paradigmas_testing.csv'
with open(filepath, newline='') as source:
    with open('C50/prediccion_lluvia.data', 'w', newline='') as dest:
        reader = csv.DictReader(source)
        output = csv.writer(dest, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        hold = None
        last_avg_row = []
        count = 0
        for row in reader:
            count = count +1
            if hold == None:
                hold = row
            else:
                rain_mm = float(hold['RAIN_MM_TOT']) + float(row['RAIN_MM_TOT'])
                if last_avg_row != []:
                    if rain_mm > 0:
                        last_avg_row.append('t')
                    else :
                        last_avg_row.append('f')
                    output.writerow(last_avg_row)
                last_avg_row= [
                mean([float(hold['AIRTEMP_C_AVG'] if hold['AIRTEMP_C_AVG'] != "" else '0.0'),float(row['AIRTEMP_C_AVG'] if row['AIRTEMP_C_AVG'] != "" else '0.0')]),
                mean([float(hold['RH_PERCENT']if hold['RH_PERCENT'] != "" else '0.0'),float(row['RH_PERCENT']if row['RH_PERCENT'] != "" else '0.0')]),
                mean([float(hold['WINDSP_MS_S']if hold['WINDSP_MS_S'] != "" else '0.0'),float(row['WINDSP_MS_S']if row['WINDSP_MS_S'] != "" else '0.0')]),
                mean([float(hold['WINDSP_MS_U']if hold['WINDSP_MS_U'] != "" else '0.0'),float(row['WINDSP_MS_U']if row['WINDSP_MS_U'] != "" else '0.0')]),
                mean([float(hold['BP_MBAR']if hold['BP_MBAR'] != "" else '0.0'),float(row['BP_MBAR']if row['BP_MBAR'] != "" else '0.0')]),
                mean([float(hold['SLR_W_AVG']if hold['SLR_W_AVG'] != "" else '0.0'),float(row['SLR_W_AVG']if row['SLR_W_AVG'] != "" else '0.0')]),
                mean([float(hold['PAR_DEN_AVG']if hold['PAR_DEN_AVG'] != "" else '0.0'),float(row['PAR_DEN_AVG']if row['PAR_DEN_AVG'] != "" else '0.0')]),
                rain_mm
                ]
                hold=None
            # print (count)
        last_avg_row.append(0)
        output.writerow(last_avg_row)
