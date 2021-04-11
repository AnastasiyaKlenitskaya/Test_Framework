import pyodbc
import csv

CSVfile = 'C:/Users/Anastasiya_Klenitska/Desktop/DQ_mentoring/4 task/Test_framework/for_testing.csv'
TEXTfile = 'C:/Users/Anastasiya_Klenitska/Desktop/DQ_mentoring/4 task/Test_framework/REG_UPDATES.txt'

conn_string = r'Driver={SQL Server};Server=localhost;Database=TRN;Trusted_Connection=Yes;'
con = pyodbc.connect(conn_string)
cur = con.cursor()

sql_query = 'SELECT * FROM hr.regions;'
rows = cur.execute(sql_query).fetchall()
records = [tuple(map(str,record)) for record in rows]

accessfile = set(records)

with open(CSVfile) as csv_file:
    reader = csv.DictReader(csv_file, delimiter = ',')
    for row in reader:
        csv_data = {row['п»їregion_id'], row['region_name']}
        diff = sorted(csv_data.difference(accessfile))
        print(diff)
    with open(TEXTfile, 'w') as result:
        for missing in diff:
            print(missing)
            result.write("".join(missing))

