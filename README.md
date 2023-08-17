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

## Executable

For ease of use, I added a windows executable to the releases. Just unzip the file to a folder and run the .exe.
If you move the exe, you have to move the xmls (at the very least the script_settings.xml, since its location is hard coded)

As this is an executable, make sure you trust me before you run it. This could be anything!
If someone wants to double check, this exe was created with pyinstaller version 5.13.0 using:

	pyinstaller -F -n FS22_AnimalFoodCalculator main.py

## Python installation

If you have no idea how to run this script without an executable but still trust me enough to run directly from code, here is how:

* Download this code from github
* Unpack it into a folder, enter the folder with this README inside it
* Install Python 3: https://www.python.org/downloads/
* Open this folder in a command line: https://www.wikihow.com/Open-a-Folder-in-Cmd
* Type 'python main.py' (without quotes)
* Profit
