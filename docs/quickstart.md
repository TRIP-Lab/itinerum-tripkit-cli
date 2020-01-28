# Getting started with itinerum-tripkit-cli

The `itinerum-tripkit-cli` is designed to get started with using the `itinerum-tripkit` library easily and without requiring to write any code. Nevertheless, as a Python command-line utility, some setup is required.

**Requirements:**
- Python3 installed and globally accessible from the command-line. If Python3 is available on your system as `python3`, use that instead of `python` when following this guide.
- *On Windows:*
	- The [Visual C++ Redistributable for Visual Studio 2015 (13.4MB)](https://www.microsoft.com/en-ca/download/details.aspx?id=48145)
	- Compiled binaries for GDAL and Fiona dependencies (find these [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/)). Be sure to download the library version compatible with your Python installation (e.g., `GDAL‑3.0.3‑cp37‑cp37m‑win_amd64.whl` for 64-bit Python 3.7)

---
**Note on Windows PowerShell**

If activating the virtual environment gives the error "Running scripts is disabled on this system", PowerShell must be set to allow unsigned scripts. This can be fixed by running `Set-ExecutionPolicy Unrestricted -Force` and restarting the shell. For more information, see the [Python Virtual Env documentation](https://virtualenv.pypa.io/en/latest/userguide/).

---


**Installation:**
1. Create a project workspace
2. *Windows only*: Add compiled binary dependencies to an easily accessible directory. In the video example, a `vendor` folder is created and used.
<p align="center">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/z6biRgyzDVg" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</p>
3. Install all project dependencies. Installations on MacOS and Linux can create the virtual environment and skip directly to the `pip install itinerum-tripkit-cli` command.
<p align="center">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/7aO8sN5PT0k" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</p>
4. Create the directories for input and output data. Add source .csv coordinates and subway stations data (if declared in config). Add the tripkit configuration file (sample below).
<p align="center">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/PAxH0J_h7Io" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</p>

**Running**:
1. Run the `itinerum-tripkit-cli` with the desired options (available from help menu)
<p align="center">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/tFTmxo9wTlI" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</p>

**Config sample**: 
Configs named `tripkit_config.py` will be used automatically; configs with other filenames can be specified with the `-c` parameter).

```python
#!/usr/bin/env python

# filename for the itinerum-cli database
SURVEY_NAME = 'itinerum'

# path of raw data directory exported from Itinerum platform or Qstarz
INPUT_DATA_DIR = './input/itinerum-csv'
# types: "itinerum" or "qstarz"
INPUT_DATA_TYPE = 'itinerum'

# path of export data from itinerum-cli
OUTPUT_DATA_DIR = './output'

# path of subway station entrances .csv for trip detection
SUBWAY_STATIONS_FP = './input/subway_stations/mtl_stations.csv'

# trip detection parameters
TRIP_DETECTION_BREAK_INTERVAL_SECONDS = 300
TRIP_DETECTION_SUBWAY_BUFFER_METERS = 300
TRIP_DETECTION_COLD_START_DISTANCE_METERS = 750
TRIP_DETECTION_ACCURACY_CUTOFF_METERS = 50

# timezone of study area for calculating complete trip days
TIMEZONE = 'America/Montreal'

# location radius for activity dwell tallies
SEMANTIC_LOCATIONS = {
    'home': ['location_home_lat', 'location_home_lon'],
    'work': ['location_work_lat', 'location_work_lon'],
    'study': ['location_study_lat', 'location_study_lon']
}
ACTIVITY_LOCATION_PROXIMITY_METERS = 50

# OSRM map matcher API URLs
MAP_MATCHING_BIKING_API_URL = 'https://osrmserver.com/osrm/match/v1/biking/'
MAP_MATCHING_DRIVING_API_URL = 'https://osrmserver.com/osrm/match/v1/driving/'
MAP_MATCHING_WALKING_API_URL = 'https://osrmserver.com/osrm/match/v1/walking/'
```
