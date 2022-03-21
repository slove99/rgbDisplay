# RGB Matrix Helper

## Display miscellaneous information through RGB LED matrix boards
## Tested on:
- Python version: <code>python3.7</code> 
- OS: <code>Raspbian GNU/Linux 10 (buster) armv6l</code> 
- Device: <code>Raspberry Pi Model B Rev 2</code> 
- RGB matrix repo commit: <code>[a56338db0f003d5236f2ce98c73a591d64a70852](https://github.com/hzeller/rpi-rgb-led-matrix/tree/a56338db0f003d5236f2ce98c73a591d64a70852)</code>
## Installation instrustions:
### Recommended:
- Create a dedicated virtual environment for this project: <code> python3 -m venv 
/path/to/new/virtual/environment </code>
### Required:
* Install system packages: <code>libopenjp2-7</code>, <code>libxcd1</code>, <code>python3-dev</code>, 
<code>python3-pillow</code> 
* Clone [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix): 
<code>git clone https://github.com/hzeller/rpi-rgb-led-matrix </code> 
* Follow instructions on [rpi-rgb-led-matrix/bindings/python](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)  to build python with required arguments:
	- Currently this involves running these commands within your <code>rpi-rgb-led-matrix</code> folder: 
		- <code>make build-python PYTHON=$(command -v python3)</code> 
		- <code>sudo make install-python PYTHON=$(command -v python3)</code>
	> If using a virtual envionment, ensure python3 is pointing to the correct location (run <code>which 
	> python3</code> and check the path points to 
	> <code><path_to_venv_folder><venv_name>/bin/python3</code>)
* Clone this repo: <code>git clone https://github.com/slove99/rgbDisplay</code> 
* Install python requirements: <code> pip install -r requirements.txt </code> 
* Run <code>main.py</code> and supply 
<code>--rows</code>, <code>--cols</code>, <code>--chain-len</code>, args to suit your needs
## Supported information types:
### Music:
* Supports getting song information from LastFM 
	* Returned object contains artist name, track name and other info
### News:
* Pulls headlines from the BBC News RSS feed
	* <code>setNewsType</code> selects which news themes to show 
	* <code>getNews</code> requests the selected news headlines and descriptions for the chosen topic
### Clock:
* Displays the current time in 24hr format
## Upcoming changes:
### To fix:
* Neaten timing code for <code>schedulerThread</code> to allow fast customisation 
* Add smarter timing of information requests to improve scrolling performance
### To add:
* Code restructuring 
	* Move away from demo code foundations to allow greater control over program layout 
* Stocks
	* Show daily changes of chosen stock symbols 
* Weather 
	* Show forecast, highs, lows and wind speed 
* Music
	* Move away from lastfm reliance and towards direct API calls for MPD and Spotify
