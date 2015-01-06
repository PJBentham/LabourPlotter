import pygmapsedit, csv, xlrd, datetime, time
from geopy import geocoders

geocode =   geocoders.GoogleV3()
            #geocoders.Yahoo('sqrWssjV34Gt8SyEoXHOljAbjI.w2o09XBQnDwu8wdhJP.rRHAhMRL1xTYjiZaqP')
            #geocoders.GeoNames()

pclatlng = {}

with open('postcodes.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        pclatlng[row[0]] = row[1], row[2]

class Day:                                  			#Day takes 2 args - 'day', which is a worksheet variable,
    def __init__(self, day, name):          	#and name, which is used for the filename (must be a string)
        self.day = day
        self.name = name
        self.jobs = {}
        self.no_jobs = 0
        self.start_row = 2
        self.last_row = self.day.nrows
        self.date = str(str(xlrd.xldate_as_tuple(day.cell_value(0,0),0)[2])+"."+str(xlrd.xldate_as_tuple(day.cell_value(0,0),0)[1])+"."+str(xlrd.xldate_as_tuple(day.cell_value(0,0),0)[0]))

        for i in range(self.start_row,self.last_row):
            try:
                self.jobs[i-1] =   [str(self.day.cell_value(i,0)).upper(), \
                                    str(self.day.cell_value(i,1)).upper(), \
                                    str(self.day.cell_value(i,2)).upper(), \
                                    str(self.day.cell_value(i,3)).upper(), \
                                    str(xlrd.xldate_as_tuple(self.day.cell_value(i,4),0)[3])+":"+str(xlrd.xldate_as_tuple(self.day.cell_value(i,4),0)[4]), \
                                    str(self.day.cell_value(i,5)).upper(), \
                                    str(self.day.cell_value(i,6)).upper(), \
                                    str(self.day.cell_value(i,7)).upper(), \
                                    str(self.day.cell_value(i,8)).upper(), \
                                    str(self.day.cell_value(i,9)).upper(), \
                                    str(self.day.cell_value(i,10)).upper(), \
                                    str(self.day.cell_value(i,11)).upper(), \
                                    str(self.day.cell_value(i,12)).upper(), \
                                    str(self.day.cell_value(i,13)).upper(), \
                                    str(self.day.cell_value(i,14)).upper(), \
                                    str(self.day.cell_value(i,15)).upper(), \
                                    str(self.day.cell_value(i,16)).upper(), \
                                    str(self.day.cell_value(i,17)).upper(), \
                                    str(self.day.cell_value(i,18)).upper()]
            except ValueError:
                print "It look's like one of your 'time' cells is incorrect!"
                self.jobs[i-1] =   [str(self.day.cell_value(i,0)).upper(), \
                                    str(self.day.cell_value(i,1)).upper(), \
                                    str(self.day.cell_value(i,2)).upper(), \
                                    str(self.day.cell_value(i,3)).upper(), \
                                    "missing", \
                                    str(self.day.cell_value(i,5)).upper(), \
                                    str(self.day.cell_value(i,6)).upper(), \
                                    str(self.day.cell_value(i,7)).upper(), \
                                    str(self.day.cell_value(i,8)).upper(), \
                                    str(self.day.cell_value(i,9)).upper(), \
                                    str(self.day.cell_value(i,10)).upper(), \
                                    str(self.day.cell_value(i,11)).upper(), \
                                    str(self.day.cell_value(i,12)).upper(), \
                                    str(self.day.cell_value(i,13)).upper(), \
                                    str(self.day.cell_value(i,14)).upper(), \
                                    str(self.day.cell_value(i,15)).upper(), \
                                    str(self.day.cell_value(i,16)).upper(), \
                                    str(self.day.cell_value(i,17)).upper(), \
                                    str(self.day.cell_value(i,18)).upper()]

        self.no_jobs = len(self.jobs)

        for i in self.jobs:
            multiple={}
            job = self.jobs[i]
            postcode = job[1]
            placename = job[3]
            try:
                if postcode in pclatlng:
                    job.insert(2,(pclatlng[postcode][0],pclatlng[postcode][1]))   
                else:
                    result = [geocode.geocode(placename,exactly_one=None)]
                    if len(result[0])>1:
                        multiple[placename] = geocode.geocode(placename,exactly_one=None)
                        favourite = raw_input("Multiple points found for this address, please choose one of the following (number & enter): \n"+",\n".join([str(a)+":"+str(b) for a,b in enumerate(multiple[placename])])+"\n>") #http://stackoverflow.com/questions/7301040/pulling-raw-input-options-form-a-list
                        placename = multiple[placename][int(favourite)][0]
                        job.insert(2,geocode.geocode(placename,exactly_one=None)[0][1])    
                    else:
                        job.insert(2,geocode.geocode(placename,exactly_one=None)[0][1])
                        time.sleep(2)
            except ValueError as error_message:
                print("Error: geocode failed on input %s with message %s"%(placename, error_message))
                continue 

        self.job_numbers = []
        self.clients = []
        self.locations = []
        self.postcodes = []
        self.latlngs = []
        for i in range(2,len(self.jobs)+2):
            self.job_numbers.append(self.jobs[i-1][0])
            self.clients.append(self.jobs[i-1][1])
            self.locations.append(self.jobs[i-1][2])
            self.postcodes.append(self.jobs[i-1][4])
            self.latlngs.append(self.jobs[i-1][3])

    def plotjobs(self):
        mymap = pygmapsedit.maps(53.644638, -2.526855, 6)
        for i in self.jobs:
            job = self.jobs[i]
            info = "<img style = 'float: left' src='icon-job.png'><div style = 'display: inline-block; width: 200px'>"\
            "<p><b>Job Number:</b> " +job[0]+"</p>"\
            "<p><b>Client:</b> "+job[1]+"</p>"\
            "<p><b>Location:</b> "+job[2]+"</p>"\
            "<p><b>Postcode:</b> "+job[4]+"</p>"\
            "<p><b>Start Time:</b> "+job[5]+"</p>"\
            "<p><b>No of Men:</b> "+job[6]+"</p>"\
            "<p><b>Allocated Labour:</b> "\
            +job[7]+": "+job[8]+", "\
            +job[9]+": "+job[10]+", " \
            +job[11]+": "+job[12]+", "\
            +job[13]+": "+job[14]+", "\
            +job[15]+": "+job[16]+", "\
            +job[17]+": "+job[18]+"</p>"\
            "<p><b>Job Information: </b>"+job[19]+"</div>"
            mymap.addpoint(float(job[3][0]), float(job[3][1]), "#0000FF",None,info,None)
        mymap.draw("./"+str(self.name)+"'s Labour.html")

class Rollout:                                  
    def __init__(self, team, name):
        self.team = team
        self.name = name
        self.jobs = {}
        self.start_row = 1
        self.last_row = self.team.nrows

        for i in range(self.start_row,self.last_row):
                try:
                    self.jobs[i-1] =   [str(self.team.cell_value(i,0)).upper(), \
                                        str(self.team.cell_value(i,1)).upper(), \
                                        str(self.team.cell_value(i,2)).upper(), \
                                        str(self.team.cell_value(i,4)).upper(), \
                                        str(self.team.cell_value(i,5)).upper(), \
                                        str(self.team.cell_value(i,6)).upper()]
                except ValueError:
                    print "It look's like one of your 'time' cells is incorrect!"
                    self.jobs[i-1] =   [str(self.team.cell_value(i,0)).upper(), \
                                        str(self.team.cell_value(i,1)).upper(), \
                                        str(self.team.cell_value(i,2)).upper(), \
                                        str(self.team.cell_value(i,4)).upper(), \
                                        "missing", \
                                        str(self.team.cell_value(i,5)).upper(), \
                                        str(self.team.cell_value(i,6)).upper()]
        
        for i in self.jobs:
            multiple={}
            job = self.jobs[i]
            postcode = job[1]
            placename = job[3]
            try:
                if postcode in pclatlng:
                    job.insert(2,(pclatlng[postcode][0],pclatlng[postcode][1]))   
                else:
                    result = [geocode.geocode(placename,exactly_one=None)]
                    if len(result[0])>1:
                        multiple[placename] = geocode.geocode(placename,exactly_one=None)
                        favourite = raw_input("Multiple points found for this address, please choose one of the following (number & enter): \n"+",\n".join([str(a)+":"+str(b) for a,b in enumerate(multiple[placename])])+"\n>") #http://stackoverflow.com/questions/7301040/pulling-raw-input-options-form-a-list
                        placename = multiple[placename][int(favourite)][0]
                        job.insert(2,geocode.geocode(placename,exactly_one=None)[0][1])    
                    else:
                        job.insert(2,geocode.geocode(placename,exactly_one=None)[0][1])
                        time.sleep(2)
            except ValueError as error_message:
                print("Error: geocode failed on input %s with message %s"%(placename, error_message))
                continue     

    def plotjobs(self):
        mymap = pygmapsedit.maps(53.644638, -2.526855, 6)
        for i in self.jobs:
            job = self.jobs[i]
            info = "<img style = 'float: left' src='icon-job.png'><div style = 'display: inline-block; width: 200px'>"\
            "<p><b>Job Number:</b> " +job[0]+"</p>"\
            "<p><b>Postcode:</b> "+job[1]+"</p>"\
            "<p><b>Distance to Next Store:</b> "+job[3]+"</p>"\
            "<p><b>Store Name:</b> "+job[4]+"</p>"\
            "<p><b>Store Address:</b> "+job[5]+"</p>"
            mymap.addpoint(float(job[2][0]), float(job[2][1]), "#0000FF",None,info,str(int(float(self.jobs[i][0]))))
        mymap.draw("./"+str(self.name)+"'s Route.html")    

#--------------------------------------------------------#
# Code for Rollouts:
<<<<<<< HEAD
workbook = xlrd.open_workbook('Example Rollout.xls')
team1 = workbook.sheet_by_name('Team 1')

Team1 = Rollout(team1, 'Team 1')

Team1.plotjobs()
=======
#workbook = xlrd.open_workbook('your_rollout.xls')
#team1 = workbook.sheet_by_name('Team 1')
#team2 = workbook.sheet_by_name('Team 2')
#team20 = workbook.sheet_by_name('Team 20')

#Team1 = Rollout(team1, 'Team 1')
#Team2 = Rollout(team2, 'Team 2')
#Team20 = Rollout(team20, 'Team 20')

#Team1.plotjobs()
#Team2.plotjobs()
#Team20.plotjobs()
>>>>>>> 781b713bc6ddf1a6dc66d83f9e02ce8b7e890cbf

#--------------------------------------------------------#


#-----------------------------------------------------#
# Code for the Boards:
# workbook = xlrd.open_workbook('your_labour.xls')
# sunday = workbook.sheet_by_name('Sunday')
# monday = workbook.sheet_by_name('Monday')
# tuesday = workbook.sheet_by_name('Tuesday')
# wednesday = workbook.sheet_by_name('Wednesday')
# thursday = workbook.sheet_by_name('Thursday')
# friday = workbook.sheet_by_name('Friday')
# saturday = workbook.sheet_by_name('Saturday')

# Sunday = Day(sunday, 'sunday')
# Sunday.plotjobs()
# Monday = Day(monday, 'monday')
# Monday.plotjobs()
# Tuesday = Day(tuesday, 'tuesday')
# Tuesday.plotjobs()
# Wednesday = Day(wednesday, 'wednesday')
# Wednesday.plotjobs()
# Thursday = Day(thursday, 'thursday')
# Thursday.plotjobs()
# Friday = Day(friday, 'friday')
# Friday.plotjobs()
# Saturday = Day(saturday, 'saturday')
# Saturday.plotjobs()
#----------------------------------------------------#
