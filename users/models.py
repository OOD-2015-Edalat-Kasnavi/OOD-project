from django.db import models
from django.contrib.auth.models import User, AnonymousUser


class KUser(models.Model):
	user = models.OneToOneField(User)
	realName = models.CharField(max_length=255)
	job = models.CharField(max_length=255)
	privilege = models.IntegerField()
	employeeId = models.IntegerField(unique=True)
	state = models.IntegerField()

	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

	def __str__(self):
		return 'User: ' + self.user.username



class Manager(KUser):
	class Meta:
		verbose_name = 'Manager'
		verbose_name_plural = 'Managers'

	def __str__(self):
		return 'Manager: ' + self.user.username


def getKnowledgeUser(usr):
	if isinstance(usr, AnonymousUser):
		return None

	if Manager.objects.filter(user__pk=usr.pk):
		return Manager.objects.get(user__pk=usr.pk)

	if KUser.objects.filter(user__pk=usr.pk):
		return KUser.objects.get(user__pk=usr.pk)

	return None


