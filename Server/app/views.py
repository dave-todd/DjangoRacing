from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import app.ProcessRWWA
from app.models import RwwaMeeting, RwwaRace, RwwaHorse

def Index(request):
	try:
		return render(request, 'app/index.html')
	except:
		return HttpResponse(status=400)

def Process(request):
	try:
		context = { 'active' : False }
		if 'meeting' in request.GET and request.GET['meeting']:
			meetingNumber = request.GET['meeting']
			startDate, raceCount = app.ProcessRWWA.GetMeetingData(meetingNumber)
			if raceCount > 0:
				races = app.ProcessRWWA.ProcessRWWA(meetingNumber, raceCount)
				context = {
					'meeting' : meetingNumber,
					'startDate' : startDate,
					'raceCount' : raceCount,
					'races' : races,
					'active' : True
				}
		return render(request, 'app/process.html', context)
	except:
		return HttpResponse(status=400)

def REST_Process(request, meetingNumber):
	try:
		meetingResponse = {}
		if request.method == 'GET':
			startDate, raceCount = app.ProcessRWWA.GetMeetingData(meetingNumber)
			if raceCount > 0:
							
				meetingResponse['meetingNumber'] = meetingNumber
				meetingResponse['startDate'] = startDate
				meetingResponse['raceCount'] = raceCount
				
				races = app.ProcessRWWA.ProcessRWWA(meetingNumber, raceCount)
				raceNumber = 0
				for race in races:
					raceResponse = {}
					raceNumber += 1
					
					horseCount = 0
					for horse in race:
						horseCount += 1
					
					raceResponse['raceNumber'] = raceNumber
					raceResponse['horseCount'] = horseCount

					for horse in race:
						horseResponse = {}
						horseResponse['horseNumber'] = int(horse[0])
						horseResponse['horseName'] = horse[1]
						horseResponse['horseBarrier'] = int(horse[2])
						horseResponse['horseRider'] = horse[3]
						horseResponse['horseTrainer'] = horse[4]
						horseResponse['horseOdds'] = horse[5]
						
						raceResponse['horse'+str(horse[0])] = horseResponse

					meetingResponse['race'+str(raceNumber)] = raceResponse
				
		return JsonResponse(meetingResponse)
	except:
		return HttpResponse(status=400)
		
def Database(request):
	try:
		meetingNumber = 17555 # hard coded just for demonstration purposes.  In production I would provide a form and let the user chose the meeting number
		startDate, raceCount = app.ProcessRWWA.GetMeetingData(meetingNumber)
		if raceCount > 0:
			racesData = app.ProcessRWWA.ProcessRWWA(meetingNumber, raceCount)
			
			meetingModel = RwwaMeeting()
			meetingModel.meetingNumber = meetingNumber
			meetingModel.startDate = startDate
			meetingModel.raceCount = raceCount
			meetingModel.save()
			
			raceNumber=0
			for race in racesData:
				raceNumber += 1
				raceModel = RwwaRace()
				raceModel.meeting = meetingModel
				raceModel.raceNumber = raceNumber
				raceModel.save()
				
				for horse in race:
					horseModel = RwwaHorse()
					horseModel.race = raceModel
					horseModel.horseNumber = int(horse[0])
					horseModel.horseName = horse[1]
					horseModel.horseBarrier = int(horse[2])
					horseModel.horseRider = horse[3]
					horseModel.horseTrainer = horse[4]
					horseModel.horseOdds = horse[5]
					horseModel.save()
			
		return render(request, 'app/database.html')
	except:
		return HttpResponse(status=400)