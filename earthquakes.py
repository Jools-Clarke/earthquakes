# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    """Retrieves earthquake data from the internet and saves it to a file"""
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    with open("eq_store.json", 'w') as f:
        f.write(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    eq_struct = json.loads(text)
    return eq_struct

def load_data():
    """Reads the stored earthquake data in from a file"""
    with open("eq_store.json", 'r') as f:
        text = f.read()
    eq_struct = json.loads(text)
    return eq_struct

def count_earthquakes(db):
    """Get the total number of earthquakes in the response."""
    
    return db['metadata']['count']


def get_magnitude(eq, db):
    """Retrive the magnitude of an earthquake item."""
    
    return db['features'][eq]['properties']['mag']


def get_location(eq, db):
    """Retrieve the latitude and longitude of an earthquake item."""
    
    lat,long = db['features'][eq]['geometry']['coordinates'][0:2]
    return {'coordinates':{'latitude':lat,'longitude':long}}


def get_maximum(db):
    """Get the magnitude and location of the strongest earthquake in the data."""
    
    max_mag = 0
    max_index = 0
    for eq in range(count_earthquakes(db)):
        if get_magnitude(eq, db) > max_mag:
            max_mag = get_magnitude(eq, db)
            max_index = eq
    return max_mag, get_location(max_index, db)['coordinates']


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")