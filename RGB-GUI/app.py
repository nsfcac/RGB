import json
import sys
import os
import re
from IPy import IP
from flask_influxdb import InfluxDB
from flask import Flask, render_template, jsonify, request, flash
from werkzeug.utils import secure_filename, redirect

import RGB_L1
import RGB_L2
import RGB_L3
import RGB_Telemetry
import RGB_Checker

app = Flask(__name__)
influx_db = InfluxDB(app=app)


# method to get info database
def get_info(client):
    db_data = client.query('SELECT * FROM clusters')
    data_points = list(db_data.get_points())
    return data_points


# method that handles file upload
def upload_file():
    if request.files['file'] or request.args.get('ip'):
        file = request.files['file']
        if file:
            client = influx_db.connection
            client.switch_database('cluster_info_db')

            file = json.load(file)
            for i in file:
                client.write_points([
                    {
                        "fields": {
                            'device_name': i['device_name'],
                            'device_type': i['device_type'],
                            'ip': i['ip'],
                            'port': i['port'],
                            'mac_address': i['mac_address']
                        },
                        "measurement": "clusters"
                    }
                ])


# method that handles getting info from form fields and writing into database
@app.route('/post_cluster_info')
def post_cluster_info():
    client = influx_db.connection
    client.switch_database('cluster_info_db')

    ip_verification = re.match(
        "^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        request.args.get('ip'))
    mac_verification = re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
                                request.args.get('mac_address').lower())
    port_verification = re.match(
        "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
        request.args.get('port'))

    if ip_verification and mac_verification and port_verification:
        client.write_points([
            {
                "fields": {
                    'device_name': request.args.get('device_name'),
                    'device_type': request.args.get('device_type'),
                    'ip': request.args.get('ip'),
                    'port': request.args.get('port'),
                    'mac_address': request.args.get('mac_address')
                },
                "measurement": "clusters"
            }
        ])
    if not ip_verification:
        return jsonify("ip error")

    if not mac_verification:
        return jsonify("mac error")

    if not port_verification:
        return jsonify("port error")

    return jsonify(get_info(client))


@app.route('/show_data_center_info', methods=['GET'])
def show_data_center_info():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    return jsonify(get_info(client))


@app.route('/result1')
def result1():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res1 = RGB_L1.runGreenTest(get_info(client))
    return jsonify(res1)


@app.route('/result2')
def result2():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res2 = RGB_L2.runGreenTest(get_info(client))
    return jsonify(res2)


@app.route('/result3')
def result3():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res3 = RGB_L3.runGreenTest(get_info(client))
    return jsonify(res3)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/level1', methods=['GET', 'POST'])
def level1():
    if request.method == 'POST':
        upload_file()
    level_type = "Level One"
    return render_template('measurement-results-page.html', level_type=level_type)


@app.route('/level2', methods=['GET', 'POST'])
def level2():
    if request.method == 'POST':
        upload_file()
    level_type = "Level Two"
    return render_template('measurement-results-page.html', level_type=level_type)


@app.route('/level3', methods=['GET', 'POST'])
def level3():
    if request.method == 'POST':
        upload_file()
    level_type = "Level Three"
    return render_template('measurement-results-page.html', level_type=level_type)


if __name__ == '__main__':
    app.secret_key = 'this key is so secret'
    app.run(debug=True, host='0.0.0.0')
