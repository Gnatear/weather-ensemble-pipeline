# weather-ensemble-pipeline v 1.0.1
This repo is a experimental ETL data pipeline to fetch weather status from multiple platforms, and ensemble them for analysing use. At the current version(main branch), it can fetch data from open meteo api, and caculate mean, sd, outliers. I'm still working on adding features and optimizing.
## how to run: 
cd ~/Projects/weather-ensemble-pipeline
source .venv/bin/activate
python main.py --city Halifax --days 7 --output-json output/result.json
## how to install environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -r environments.txt
python main.py
## how to run test:
pytest
pytest test/test_....py
## how to compile:
python -m compileall
## if permission denied: test/....py:
test folder: chmod -R 755 test/
single file: chmod 644 test/....py
6 - rw
4 - r
4 - r
single file: xattr -c test/....py
## reasons of all the empty __init__.py files exist:
when trying to run the tests it says import failed. tried to use those files to tell python to read them as pakages to allow import.
not sure what's the problem. not sure it's fixed because of those files or something else. tend to not touch those files since the current program can run.
# current file structure
## README.md
## environment.txt
## config/
### -- initializer.py
- default flobal settings and API keys
* DEFAULT_CITY - Halifax
* DEFAULT_DAYS - 7
* DEFAULT_LAT, DEFAULT_LON - coordinates
## models/
### -- normalizer.py
- class WeatherPoint - unified weather record
* source, timestamp, temperature_c, wind_speed_ms, humidity, precipitation_mm, condition_code
- normalize_open_meteo(raw, source_name) - convers open meteo raw json into WeatherPoint opjects list
* extracts hourly arrays, aligns values by index, skips missing temperature values, returns normalized points
## fetchers/
### -- fetcher.py
- defines the base class(abstract) for all weather fetchers
* class Base Fetcher(ABC) require:
* - fetch_7days_forecast(city, days) - returns raw json from api 
### -- open_meteo.py
- fetches open meteo api
* __init__(lat, lon) - stores coordinates for api queries
* fetch_7day_forecast(city, days) - calls open-meteo forecast endpoint, requests hourly temperature, humidity, precipitation, wind. returns raw json
### -- weatherapi_fetcher.py
- empty for now
### -- visualcrossing_fetcher.py
- empty for now
## stats/
### -- aggregator.py
- statistical methods for ensemble analysis
* - aggregate_by_timestamp(points) - groups WeatherPoint objs by ts
* - compute_mean_ds(values) - get mean, sd
* - detect_outliers(values, z_threhold) - uses z-score. z = (value - mean) / sd, flags values when |z| > threshold, returns a list of booleans
## pipeline/
### -- run_pipeline.py
- run(city, days)
* - load defaults
* - call all fetchers
* - normalize raw data from api
* - group data by ts
* - compute mean, sd, outlier(flag)
* - return: structured dictionary which suppossed to look like this: 
{
  "city": "...",
  "days": ...,
  "source_count": ...,
  "timestamps": [
      {
        "timestamp": "...",
        "n_points": ...,
        "temperature_c": {
            "values": [...],
            "mean": ...,
            "sd": ...,
            "outlier_sources": [...]
        }
      }
  ]
}
## main.py
- command line entry point
* - parse_args() - parses: city, days, output-json
* - save_json(result, path) - writes pipeline output to disk
* - main() - parse CLI agrs, run pipeline, print summary, optionally save json as output
---------------------------------------------------------------
# update log
### Dec 10, 2025
updated README.md: added technical instructions, file structures, v 1.0.1 is ready


