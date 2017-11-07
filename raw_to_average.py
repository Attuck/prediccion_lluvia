import csv
from numpy import mean
STATION_COUNT = {
1:127799,
2:264368,
3:380367,
4:439439,
5:469243,
6:499160
}
# STATION_COUNT = {
# 1:19,
# 2:83,
# 3:99,
# }
STATION_TEST = {
1:int(STATION_COUNT[1]*0.2),
2:int((STATION_COUNT[2]-STATION_COUNT[1])*0.2),
3:int((STATION_COUNT[3]-STATION_COUNT[2])*0.2),
4:int((STATION_COUNT[4]-STATION_COUNT[3])*0.2),
5:int((STATION_COUNT[5]-STATION_COUNT[4])*0.2),
6:int((STATION_COUNT[6]-STATION_COUNT[5])*0.2)
}
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

print(STATION_TEST)
# filepath = '/Users/rapuc/Google Drive/UCR/2017-II/CI-1441_Paradigmas/prediccion_lluvia/datos_paradigmas_test_100.csv'
filepath = 'datos_paradigmas_without_manual_limited.csv'
# filepath =  'datos_paradigmas_testing.csv'
with open(filepath, newline='') as source:
    with open('C50/prediccion_lluvia.data', 'w', newline='') as data_dest:
        with open('C50/prediccion_lluvia.test', 'w', newline='') as test_dest:
            reader = csv.DictReader(source)
            output_data = csv.writer(data_dest, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            output_test = csv.writer(test_dest, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            hold = None
            last_avg_row = []
            count = 0
            station = 1
            for row in reader:
                # print(count)
                if count == STATION_COUNT[station] :
                    station = station+1
                    last_avg_row.append('f')
                    output_data.writerow(last_avg_row)
                    last_avg_row = []
                    hold = None
                if hold == None:
                    hold = row
                else:
                    if hold['RAIN_MM_TOT'] == "" and row['RAIN_MM_TOT'] == "":
                        rain_mm = "?"
                    elif hold['RAIN_MM_TOT'] == "":
                        rain_mm =float(row['RAIN_MM_TOT'])
                    elif row['RAIN_MM_TOT'] == "":
                        rain_mm =float(hold['RAIN_MM_TOT'])
                    else:
                        try:
                            rain_mm = float(hold['RAIN_MM_TOT']) +float(row['RAIN_MM_TOT'])
                        except Exception:
                            print(hold['RAIN_MM_TOT'])
                            print(row['RAIN_MM_TOT'])
                            print(count)
                            rain_mm = 0.0
                            pass
                    if last_avg_row != []:
                        if rain_mm == "?" or rain_mm ==0:
                            last_avg_row.append('f')
                        else :
                            last_avg_row.append('t')
                        if count < STATION_COUNT[station]-STATION_TEST[station]:
                            output_data.writerow(last_avg_row)                      
                            last_avg_row = []
                        else:
                            output_test.writerow(last_avg_row)
                            last_avg_row = []

                    for column in COLUMNS:
                        if hold[column] == "" and row[column] == "":
                             last_avg_row.append("?")
                        elif hold[column] == "":
                            last_avg_row.append(float(row[column]))
                        elif row[column] == "":
                            last_avg_row.append(float(hold[column]))
                        else:
                            last_avg_row.append(mean([float(hold[column]),float(row[column])]))
                    last_avg_row.append(rain_mm )
                    hold=None
                count = count +1
            last_avg_row.append('f')
            output_data.writerow(last_avg_row)
