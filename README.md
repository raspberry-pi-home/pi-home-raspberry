# pi-home

[![Build Status](https://travis-ci.org/gingrassia/pi-home.svg?branch=master)](https://travis-ci.org/gingrassia/pi-home)

Home Automation solution for Raspberry Pi using Python >= 3.5

### Dependencies

[aiohttp](http://aiohttp.readthedocs.io/en/stable/)

[aiohttp_jinja2](https://aiohttp-jinja2.readthedocs.io/en/stable/)

[gpiozero](https://gpiozero.readthedocs.io/en/stable/)

### Usage

```sh
git clone https://github.com/gingrassia/pi-home.git

cd pi-home

pip install -r requirements.txt
pip install -r requirements-raspberry.txt

python run_server.py
```

Then go to [raspberry-pi's ip on port 8000](http://localhost:8000) to see instructions to connect to the server and start playing with it

Note: if you don't install `gpiozero`, a mock version of it will be used so gpio ports of the raspberry-pi won't work (this is very useful for developing in a computer)

### Unit tests

```sh
cd pi-home

python -m unittest
```
