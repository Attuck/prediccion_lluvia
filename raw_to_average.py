import csv
# from numpy import mean
# STATION_COUNT = {
# 1:127799,
# 2:264368,
# 3:380367,
# 4:439439,
# 5:469243,
# 6:499160
# }
# STATION_COUNT = {
# 1:19,
# 2:83,
# 3:99,
# }
# STATION_TEST = {
# 1:int(STATION_COUNT[1]*0.5),
# 2:int((STATION_COUNT[2]-STATION_COUNT[1])*0.5),
# 3:int((STATION_COUNT[3]-STATION_COUNT[2])*0.5),
# 4:int((STATION_COUNT[4]-STATION_COUNT[3])*0.5),
# 5:int((STATION_COUNT[5]-STATION_COUNT[4])*0.5),
# 6:int((STATION_COUNT[6]-STATION_COUNT[5])*0.5)
# }

#1:0
#2:127799
#3:264368
#4:380367
#32:439439
#33:469243
#499160
#total_rows= 127799
total_rows = 499160
test_proportion = 0.5
COLUMNS = [
'AIRTEMP_C_AVG',
'AIRTEMP_C_MAX',
'AIRTEMP_C_MIN',
'RH_PERCENT',
'WINDSP_MS_S',
'WINDSP_MS_U',
'BP_MBAR',
'SLR_W_AVG',
'SLR_W_MAX',
'SLR_W_MIN',
'PAR_DEN_AVG',
'PAR_DEN_MAX',
'PAR_DEN_MIN'
]
#DATA_DATE,hour,IDSTATION,AIRTEMP_C_AVG,AIRTEMP_C_MAX,AIRTEMP_C_MIN,RH_PERCENT,WINDSP_MS_S,WINDSP_MS_U,WINDDIR_DU,WINDDIR_SDU,BP_MBAR,SLR_W_AVG,SLR_W_MAX,SLR_W_MIN,SLR_W_STD,PAR_DEN_AVG,PAR_DEN_MAX,PAR_DEN_MIN,PAR_DEN_STD,RAIN_MM_TOT

print(total_rows)
# filepath = 'datos_paradigmas_test_100.csv'
filepath = 'datos_paradigmas_without_manual_limited.csv'
# filepath =  'datos_paradigmas_testing.csv'
with open(filepath, newline='') as source:
    with open('C50/prediccion_lluvia.data', 'w', newline='') as data_dest:
        with open('C50/prediccion_lluvia.test', 'w', newline='') as test_dest:
            reader = csv.DictReader(source)
            output_data = csv.writer(data_dest, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            output_test = csv.writer(test_dest, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            classified_row = []
            count = 0
            # station = 1
            test_rows = total_rows*test_proportion
            test_modulo = int(total_rows/test_rows)
            for row in reader:
                # print(count)
                if count == total_rows:
                    break
                for column in COLUMNS:
                    if row[column] == "" or row[column] == None:
                        classified_row.append("?")
                    else:
                        classified_row.append(float(row[column]))

                try:
                    rain = float(row['RAIN_MM_TOT'])
                except Exception as identifier:
                    rain = 0.0
                    pass
                if  rain > 0.0:
                    classified_row.append('t')
                else:
                    classified_row.append('f')

                if count % test_modulo == 0:
                    output_test.writerow(classified_row)
                    classified_row = []
                    # print('one to test')
                else:
                    output_data.writerow(classified_row)
                    classified_row = []
                    # print('one to data')


                count = count +1
