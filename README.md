# rgbDisplay

Created using commit 9f5ffd8 from https://github.com/hzeller/rpi-rgb-led-matrix

This repo will be combined with  the original rpi-rgb-led-matrix library for ease of install

**Supported information types:**

 Music

* Supports getting song information from LastFM
* Returned object contains artist name, track name and other info


News

* Pulls from the BBC News RSS feed
* setNewsType selects which news themes to show
* getNews requests the selected news headlines and descriptions for the chosen topic

Clock

* Displays the current time in 24hr format

**To fix:**

* Neaten timing code for schedulerThread to allow fast customisation

**To add:**

Multi display

* Connect and test 2 displays and provide simple parameters to select number of daisy chained displays

Stocks

* Show daily changes of chosen stocks

Weather

* Show forecast, highs, lows and wind speed
