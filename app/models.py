from django.db import models

# Create your models here.

class RwwaMeeting(models.Model):
	meetingNumber = models.IntegerField()
	startDate = models.DateField()
	raceCount = models.IntegerField()
	
class RwwaRace(models.Model):
	meeting = models.ForeignKey(RwwaMeeting, on_delete=models.CASCADE)
	raceNumber = models.IntegerField()
	
class RwwaHorse(models.Model):
	race = models.ForeignKey(RwwaRace, on_delete=models.CASCADE)
	horseNumber = models.IntegerField()
	horseName = models.CharField(max_length=60)
	horseBarrier = models.IntegerField()
	horseRider = models.CharField(max_length=60)
	horseTrainer = models.CharField(max_length=60)
	horseOdds = models.CharField(max_length=10)
	