from django.shortcuts import render
import app.ProcessRWWA

def index(request):
    return render(request, 'app/index.html')

def process(request):
	if 'meeting' in request.GET and request.GET['meeting']:
		context = {
			'meeting' : request.GET['meeting'],
			'start_date' : app.ProcessRWWA.GetStartDate(request.GET['meeting']),
			'race_count' : app.ProcessRWWA.GetRaceCount(request.GET['meeting']),
			'data' : app.ProcessRWWA.ProcessRWWA(request.GET['meeting']),
			'active' : True
		}
	else:
		context = {
			'meeting' : -1,
			'start_date' : 'NODATA',
			'race_count' : 'NODATA',
			'data' : 'NODATA',
			'active' : False
		}
	return render(request, 'app/process.html', context)

