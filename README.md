
# itinerum-tripkit-cli

[![Python Version](https://img.shields.io/badge/Python-3.6%7C3.7-blue.svg?style=flat-square)]()

Want to get up and running fast? Try the [itinerum-tripkit-cli quickstart guide](https://trip-lab.github.io/itinerum-tripkit-cli/quickstart)!

If you're more interested in taking a look under the hood, you can find our underlying *itinerum-tripkit* and documentation here: https://github.com/TRIP-Lab/itinerum-tripkit


## Quick comands
*Show help:*
```bash
$ tripkit-cli --help
```

*Logging verbosity:*
```bash
$ tripkit-cli -q  # quiet (no output messages)
$ tripkit-cli -v  # verbose
```

*Supply config:*
```bash
$ tripkit-cli -c config.py
```

*Write GIS data outputs*
```bash
$ tripkit-cli
```

## Config
*Sample config:*

```python
##
## itinerum-tripkit configuration
##
SURVEY_NAME = 'itinerum_survey'

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

# semantic location radius for activity dwell tallies
ACTIVITY_LOCATION_PROXIMITY_METERS = 50

# OSRM map matcher API URLs
MAP_MATCHING_BIKING_API_URL = 'https://osrm.server.com/match/v1/biking/'
MAP_MATCHING_DRIVING_API_URL = 'https://osrm.server.com/match/v1/driving/'
MAP_MATCHING_WALKING_API_URL = 'https://osrm.server.com/match/v1/walking/'

##
## itinerum-tripkit-cli configuration
##
# GIS output formats: shp (shapefile), gpkg (geopackage), geojson
GIS_OUTPUT_FORMAT = 'shp'

```
