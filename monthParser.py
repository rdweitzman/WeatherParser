def main():
	import csv, sys, os, glob
	from WeatherParser import WeatherReader, DailyListerFormatter, WeatherWriter
	'''
		Runs on the "Daily_Lister" type text files
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
		filePrefix = "metric_"
	else:
		filePrefix = "imperial_"

	#loop through files in this directory
	os.chdir("../RAWS_hourly/months")
	#os.chdir("test_input/dailyLister")
	for files in glob.glob("*.txt"):
	    #print files
	    #create object with filename
	    readerObject_day = WeatherReader(files, True)
	    #read file in
	    fileContainer_day = readerObject_day.readFile()
	    #format file
	    formatObject_day = DailyListerFormatter(fileContainer_day, convertToMetricFlag)
	    formattedObject_day = formatObject_day.format()
	    #write out file as csv
	    weatherWrite_day = WeatherWriter(formattedObject_day, filePrefix + files +".csv")
main()