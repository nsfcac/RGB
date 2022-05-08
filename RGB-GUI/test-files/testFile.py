import json
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)

client.switch_database('cluster_info_db')

dbData = client.query('SELECT * FROM clusters')

data_points = []
for measurement, tags in dbData.keys():
    for p in dbData.get_points(measurement=measurement, tags=tags):
        data_points.append(p)

dbData_points = list(dbData.get_points())
final_points = []

for i in dbData_points:
    final_points.append(i)


def upload_file():
    with open('JSON_test_file') as json_file:
        file = json.load(json_file)

        client.write_points([
            {
                "fields": {
                    'cluster_name': file["cluster_name"],
                    'cluster_type': file["cluster_type"],
                    'ip': file["ip"],
                    'port': file["port"],
                    'mac_address': file["mac_address"]
                },
                "measurement": "clusters"
            }
        ])


upload_file()
