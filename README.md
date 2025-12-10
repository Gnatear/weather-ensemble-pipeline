# weather-ensemble-pipeline
## how to run: 
cd ~/Projects/weather-ensemble-pipeline
source .venv/bin/activate
python main.py
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