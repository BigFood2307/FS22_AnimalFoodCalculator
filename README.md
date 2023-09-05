# Animal Food Calculator

__This is a standalone programm! For the mod, that just shows the Food requirements ingame, check out FS22_AnimalFoodCalculatorIngame!__

This script will calculate your food needs over a given amount of time.

All config is done in the xmls/script_settings.xml file

* Choose your base animals xml (animals is vanilla, eas_animals with EAS, copy in from a map if different)
* Choose your override xml (M+, M+ and EAS, custom). Use "" if you dont use M+
* Specify the path to your eas_settings file. Use "" if you dont use EAS (or if you use EAS pre 2.2.0.0)
* Give the path to your savegames placeables.xml. All animals will be read from there
* List all farmIds for which the animals should be read, other farms will be ignored
* Give the timeframe in months for which the calculation should be done
* In the age filter set minAge, maxAge. Only animals included in this range will be used when calculating the food amount
* List all the animal subtypes, that you want to calculate the in/outputs for
* Set your daysPerMonth for the daily food calculation
* Specify if you want to use the program in commandline or gui mode

Then just run the script...

The given amounts are for the entire timeframe, values in brackets behind it are average per day.

## GUI

A very basic GUI lets you change some settings on the fly and then rerun the calculation.  
You can also disable some Husbandries to exclude them from the result.
More functionality may follow at a later point.

## New births, deaths and selling

New animals are not currently added automatically. This may be included at a later date.
Similarly deaths or sales at certain ages for eg. bulls are an interesting topic, but not implemented.

## EAS Compatibility

EAS makes food usage and milk production a little more varied, by adjusting it shortly after a birth.  
If you specify a eas_settings file this programm will automatically read the adjustments from there and calculate food/milk accordingly.  
However, EAS also changed insemination to be chance based. This script assumes all inseminations are immediatley successful.  
In reality it takes about 0.72 months on average. This inaccuracy is bareley noticable in the short term, but will change the result slightly over longer timeframes.  
https://www.farming-simulator.com/mod.php?mod_id=259964&title=fs2022

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
