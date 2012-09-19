class WeatherReader:
	'''Class used to read in a file and store it in a data structure'''

	def __init__(self, fileName_in, leadingLine):
		'''used to load the file associated to the filename into a datastructure (array containing lists of lines).'''
		self.fileName = fileName_in
		self.leadingLine = leadingLine

	def readFile(self):
		'''reads in the file and returns the dataContainer containing the file contents'''
		self.file = open(self.fileName, "r", 1)
		self.fileContainer = self.file.readlines()
		self.file.close()

		#clean up the list object
		self.dataList = []

		for item in self.fileContainer:
			self.dataList.append(' '.join(item.split()))

		#remove first line in list object if monthparser calls
		if self.leadingLine == True:
			del self.dataList[0]	

		return self.dataList

	def setFile(self, fileName_in):
		'''used to set a different filename into memory'''
		self.file = fileName_in

	def printFile(self):
		'''used to display the file for troubleshooting'''
		print self.dataList

class IndividualDaysFormatter:
	'''Class used to format the data that was read in from the file.'''

	def __init__(self, fileObject_in, convertToMetricFlag_in):
		'''sets up the formatter object with the file object created by the reader'''
		self.fileObject = fileObject_in
		self.convertToMetricFlag = convertToMetricFlag_in

	def format(self):
		'''performs formatting operations on the file object
			http://stackoverflow.com/questions/3685195/line-up-columns-of-numbers-print-output-in-table-format
		'''
		data = self.fileObject
		flag = self.convertToMetricFlag

		#create formatted times
		times = self.timeFormat(data)

		listOfRows = []
		
		#split on whitespace
		for line in data:
			listOfRows.append(line.split(' '))

		#add proper times to the data object
		i = 0
		for line in listOfRows:
			del line[:2]
			line.insert(0, times[i])
			i += 1 	
		
		#add headers to the data object
		headers, subheaders = self.individualHeaders()
		listOfRows.insert(0, subheaders)
		listOfRows.insert(0, headers)

		#account for holes in the data
		for item in listOfRows:
			if len(item) < 8:
				item.insert(2, " ")
			if len(item) < 9:
				item.insert(3, " ")
		
		return listOfRows


	def individualHeaders(self):
		''' creates the headers for the IndivudualWeatherFormatter columns'''
		headers = ["Hour of Day", "Average Wind Speed", "Wind Velocity Direction", "Maximum Wind Speed", "Air Temperature", "Relative Humidity", "Dew Point", "Wet Bulb", "Total Precipitation"]
		subheaders = [" ", "(Meters/Second)", "(Degree)", "(Meters/Second)", "(Mean)", "(Mean/Percent)", " ", "(Deg. C)", "(Millimeters)"]

		return headers, subheaders

	def timeFormat(self, to_format):
		''' changes times from 12 to 24 hours'''
		data = to_format
		newtimes = []

		#convert 12 to 24 hour time
		for item in data:
			lastLetterM = item.index("m")
			sliceOfInterest = item[:lastLetterM + 1]
			
			#if the last two letters are am, add the appropriate minutes
			if sliceOfInterest[2:].strip() == 'am':
				if len(sliceOfInterest[:2].strip()) >= 2:
					#check for special case of midnight
					if int(sliceOfInterest[:2].strip()) == 12:
						newtimes.append("00:00")
					#otherwise...
					else:
						newtimes.append(sliceOfInterest[:2].strip() + ":00")
				else:
					newtimes.append("0" + sliceOfInterest[:2].strip() + ":00")


			#if the last two letters are pm, add the appropriate hours and minutes
			elif sliceOfInterest[2:].strip() == 'pm':
				#special case if it's noon
				if int(sliceOfInterest[:2].strip()) == 12:
					temptime = int(sliceOfInterest[:2].strip()) + 0
					stringTime = str(temptime)
					newtimes.append(stringTime + ":00 ")
				#otherwise
				else:
					tempTime = int(sliceOfInterest[:2].strip()) + 12
					stringTime = str(tempTime)
					newtimes.append(stringTime + ":00 ")

		return newtimes

	def setObject(self, newObject_in):
		'''sets file object to some new object'''
		self.fileObject = newObject_in

	def printObject(self):
		'''prints the object for troubleshooting'''
		print self.fileObject

class DailyListerFormatter:
	''' used to format the daily lister text file '''

	def __init__(self, fileObject_in, convertToMetricFlag_in):
		'''sets up the formatter object with the file object created by the reader'''
		self.fileObject = fileObject_in
		self.convertToMetricFlag = convertToMetricFlag_in

	def format(self):
		''' formats the data appropriately '''
		data = self.fileObject			
		flag = self.convertToMetricFlag

		#need to check flag and change units depending on it

		#get lists of formatted time
		totalDateTime, yearMonth, day, hourMinute = self.dateTimeFormat(data)

		#make lists of each row in data
		rows = []
		for item in data:
			rows.append(item.split(" "))

		#remove incorrectly formatted times, then add correctly formatted ones
		i = 0
		for row in rows:
			del row[0]
			row.insert(0, hourMinute[i])
			row.insert(0, day[i])
			row.insert(0, yearMonth[i])
			row.insert(0, totalDateTime[i])
			i += 1

		#check flag and if true, then convert from imperial to metric units and add the appropriate headers
		if flag: 
			rows = self.convertToMetric(rows)
			headers, subheaders = self.conversionHeaders()
		else:
			#add regular headers
			headers, subheaders = self.individualHeaders()

		# add headers
		rows.insert(0, subheaders)
		rows.insert(0, headers)

		return rows

	def convertToMetric(self, rows):
		#perform conversion to metric line by line on those elements that need them 
		#columns 4,5,7,8,12 need conversion
		for i in rows:
			#if the values in column 4,5,7,8,or 12 are greater than 0, perform the following conversions
			
			if float(i[4]) > 0:
				#convert inches to millimeters
				toConvert = float(i[4])
				converted = toConvert * (25.4/1)
				i[4] = converted
			
			if float(i[5]) > 0:
				#convert mph to kmph
				toConvert = float(i[5])
				converted = toConvert * (1.60934/1)
				i[5] = converted				
			
			if float(i[7]) > 0:
				#convert Fahrenheit to Celsius
				toConvert = float(i[7])
				converted = ((toConvert - 32) * 5) / 9
				i[7] = converted

			if float(i[8]) > 0:
				#convert Fahrenheit to Celsius
				toConvert = float(i[8])
				converted = ((toConvert - 32) * 5) / 9
				i[8] = converted
				
			if float(i[12]) > 0:
				#convert mph to kmph
				toConvert = float(i[12])
				converted = toConvert * (1.60934/1)
				i[12] = converted	

		return rows

	def individualHeaders(self):
		''' creates the headers for the columns'''
		headers = ["YRMTHDAYHHMM", "YRMTH", "DAY", "HHMM", "Precipitation", "Wind Speed", "Wind Direction", "Average Air Temperature", "Fuel Temperature", "Relative Humidity", "Battery Voltage", "Max Gust Direction", "Max Gust Speed", "Solar Radiation"]
		subheaders = ["-", "-", "-", "-", "(inches)", "(mph)", "(degrees)", "(degrees F)", "(degrees F)", "(percentage)", "(volts)", "(degrees)", "(mph)", "(watts/meters squared)"]

		return headers, subheaders

	def conversionHeaders(self):
		''' creates the headers for the columns using converted units instead of the raw units (imperial to metric)'''
		headers = ["YRMTHDAYHHMM", "YRMTH", "DAY", "HHMM", "Precipitation", "Wind Speed", "Wind Direction", "Average Air Temperature", "Fuel Temperature", "Relative Humidity", "Battery Voltage", "Max Gust Direction", "Max Gust Speed", "Solar Radiation"]
		subheaders = ["-", "-", "-", "-", "(mm)", "(kmph)", "(degrees)", "(degrees C)", "(degrees C)", "(percentage)", "(volts)", "(degrees)", "(kmph)", "(watts/meters squared)"]

		return headers, subheaders

	def dateTimeFormat(self, to_format):
		''' formats the date and time columns YYMMDDhhmm'''
		totalDateTime = []
		yearMonth = []
		day = []
		hourMinute = []

		for line in to_format:
			#print line[:9]
			totalDateTime.append("20" + line[:9])
			yearMonth.append("20" + line[:4])
			day.append(line[4:6])
			hourMinute.append(line[6:10])
		
		return totalDateTime, yearMonth, day, hourMinute

class WeatherWriter:
	'''Class used to print formatted data to a file.'''

	def __init__(self, fileObject_in, fileName_in):
		'''sets up the formatter object with the file object created by the reader'''
		self.fileObject = fileObject_in
		self.fileName = fileName_in
		self.writeObject()

	def writeObject(self):
		'''prints object passed in '''
		import csv

		f = open(self.fileName, "wb")

		writer = csv.writer(f)
	
		for item in self.fileObject:
			writer.writerow(item)

		'''
		for item in self.fileObject:
			f.write("%s\n" % item + "\n")
			#print item
		'''
		f.close()

def main():
	#test code:
	import csv

	#daily weather data
	readerObject_day = WeatherReader("Daily_Lister.txt")
	fileContainer_day = readerObject_day.readFile()
	formatObject_day = DailyListerFormatter(fileContainer_day)
	formattedObject_day = formatObject_day.format()
	weatherWrite_day = WeatherWriter(formattedObject_day, "DailyLister_csvOutput.csv")

	#monthly weather data in individual days
	readerObject_month = WeatherReader("Individual_Days.txt")
	fileContainer_month = readerObject_month.readFile()
	formatObject_month = IndividualDaysFormatter(fileContainer_month)
	formattedObject_month = formatObject_month.format()
	weatherWrite_month = WeatherWriter(formattedObject_month, "IndividualDays_csvOutput.csv")
	
#main()
