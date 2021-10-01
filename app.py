from flask import Flask, jsonify, request
import requests as rq
import json

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['TRANS_ID'] = 0
# Capture Charging level

def get_charge_level(vin):
    url = "https://restmock.techgig.com/merc/charge_level"
    body = {
        "vin" : vin
    }
    headers = {'content-type': 'application/json'}
    response = rq.post(url,headers=headers,data=json.dumps(body))
    if response.status_code  == 200:
        return response.json()
    else:
        return json.dumps({"errors": [ { "id": 9999, "description": "Technical Exception" } ]})


# Capturing distance between source and destination

def get_distance(source,destination):
    url = "https://restmock.techgig.com/merc/distance"
    body = {
        "source" : source,
        "destination" : destination
    }
    headers = {'content-type': 'application/json'}
    response = rq.post(url,headers=headers,data=json.dumps(body))
    if response.status_code == 200:
        return response.json()
    else:
        return json.dumps({"errors": [ { "id": 9999, "description": "Technical Exception" } ]})


# Capturing the Charging points between source and destination


def get_charging_stations(source,destination):
    url = "https://restmock.techgig.com/merc/charging_stations"
    body = {
        "source" : source,
        "destination" : destination
    }
    headers = {'content-type': 'application/json'}
    response = rq.post(url,headers=headers,data=json.dumps(body))
    if response.status_code == 200:
        return response.json()
    else:
        return json.dumps({"errors": [ { "id": 9999, "description": "Technical Exception" } ]})
@app.route("/")
def index():
    return jsonify({"status": "Container is up and running"})

@app.route("/merc/estimate_travel", methods=["POST"])
def create_artist():
    
    # Capturing the input data
    
    app.config['TRANS_ID'] = app.config['TRANS_ID'] + 1
    trans_id = app.config['TRANS_ID']
    vehical_registration = request.json.get('vin')
    source = request.json.get('source')
    destination = request.json.get('destination')
    
    # Getting current charging level
    charge_details = get_charge_level(vehical_registration)

    if charge_details['error']:
        return jsonify({"transactionId": trans_id,"errors": [{"id": 9999,"description": "Technical Exception"},distance_details['error']]})
    else:
        current_charging = charge_details['currentChargeLevel']
        #print(current_charging)
    
    
    # Getting distance between source and destincation

    distance_details = get_distance(source=source, destination=destination)

    if distance_details['error']:
        return jsonify({"transactionId": trans_id,"errors": [{"id": 9999,"description": "Technical Exception"}]})
    else:
        distance = distance_details['distance']
        #print(distance)
        
    
    # Comparing the charging and distance to return if charging is > distance
    
    if current_charging >= distance:
        #print("Charging not requried")
        charging_required = False
        return jsonify({ "transactionId": trans_id , "vin": vehical_registration , "source": source , "destination": destination, "distance": distance , "currentChargeLevel": current_charging, "isChargingRequired": charging_required })
    else:
        #print("Charging required")
        charging_required = True
    
    # Getting the charging stations between source and destination

    station_details = get_charging_stations(source=source, destination=destination)

    if station_details['error']:
        return jsonify({"transactionId": trans_id,"errors": [{"id": 9999,"description": "Technical Exception"}]})
    else:
        charging_stations = station_details['chargingStations']
        #print(charging_stations)
        
    
    # Finding No of stations required
    
    ori_distance = distance
    ori_charge = current_charging
    stations = list()
    
    for station in charging_stations:
        #print(station)
    
        stations.append(station)
        charge_station_distance = station['distance']
    
        # Check if current charging is sufficient to reach the charging station
        #print("Current Charging : " + str(current_charging))
        #print("Charging Station Distance: " + str(charge_station_distance))
        
        if current_charging <= charge_station_distance: 
            return jsonify({ "transactionId": trans_id , "vin": vehical_registration , "source": source, "destination": destination, 
               "distance": ori_distance , "currentChargeLevel": ori_charge , "isChargingRequired": charging_required, 
               "errors": [ { "id": 8888, "description": "Unable to reach the destination with the current fuel level" } ] })
        
        
        # Updating new distance and charging available in car after reaching fuel station
        current_charging = (current_charging - charge_station_distance) + station['limit']
        
        # Current charging cannot be more than 100 %
        
        if current_charging > 100:
            current_charging = 100
        distance = distance - charge_station_distance
    
        # Check if current charging is enough for a destincation or go for another charging station
    
        if current_charging >= distance:
            return jsonify({ "transactionId": trans_id , "vin": vehical_registration , "source": source, "destination": destination, 
               "distance": ori_distance , "currentChargeLevel": ori_charge , "isChargingRequired": charging_required,
               "chargingStations": [stations]})
        
    

    return jsonify({ "transactionId": trans_id, "vin": vehical_registration , "source": source, "destination": destination, 
               "distance": distance , "currentChargeLevel": ori_distance , "isChargingRequired": ori_charge, 
               "errors": [ { "id": 8888, "description": "Unable to reach the destination with the current fuel level" } ] })


if __name__ == '__main__':
    app.run(debug=True)

