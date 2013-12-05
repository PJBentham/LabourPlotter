import pygmaps, csv, xlrd, datetime
workbook = xlrd.open_workbook('Digital Board.xls')
sunday = workbook.sheet_by_name('Sunday')
monday = workbook.sheet_by_name('Monday')
tuesday = workbook.sheet_by_name('Tuesday')
wednesday = workbook.sheet_by_name('Wednesday')
thursday = workbook.sheet_by_name('Thursday')
friday = workbook.sheet_by_name('Friday')
saturday = workbook.sheet_by_name('Saturday')
sunjobs = {} #
monjobs = {} #
tuejobs = {} #Empty dictionaries waiting for job info to be put in by 'getjobs', which picks up 'job number,
wedjobs = {} #location, postcode, start time & number of men required' from the required sheet (each allocated
thujobs = {} #to variable) in the file (allocated to the variable 'workbook')
frijobs = {} #
satjobs = {} #
daysofweek = {sunday:sunjobs, monday:monjobs, tuesday:tuejobs, wednesday:wedjobs, thursday:thujobs, friday:friday, saturday:satjobs} #dictionary of sheets and info, required for the getjobs function
jobslist = [sunjobs, monjobs, tuejobs, wedjobs, thujobs, frijobs, satjobs] #list of job dictionarys to be used in the main programme
start_row = 2 #used to show the information cells don't start until the 3rd row in the excel file (or 2nd if starting to count at 0)
filename = 1 #used to name the html files, to differentiate each days jobs

def getjobs(day, jobsdic): #populates a dictionary with the information from the excel sheet
	for i in range(start_row,day.nrows):
		jobsdic[i-1] = [str(day.cell_value(i,0)).upper(), str(day.cell_value(i,1)).upper(), str(day.cell_value(i,2)).upper(), str(xlrd.xldate_as_tuple(day.cell_value(i,3),0)[3])+":"+str(xlrd.xldate_as_tuple(day.cell_value(i,3),0)[4]), str(day.cell_value(i,4)).upper()]

def getlatlng(jobsdic): #gets the latitudes and longitudes from the csv file and appends them to the dictionaries as a tuple
	for i in jobsdic:
		with open('postcodes.csv', 'rb') as f: #see http://docs.python.org/2/library/csv.html#csv-examples
			reader = csv.reader(f)
			for row in reader:
				if row[0] == jobsdic[i][2]:
					jobsdic[i].append((row[1],row[2]))
                        else:
                            jobsdic[i].append((54.764919,-1.368824))

def plotjobs(x,y): #plots the latitude and longitudes of a job on a map (x would be the job dictionary, y is used to differentiate the filename)
    mymap = pygmaps.maps(53.644638, -2.526855, 7)
    for i in x:
		title = "Job Number: "+x[i][0]+", Location: "+x[i][1]+", Postcode: "+x[i][2]+", Start Time: "+x[i][3]+", No of Men: "+x[i][4]
		mymap.addpoint(float(x[i][5][0]), float(x[i][5][1]), "#0000FF",title)
    mymap.draw('./'+str(y)+'digiboard.html')


for i in daysofweek: #populating all dictionarires with the info from each days sheet
    getjobs(i, daysofweek[i])

for i in jobslist: #produces a different html file for each sheet in the workbook with markers on for each job on that day - jackpot!
    getlatlng(i)
    plotjobs(i, filename)
    filename += 1
