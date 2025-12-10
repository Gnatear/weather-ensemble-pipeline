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
## if permission denied: test/....py
test folder: chmod -R 755 test/
single file: chmod 644 test/....py
6 - rw
4 - r
4 - r
single file: xattr -c test/....py
