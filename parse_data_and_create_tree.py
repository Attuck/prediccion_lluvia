import csv
import subprocess

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

# from numpy import mean
STATION_COUNT = {
1:127799,
2:264368,
3:380367,
4:439439,
5:469243,
0:499160
}
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
test_proportion = 0.5
station = 1 #0 means all
COLUMNS = [
'AIRTEMP_C_AVG',
'AIRTEMP_C_MAX',
'AIRTEMP_C_MIN',
'RH_PERCENT',
'WINDSP_MS_S',
'WINDSP_MS_U',
#'WINDDIR_DU',
'BP_MBAR',
'SLR_W_AVG',
'SLR_W_MAX',
'SLR_W_MIN',
'PAR_DEN_AVG',
'PAR_DEN_MAX',
'PAR_DEN_MIN'
]
#DATA_DATE,hour,IDSTATION,AIRTEMP_C_AVG,AIRTEMP_C_MAX,AIRTEMP_C_MIN,RH_PERCENT,WINDSP_MS_S,WINDSP_MS_U,WINDDIR_DU,WINDDIR_SDU,BP_MBAR,SLR_W_AVG,SLR_W_MAX,SLR_W_MIN,SLR_W_STD,PAR_DEN_AVG,PAR_DEN_MAX,PAR_DEN_MIN,PAR_DEN_STD,RAIN_MM_TOT

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
            if station <= 1:
                total_rows = STATION_COUNT[station]
            else:
                total_rows = STATION_COUNT[station]-STATION_COUNT[station-1] 
            print(total_rows)
            test_rows = total_rows*test_proportion
            test_modulo = int(total_rows/test_rows)
            for row in reader:
                # print(count)
                if count == STATION_COUNT[station]:
                    break
                if station > 0:
                    if int(row['IDSTATION']) < station:
                         continue
                    elif int(row['IDSTATION']) > station:
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

cmd = "cd C50 && ./c5.0 -f predicción_lluvia > output_prediccion_lluvia_" + str(station) + "_" + str(test_proportion) + ".txt && cd .."
bash_command(cmd);
