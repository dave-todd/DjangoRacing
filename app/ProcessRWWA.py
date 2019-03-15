import webbrowser, sys, requests, bs4, re, datetime, time, html5lib

def GetStartDate(meeting):
    address = "http://www.rwwa.com.au/cris/meeting.aspx?meeting=" + meeting
    res = requests.get(address)
    try:
        res.raise_for_status()
    except Exception as exc:
        return('There was a problem: %s' % (exc))
    racenoSoup = bs4.BeautifulSoup(res.text, "html5lib")
    temp = str(racenoSoup.find("span", {"id": "ctl00_ContentPlaceHolderMain_labelTitle"}))
    temp = temp[51:-7]
    temp = temp[-10:]
    retVal = datetime.datetime.strptime(temp, "%d/%m/%Y").date()
    return(retVal)
	
def GetRaceCount(meeting):
    address = "http://www.rwwa.com.au/cris/meeting.aspx?meeting=" + meeting
    res = requests.get(address)
    try:
        res.raise_for_status()
    except Exception as exc:
        return('There was a problem: %s' % (exc))
    racenoSoup = bs4.BeautifulSoup(res.text, "html5lib")
    table = racenoSoup.find("table", {"class": "tblcris"})
    raceList = table.findAll("tr")
    return (len(raceList)-1)
	
def GetHorseNum(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    return(temp)

def GetHorseName(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    if temp[:7] == "bgcolor": # deal with a very strange background colour issue that appears every now and then
        temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[:temp.find("<")] # remove everything after <
    temp = temp.replace("&amp;", "&") # change html & to &
    return(temp)
    
def GetHorseBr(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    return(temp)
    
def GetHorseRider(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    if temp[:7] == "bgcolor": # deal with a very strange background colour issue that appears every now and then
        temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[:temp.find("<")] # remove everything after <
    temp = temp.replace("&amp;", "&") # change html & to &
    return(temp)
    
def GetHorseTrainer(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    if temp[:7] == "bgcolor": # deal with a very strange background colour issue that appears every now and then
        temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[:temp.find("<")] # remove everything after <
    temp = temp.replace("&amp;", "&") # change html & to &
    return(temp)

def GetHorseOdds(garbage):
    temp = garbage[4:-5] # remove <td> </td> from ends
    temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[temp.find(">")+1:] # remove everything before >
    temp = temp[:temp.find("<")] # remove everything after <
    temp = temp.replace("&amp;", "&") # change html & to &
    return(temp)
	
def ProcessRace(meeting, raceNum):
	race=[]
	address = "http://www.rwwa.com.au/cris/racefield.aspx?meeting="+meeting+"&race="+str(raceNum)
	res = requests.get(address)
	
	try:
		res.raise_for_status()
	except Exception as exc:
		return('There was a problem: %s' % (exc))
	
	racenoSoup = bs4.BeautifulSoup(res.text, "html5lib")
	table = racenoSoup.find("table", {"class":"tblcris raceField"})
	rows = table.findAll("tr")
	
	for row in rows:
		column = 0
		horseNum = "?"
		horseName = "?"
		horseBr = "?"
		horseRider = "?"
		horseTrainer = "?"
		horseOdds = "?"

		fields = row.findAll("td")
		for field in fields: # lets see all the td's in each tr
			if column == 1:
				horseNum = GetHorseNum(str(field))
			elif column == 2:
				horseName = GetHorseName(str(field))
			elif column == 5:
				horseBr = GetHorseBr(str(field))
			elif column == 8:
				horseRider = GetHorseRider(str(field))
			elif column == 9:
				horseTrainer = GetHorseTrainer(str(field))
			elif column == 10:
				horseOdds = GetHorseOdds(str(field))
			column += 1
			
		if (horseName != "?") & (horseOdds != "       S"):
			horse = [horseNum, horseName, horseBr, horseRider, horseTrainer, horseOdds]
			race.append(horse)
			
	return(race)

def ProcessRWWA(meeting):
	retVal=[]
	raceCount = GetRaceCount(meeting)
	for raceNum in range(1, raceCount+1):
		raceData = ProcessRace(meeting, raceNum)
		retVal.append(raceData)
	return(retVal)