from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#This is Registration model which  has ONETORELATION with User model directly and have common fields
class Registration(models.Model):
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    dob=models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.First_name

class Position(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

#This is model of candidate
class Candidate(models.Model):
    full_name = models.CharField(max_length=30)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    total_vote = models.IntegerField(default=0)
    def __str__(self):
        return "{} - {}".format(self.full_name,self.position.title)

class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.position, self.status)




