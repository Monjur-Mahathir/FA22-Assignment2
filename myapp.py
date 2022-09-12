from flask import Flask, jsonify
import requests, json
import numpy as np
from datetime import date, datetime
from datetime import timedelta

app = Flask(__name__)

@app.route("/myjoke", methods=["GET"])
def mymethod():
    joke = "Why did everyone cross the road? Ha! ha, ha!"
    ret = {'category' : 'very funny', 'value' : joke}
    return jsonify(ret)

@app.route("/heartrate/last", methods=["GET"])
def last_heartrate():
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    current_time = datetime.now()
    fitbit_last_time = resp['activities-heart'][0]['dateTime'] + ' ' +resp['activities-heart-intraday']['dataset'][-1]['time']
    offset = str(current_time -  datetime.strptime(fitbit_last_time, '%Y-%m-%d %H:%M:%S'))
    print(offset)
    splitted_str = offset.split(':')
    offset_str = splitted_str[0] + ' hours, ' + splitted_str[1] + ' minutes and ' + splitted_str[2] + ' seconds'
    ret = {'heart-rate' : resp['activities-heart-intraday']['dataset'][-1]['value'], 'time-offset': offset_str}
    return jsonify(ret)

@app.route("/steps/last", methods=["GET"])
def last_step():
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    print(resp)
    fitbit_web_api_request_url_1 = "https://api.fitbit.com/1/user/-/activities/distance/date/today/1d.json"
    dis_resp = requests.get(fitbit_web_api_request_url_1, headers=user_auth).json()
    print(dis_resp)
    current_time = datetime.now()
    fitbit_last_time = resp['activities-steps'][0]['dateTime'] + ' ' +resp['activities-steps-intraday']['dataset'][-1]['time']
    offset = str(current_time -  datetime.strptime(fitbit_last_time, '%Y-%m-%d %H:%M:%S'))
    splitted_str = offset.split(':')
    offset_str = splitted_str[0] + ' hours, ' + splitted_str[1] + ' minutes and ' + splitted_str[2] + ' seconds'
    ret = {'step-count' : resp['activities-steps'][0]['value'], 'distance':dis_resp['activities-distance'][0]['value'] ,'time-offset': offset_str}
    return jsonify(ret)

@app.route("/sleep/<date>", methods=["GET"])
def sleep_log(date):
    fitbit_web_api_request_url = "https://api.fitbit.com/1.2/user/-/sleep/date/" + str(date) + ".json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    ret = {'deep': resp['summary']['stages']['deep'], 'light': resp['summary']['stages']['light'], 'rem': resp['summary']['stages']['rem'], 'wake': resp['summary']['stages']['wake']}
    return ret

@app.route("/activity/<date>", methods=["GET"])
def get_activity(date):
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesSedentary/date/" + str(date) +"/1d.json"
    resp_sedentary = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesLightlyActive/date/" + str(date) +"/1d.json"
    resp_light_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesFairlyActive/date/" + str(date) +"/1d.json"
    resp_fairly_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
        
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesVeryActive/date/" + str(date) +"/1d.json"
    resp_highly_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()

    ret = {'very-active' : int(resp_highly_active['activities-minutesVeryActive'][0]['value']), 'lightly-active':int(resp_light_active['activities-minutesLightlyActive'][0]['value']) ,'sedentary': int(resp_sedentary['activities-minutesSedentary'][0]['value'])}
    return jsonify(ret)
    
if __name__ == '__main__':
    user_auth = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRNVIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIxOTk2LCJpYXQiOjE2NjA3ODU5OTZ9.Rw2SpXEMA3YVx1-O1W0ZamKq2BwRnUpOw_fQCMRn0z8'}
    app.run(debug=True)