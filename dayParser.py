def main():
	import csv, sys, os, glob
	from WeatherParser import WeatherReader, IndividualWeatherFormatter, WeatherWriter
	'''
		Runs on the "Individual_Days" type text files
		Runs on all textfiles in the directory, converting them to csv files.
		Command line argument:
			-m = convert time format to metric units
		 blank = leave file as imperial units
	'''
	
	#handle the convert to metric switch
	convertToMetricFlag = False
	try:
		argument = sys.argv[1]
	except:
		argument = False
	
	if argument == "-c":
		convertToMetricFlag = True

	#loop through files in this directory
	os.chdir("../RAWS_hourly/days")
	for files in glob.glob("*.txt"):
	    #print files
	    #create object with filename
	    readerObject_month = WeatherReader(files, False)
	    #read file in
	    fileContainer_month = readerObject_month.readFile()
	    #format file
	    formatObject_month = IndividualWeatherFormatter(fileContainer_month, convertToMetricFlag)
	    formattedObject_month = formatObject_month.format()
	    #write out file as csv
	    weatherWrite_month = WeatherWriter(formattedObject_month, "imperial_" + files +".csv")
main()