# Animal Food Calculator

This script will calculate your food needs over a given amount of time.

All config is done in the xmls/script_settings.xml file

* Choose your base animals xml (animals is vanilla, eas_animals with EAS, copy in from a map if different)
* Choose your override xml (M+, M+ and EAS, custom). Use "" if you dont use M+
* Give the path to your savegames placeables.xml. All animals will be read from there
* List all farmIds for which the animals should be read, other farms will be ignored
* Give the timeframe in months for which the calculation should be done
* In the age filter set minAge, maxAge. Only animals included in this range will be used when calculating the food amount
* List all the animal subtypes, that you want to calculate the in/outputs for
* Set your daysPerMonth for the daily food calculation

Then just run the script...

The given amounts are for the entire timeframe, values in brackets behind it are average per day.

## Python installation

If you have no idea how to run this script but still trust me enough to run some code you dont understand, here is how:

* Install Python 3: https://www.python.org/downloads/
* Open this folder in a command line: https://www.wikihow.com/Open-a-Folder-in-Cmd
* Type 'python main.py' (without quotes)
* Profit