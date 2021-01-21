from flask import Flask
import json
import os
import requests

app = Flask(__name__)

@app.route('/houses')
def houses():
    current_dir = os.path.dirname(__file__)
    rel_path = "funda.json"
    abs_file_path = os.path.join(current_dir, rel_path)

    with open(abs_file_path) as json_file:
        data = json.load(json_file)
    first_coords = get_geocoords_by_postcode(data[0]['postcode'])

    return json.dumps(first_coords)

def get_geocoords_by_postcode(postcode):
    res_geo_api = json.loads(requests.get(
        'https://api.mapbox.com/geocoding/v5/mapbox.places/' + postcode + 
        '.json?access_token=pk.eyJ1IjoiamVzc2llemgiLCJhIjoiY2pxeG5yNHhqMDBuZzN4cHA4ZGNwY2l3OCJ9.T2B6-B6EMW6u9XmjO4pNKw'
        ).content)
    geo_coord_x = res_geo_api['features'][0]['center'][0]
    geo_coord_y = res_geo_api['features'][0]['center'][1]
    return (geo_coord_x, geo_coord_y)

if __name__ == '__main__':
    app.run()