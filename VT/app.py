from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import xml.etree.ElementTree as ET
import os
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

API_KEY = 'b3818ae83b1500f6d34467a766e9972c03838945bfb40f570835193d7931edee'
VIRUSTOTAL_URL_FILE = 'https://www.virustotal.com/vtapi/v2/file/report'
VIRUSTOTAL_URL_SCAN = 'https://www.virustotal.com/vtapi/v2/file/scan'
VIRUSTOTAL_URL_URL = 'https://www.virustotal.com/vtapi/v2/url/report'

UPLOAD_FOLDER = '/tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

recent_results = []

@app.route('/')
def index():
    return render_template('index.html', recent_results=recent_results)

@app.route('/analyze', methods=['POST'])
def analyze():
    file_hash = request.form.get('file_hash')
    xml_data = request.form.get('xml_data')
    file = request.files.get('file')
    url = request.form.get('url')

    if not file and not url and not file_hash and not xml_data:
        flash('Please input File, URL or Hash', 'error')
        return redirect(url_for('index'))

    if xml_data:
        try:
            root = ET.fromstring(xml_data)
            file_hash = root.findtext('hash')
        except ET.ParseError:
            flash('Invalid XML data.', 'error')
            return redirect(url_for('index'))

    result = {}

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        try:
            file.save(file_path)
            with open(file_path, 'rb') as f:
                files = {'file': (file.filename, f)}
                response = requests.post(VIRUSTOTAL_URL_SCAN, files=files, params={'apikey': API_KEY})
                result = response.json()

                # Check if the scan was successful
                if result.get('response_code') == 1:
                    resource_id = result['resource']
                    time.sleep(15)  # Wait to give VirusTotal time to generate the report
                    params = {'apikey': API_KEY, 'resource': resource_id}
                    report_response = requests.get(VIRUSTOTAL_URL_FILE, params=params)
                    result = report_response.json()
                else:
                    flash('Error scanning file: {}'.format(result.get('verbose_msg', 'Unknown error')), 'error')
                    return redirect(url_for('index'))
        finally:
            os.remove(file_path)

    elif url:
        params = {'apikey': API_KEY, 'resource': url}
        response = requests.get(VIRUSTOTAL_URL_URL, params=params)
        result = response.json()

    elif file_hash:
        params = {'apikey': API_KEY, 'resource': file_hash}
        response = requests.get(VIRUSTOTAL_URL_FILE, params=params)
        result = response.json()

    else:
        flash('No valid input provided.', 'error')
        return redirect(url_for('index'))

    if result.get('response_code') == 1:
        formatted_result = {
            'file_name': file.filename if file else url if url else file_hash,
            'scan_date': result.get('scan_date', 'N/A'),
            'positives': result.get('positives', 0),
            'total': result.get('total', 0),
            'detections': []
        }

        for engine, details in result.get('scans', {}).items():
            if details.get('detected'):
                formatted_result['detections'].append({
                    'engine': engine,
                    'result': details.get('result', 'N/A'),
                    'version': details.get('version', 'N/A'),
                    'update': details.get('update', 'N/A')
                })

        # Save the formatted result in the recent_results list
        recent_results.insert(0, formatted_result)
        if len(recent_results) > 10:
            recent_results.pop()

        # Count malware and clean detections based on the current scan result
        malware_count = formatted_result['positives']
        clean_count = formatted_result['total'] - malware_count
        
        chart_data = {
            'malware_count': malware_count,
            'clean_count': clean_count
        }
    else:
        flash('Not included in Database / Scan in Progress', 'error')
        return redirect(url_for('index'))

    return render_template('result.html', result=formatted_result, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
