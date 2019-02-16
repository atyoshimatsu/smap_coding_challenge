#coding:utf-8
import csv
import glob

import_files = glob.glob('./data/consumption/*.csv')
print(import_files)
for file in import_files:
    print('checking user_id:{}...'.format(file[-8:-4]))
    temp = ['','']
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            usage_time=row['datetime']
            kWh=row['consumption']
            if temp[0] == usage_time:
                print(temp[0], temp[1])
                print(usage_time, kWh)
            temp = [usage_time, kWh]