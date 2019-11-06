
# itinerum-tripkit-cli

[![Python Version](https://img.shields.io/badge/Python-3.6%7C3.7-blue.svg?style=flat-square)]()

The `itinerum-tripkit-cli` makes using the `itinerum-tripkit` library fast and simple:

1. Create an `./input` and `./output` directory. Copy source .csv data to `./input`.
2. Edit a `config.py` file with data filepaths and trip processing parameters.
3. Run the tripkit command-line tool:
	### Itinerum
	```bash
	$ pip install itinerum-tripkit-cli
	$ tripkit-cli -c config.py itinerum
	```

	### QStarz
	```bash
	$ pip install itinerum-tripkit-cli
	$ tripkit-cli -c config.py qstarz
	```

## Config

*Sample config:*

```python
# filename for the itinerum-cli database
DATABASE_FN = 'itinerum_data.sqlite'

# path of raw data directory exported from Itinerum platform or Qstarz
INPUT_DATA_DIR = './input/csv-data-dir'
# types: "itinerum" or "qstarz"
INPUT_DATA_TYPE = 'itinerum'

# path of export data from itinerum-cli
OUTPUT_DATA_DIR = './output'

# path of subway station entrances .csv for trip detection
SUBWAY_STATIONS_FP = './input/subway_stations/stations.csv'

# trip detection parameters
TRIP_DETECTION_BREAK_INTERVAL_SECONDS = 300
TRIP_DETECTION_SUBWAY_BUFFER_METERS = 300
TRIP_DETECTION_COLD_START_DISTANCE_METERS = 750
TRIP_DETECTION_ACCURACY_CUTOFF_METERS = 50

# timezone of study area for calculating complete trip days
TIMEZONE = 'America/Montreal'

# semantic location columns in survey responses ('name': [lat_column, lon_column])
SEMANTIC_LOCATIONS = {
    'home': ['location_home_lat', 'location_home_lon'],
    'work': ['location_work_lat', 'location_work_lon'],
    'study': ['location_study_lat', 'location_study_lon']
}
SEMANTIC_LOCATION_PROXIMITY_METERS = 50

# OSRM map matcher API URLs
MAP_MATCHING_BIKING_API_URL = 'https://osrm.server.com/match/v1/biking/'
MAP_MATCHING_DRIVING_API_URL = 'https://osrm.server.com/match/v1/driving/'
MAP_MATCHING_WALKING_API_URL = 'https://osrm.server.com/match/v1/walking/'
```