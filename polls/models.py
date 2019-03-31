from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Positions(models.Model):

	position = models.CharField(max_length=5,
		choices=(
			("PR", "President"),
			("VP", "Vice President"),
			("HG", "Honorary Secretary"),
			("None", "Choose position")
		),
		default="None"
	)

	def __str__(self):
		return self.position

class Applicant(models.Model):
	
	name = models.CharField(max_length=200) 
	year = models.IntegerField(
		choices=(
			(1, '1'),
			(2, '2'),
			(3, '3'),
			(4, '4')
		),
		default=1
	)
	major = models.CharField(max_length=200)

	choices = models.ManyToManyField(Positions, through='Choice')

	image = models.ImageField(upload_to='applicant photos', blank=True)

	def __str__(self):
		return self.name

class Choice(models.Model):

	choice = models.ForeignKey(Positions, on_delete=models.CASCADE)
	applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

	number_of_votes = models.IntegerField(default=0)

	number_of_votes_against = models.IntegerField(default=0)

	class Meta:
		ordering = ['choice', '-number_of_votes']

	def __str__(self):
		return self.applicant.name + '__' + self.choice.position + '__' + str(self.number_of_votes)


class Vote(models.Model):

	vote = models.ForeignKey(Choice, on_delete=models.CASCADE)

	voter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	vote_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.voter.username + '__' + self.vote.choice.__str__()

	class Meta:
		ordering = ['voter', 'vote']
		unique_together = (("vote", "voter"),)




	